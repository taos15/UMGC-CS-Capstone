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
        },
    )

    assert response.status_code == 200
    result = response.json()
    assert result["jobId"] == "job-electrician"
    assert len(result["recommendations"]) == 1
    assert result["recommendations"][0]["employeeId"] == "emp-alex"
    assert result["recommendations"][0]["missingRequirements"] == []
    assert result["recommendations"][0]["scoreBreakdown"] == {
        "requiredSkills": 50,
        "preferredSkills": 10,
        "requiredCertifications": 25,
        "experience": 15,
    }
    assert sum(result["recommendations"][0]["scoreBreakdown"].values()) == result[
        "recommendations"
    ][0]["score"]


def test_missing_job_returns_not_found(client) -> None:
    response = client.post(
        "/api/v1/jobs/missing/recommendations",
        json={},
    )

    assert response.status_code == 404


def test_employee_and_job_reads_preserve_seed_data(client) -> None:
    employees = client.get("/api/v1/employees").json()
    assert [employee["id"] for employee in employees] == ["emp-alex", "emp-jordan", "emp-sam"]
    assert client.get("/api/v1/employees/emp-alex").json() == employees[0]
    assert client.get("/api/v1/jobs/job-hvac").json() == {
        "id": "job-hvac",
        "title": "HVAC Technician",
        "required_skills": ["hvac repair", "troubleshooting"],
        "preferred_skills": [],
        "required_certifications": ["epa 608"],
        "minimum_years_experience": 3.0,
    }


@pytest.mark.parametrize("path,detail", [
    ("/api/v1/employees/missing", "Employee not found"),
    ("/api/v1/jobs/missing", "Job not found"),
])
def test_missing_resources(path: str, detail: str, client) -> None:
    response = client.get(path)
    assert response.status_code == 404
    assert response.json() == {
        "type": "about:blank", "title": "Not Found", "status": 404,
        "code": "NOT_FOUND", "request_id": response.headers["X-Request-ID"],
        "detail": detail, "field_errors": [],
    }


def test_recommendation_defaults_scores_and_explanation(client) -> None:
    response = client.post("/api/v1/jobs/job-electrician/recommendations", json={})
    assert response.status_code == 200
    recommendations = response.json()["recommendations"]
    assert [(item["employeeId"], item["score"]) for item in recommendations] == [
        ("emp-alex", 100.0), ("emp-jordan", 55.33), ("emp-sam", 31.67)
    ]
    assert recommendations[1]["missingRequirements"] == ["blueprint reading", "licensed electrician"]
    assert recommendations[1]["explanation"] == (
        "Jordan Lee matches 2 of 3 required skills and holds 0 of 1 required certifications. "
        "They have 4 years of experience, below the 5-year requirement. "
        "Missing requirements: blueprint reading, licensed electrician."
    )


@pytest.mark.parametrize("options,expected", [
    ({"candidateEmployeeIds": []}, []),
    ({"candidateEmployeeIds": ["unknown"]}, []),
    ({"candidateEmployeeIds": ["emp-jordan", "emp-jordan"]}, ["emp-jordan"]),
    ({"minimumScore": 55.33}, ["emp-alex", "emp-jordan"]),
    ({"minimumScore": 55.34}, ["emp-alex"]),
])
def test_recommendation_candidate_and_threshold_options(options: dict, expected: list[str], client) -> None:
    response = client.post("/api/v1/jobs/job-electrician/recommendations", json=options)
    assert response.status_code == 200
    assert [item["employeeId"] for item in response.json()["recommendations"]] == expected


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
    from skillmatch.features.employees.schemas import Employee
    candidates = [Employee(id=employee_id, name=employee_id, skills=['electrical wiring'],
                           certifications=['licensed electrician'], years_experience=5)
                  for employee_id in ('z', 'a')]
    monkeypatch.setattr('skillmatch.features.recommendations.service.get_employees', lambda ids: candidates)
    first = client.post('/api/v1/jobs/job-electrician/recommendations', json={})
    candidates.reverse()
    second = client.post('/api/v1/jobs/job-electrician/recommendations', json={})
    assert first.status_code == second.status_code == 200
    assert first.json()['model_version'] == second.json()['model_version']
    assert first.json()['recommendations'] == second.json()['recommendations']
    assert [item['employeeId'] for item in first.json()['recommendations']] == ['a', 'z']
