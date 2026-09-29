from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_check_v1_reports_database_status() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


def test_recommendations_are_ranked_and_support_request_options() -> None:
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


def test_missing_job_returns_not_found() -> None:
    response = client.post(
        "/api/v1/jobs/missing/recommendations",
        json={},
    )

    assert response.status_code == 404
