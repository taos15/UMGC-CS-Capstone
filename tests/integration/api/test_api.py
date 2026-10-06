import pytest



def test_health_check(client) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_check_v1_reports_database_status(client) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


def test_recommendations_are_ranked_and_support_request_options(client) -> None:
    response = client.post(
        "/api/v1/jobs/job-electrician/recommendations",
        json={
            "candidateEmployeeIds": ["emp-jordan", "emp-alex"],
            "topK": 1,
            "includeMissingSkills": False,
            "minimumScore": 0,
            "includeIneligible": True,
        },
    )

    assert response.status_code == 200
    result = response.json()
    assert result["jobId"] == "job-electrician"
    assert len(result["recommendations"]) == 1
    assert result["recommendations"][0]["employee_id"] == "emp-alex"
    assert result["recommendations"][0]["eligible"] is True
    assert result["recommendations"][0]["missing_skills"] == []
    assert result["recommendations"][0]["component_scores"] == {
        "required_skills": 1.0,
        "preferred_skills": 1.0,
        "required_certifications": 1.0,
        "experience": 1.0,
    }
    assert result["recommendations"][0]["score"] == 100.0


def test_missing_job_returns_not_found(client) -> None:
    response = client.post(
        "/api/v1/jobs/missing/recommendations",
        json={},
    )

    assert response.status_code == 404


def test_employee_and_job_reads_preserve_seed_data(client) -> None:
    employees = client.get("/api/v1/employees").json()
    assert [employee["id"] for employee in employees] == ["emp-alex", "emp-jordan", "emp-sam"]
    assert all(employee["status"] == "ACTIVE" for employee in employees)
    assert client.get("/api/v1/employees/emp-alex").json() == employees[0]
    from skillmatch.features.jobs.schemas import JobProfile
    job = JobProfile.model_validate(client.get('/api/v1/jobs/job-hvac').json())
    assert job.title == 'HVAC Technician'
    assert job.certification_requirements == ['epa 608']
    assert [item.skill_id for item in job.skill_requirements] == ['hvac repair', 'troubleshooting']
    assert [item.minimum_proficiency for item in job.skill_requirements] == [3, 3]
    assert [item.importance for item in job.skill_requirements] == [3, 2]
    assert job.status == 'OPEN'
    assert job.minimum_years_experience == 3
    assert job.version == 1



@pytest.mark.parametrize("path,detail", [
    ("/api/v1/employees/missing", "Employee not found."),
    ("/api/v1/jobs/missing", "Job not found."),
])
def test_missing_resources(path: str, detail: str, client) -> None:
    response = client.get(path)
    assert response.status_code == 404
    assert response.json() == {
        "type": "about:blank", "title": "Not Found", "status": 404,
        "code": "EMPLOYEE_NOT_FOUND" if "employees" in path else "JOB_NOT_FOUND", "request_id": response.headers["X-Request-ID"],
        "detail": detail, "field_errors": [],
    }


def test_recommendation_defaults_excludes_ineligible_candidates(client) -> None:
    """Jordan/Sam are missing the mandatory 'licensed electrician' certification,
    so they are eligibility-gated out of the default (include_ineligible=False) result."""
    response = client.post("/api/v1/jobs/job-electrician/recommendations", json={})
    assert response.status_code == 200
    recommendations = response.json()["recommendations"]
    assert [(item["employee_id"], item["score"]) for item in recommendations] == [
        ("emp-alex", 100.0)
    ]


