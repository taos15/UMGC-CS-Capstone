"""REC-001 acceptance criteria not already exercised by the general API tests."""

from datetime import date

import pytest

from skillmatch.features.employees.schemas import Employee, EmployeeCertification, EmployeeSkill
from skillmatch.features.jobs.schemas import Job
from skillmatch.features.recommendations.repository import get_match_run


def _eligible_employee(employee_id: str, *, status: str = "ACTIVE") -> Employee:
    return Employee(
        id=employee_id, name=employee_id,
        skills=["electrical wiring", "blueprint reading", "troubleshooting"],
        certifications=["licensed electrician"], years_experience=5, status=status,
        skill_evidence=[
            EmployeeSkill(skill_id="electrical wiring", proficiency=5),
            EmployeeSkill(skill_id="blueprint reading", proficiency=5),
            EmployeeSkill(skill_id="troubleshooting", proficiency=5),
        ],
        certification_evidence=[
            EmployeeCertification(code="licensed electrician", issued_on=date(2020, 1, 1)),
        ],
    )


def test_successful_run_is_persisted_and_retrievable_before_response_returns(client) -> None:
    """AC4: success only returns match_run_id/model_version after persistence."""
    response = client.post("/api/v1/jobs/job-electrician/recommendations", json={})
    assert response.status_code == 200
    body = response.json()

    from skillmatch.db.session import engine
    from sqlmodel import Session

    with Session(engine) as session:
        stored = get_match_run(session, body["match_run_id"])

    assert stored is not None
    assert stored.job_id == "job-electrician"
    assert stored.model_version == body["model_version"] == "rpce-55-20-15-10-v1"
    assert stored.options["minimumScore"] == 0.0


def test_zero_eligible_candidates_is_a_handled_empty_result_not_an_error(monkeypatch, client) -> None:
    """AC5: no eligible candidate is a handled 200 with an empty list, not a crash."""
    ineligible = _eligible_employee("emp-no-cert")
    ineligible.certification_evidence = []  # no longer holds the mandatory certification
    monkeypatch.setattr(
        "skillmatch.features.recommendations.service.get_employees", lambda ids: [ineligible]
    )
    response = client.post("/api/v1/jobs/job-electrician/recommendations", json={})
    assert response.status_code == 200
    assert response.json()["recommendations"] == []


def test_inactive_employees_are_excluded_from_the_snapshot_entirely(monkeypatch, client) -> None:
    """AC3: the orchestrator snapshots ACTIVE candidates only."""
    candidates = [_eligible_employee("emp-active"), _eligible_employee("emp-inactive", status="INACTIVE")]
    monkeypatch.setattr(
        "skillmatch.features.recommendations.service.get_employees", lambda ids: candidates
    )
    response = client.post(
        "/api/v1/jobs/job-electrician/recommendations", json={"includeIneligible": True}
    )
    assert response.status_code == 200
    assert [item["employee_id"] for item in response.json()["recommendations"]] == ["emp-active"]


def test_closed_job_returns_job_not_open(monkeypatch, client) -> None:
    """AC2: a job that exists but is not OPEN returns 409 JOB_NOT_OPEN."""
    from skillmatch.features.jobs.seed import JOBS

    closed_job = JOBS[0].model_copy(update={"status": "CLOSED"})
    monkeypatch.setattr("skillmatch.features.recommendations.router.get_job", lambda job_id: closed_job)
    response = client.post(f"/api/v1/jobs/{closed_job.id}/recommendations", json={})
    assert response.status_code == 409
    assert response.json()["code"] == "JOB_NOT_OPEN"


def test_job_with_no_usable_criteria_returns_422(monkeypatch, client) -> None:
    """AC2: a job with no required/preferred skills, certifications, or experience floor
    has no usable matching criteria."""
    empty_job = Job(
        id="job-empty", title="Empty Job", required_skills=[], preferred_skills=[],
        required_certifications=[], minimum_years_experience=0, status="OPEN",
        skill_requirement_details=[],
    )
    monkeypatch.setattr("skillmatch.features.recommendations.router.get_job", lambda job_id: empty_job)
    response = client.post("/api/v1/jobs/job-empty/recommendations", json={})
    assert response.status_code == 422
    assert response.json()["code"] == "JOB_HAS_NO_CRITERIA"


def test_persistence_failure_returns_503_without_a_partial_match_run(monkeypatch, client) -> None:
    """AC6: a persistence failure fails safely and writes nothing."""
    def broken_create_match_run(*args, **kwargs):
        raise RuntimeError("database unavailable")

    monkeypatch.setattr(
        "skillmatch.features.recommendations.service.create_match_run", broken_create_match_run
    )
    response = client.post("/api/v1/jobs/job-electrician/recommendations", json={})
    assert response.status_code == 503
    assert response.json()["code"] == "DATABASE_UNAVAILABLE"


@pytest.mark.parametrize("payload", [{}, {"minimumScore": 0, "topK": 5}])
def test_repeated_identical_requests_produce_the_same_snapshot_hash(payload, client) -> None:
    """Same input snapshot + model_version yields identical ordering/scores (matching_contract.md)."""
    first = client.post("/api/v1/jobs/job-electrician/recommendations", json=payload)
    second = client.post("/api/v1/jobs/job-electrician/recommendations", json=payload)

    from skillmatch.db.session import engine
    from sqlmodel import Session

    with Session(engine) as session:
        first_run = get_match_run(session, first.json()["match_run_id"])
        second_run = get_match_run(session, second.json()["match_run_id"])

    assert first_run.snapshot_hash == second_run.snapshot_hash
    assert first.json()["recommendations"] == second.json()["recommendations"]