def test_recommendation_with_ineligible_candidates_shown(client) -> None:
    response = client.post(
        "/api/v1/jobs/job-electrician/recommendations", json={"includeIneligible": True}
    )
    assert response.status_code == 200
    recommendations = response.json()["recommendations"]
    assert [(item["employee_id"], item["score"], item["eligible"]) for item in recommendations] == [
        ("emp-alex", 100.0, True),
        ("emp-jordan", 67.29, False),
        ("emp-sam", 25.71, False),
    ]
    assert recommendations[1]["missing_skills"] == ["blueprint reading"]
    assert recommendations[1]["missing_certifications"] == ["licensed electrician"]
    assert recommendations[1]["ineligible_reasons"] == [
        "MISSING_MANDATORY_CERTIFICATION:licensed electrician"
    ]
    assert recommendations[1]["explanation"] == (
        "Jordan Lee scored 67.29 for Commercial Electrician. "
        "Ineligible: MISSING_MANDATORY_CERTIFICATION:licensed electrician. "
        "Missing required skills: blueprint reading. "
        "Missing required certifications: licensed electrician."
    )


@pytest.mark.parametrize("options,expected", [
    ({"candidateEmployeeIds": []}, []),
    ({"candidateEmployeeIds": ["unknown"]}, []),
    ({"candidateEmployeeIds": ["emp-jordan", "emp-jordan"]}, []),
    ({"candidateEmployeeIds": ["emp-jordan", "emp-jordan"], "includeIneligible": True}, ["emp-jordan"]),
    ({"includeIneligible": True, "minimumScore": 30}, ["emp-alex", "emp-jordan"]),
    ({"includeIneligible": True, "minimumScore": 70}, ["emp-alex"]),
])
def test_recommendation_candidate_and_threshold_options(options: dict, expected: list[str], client) -> None:
    response = client.post("/api/v1/jobs/job-electrician/recommendations", json=options)
    assert response.status_code == 200
    assert [item["employee_id"] for item in response.json()["recommendations"]] == expected


@pytest.mark.parametrize("options", [
    {"topK": 0}, {"topK": 101}, {"minimumScore": -1}, {"minimumScore": 101}
])
def test_recommendation_validation(options: dict, client) -> None:
    assert client.post("/api/v1/jobs/job-electrician/recommendations", json=options).status_code == 422


def test_database_unavailable_health(monkeypatch: pytest.MonkeyPatch, client) -> None:
    def unavailable():
        raise RuntimeError("database unavailable")

    monkeypatch.setattr("skillmatch.main.engine.connect", unavailable)
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "degraded", "database": "unavailable"}
    assert client.get("/health").json() == {"status": "ok"}


def test_api_ties_are_independent_of_candidate_input_order(monkeypatch, client):
    from datetime import date
    from skillmatch.features.employees.schemas import Employee, EmployeeCertification, EmployeeSkill

    def make_employee(employee_id: str) -> Employee:
        return Employee(
            id=employee_id, name=employee_id,
            skills=['electrical wiring', 'blueprint reading', 'troubleshooting'],
            certifications=['licensed electrician'], years_experience=5,
            skill_evidence=[
                EmployeeSkill(skill_id='electrical wiring', proficiency=5),
                EmployeeSkill(skill_id='blueprint reading', proficiency=5),
                EmployeeSkill(skill_id='troubleshooting', proficiency=5),
            ],
            certification_evidence=[
                EmployeeCertification(code='licensed electrician', issued_on=date(2020, 1, 1)),
            ],
        )

    candidates = [make_employee(employee_id) for employee_id in ('z', 'a')]
    monkeypatch.setattr('skillmatch.features.recommendations.service.get_employees', lambda ids: candidates)
    first = client.post('/api/v1/jobs/job-electrician/recommendations', json={})
    candidates.reverse()
    second = client.post('/api/v1/jobs/job-electrician/recommendations', json={})
    assert first.status_code == second.status_code == 200
    assert first.json()['model_version'] == second.json()['model_version']
    recommendations = first.json()['recommendations']
    assert [item['employee_id'] for item in recommendations] == ['a', 'z']
    assert all(item['eligible'] for item in recommendations)
    # 80.0: full marks on required skills/cert/experience, but neither candidate
    # has the preferred "project coordination" skill (worth 20% weight).
    assert [item['score'] for item in recommendations] == [80.0, 80.0]
    assert [item['employee_id'] for item in second.json()['recommendations']] == ['a', 'z']
