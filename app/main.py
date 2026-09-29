from fastapi import FastAPI, HTTPException
from sqlalchemy import text

from app.employee_service import get_employee, get_employees
from app.job_service import get_job
from app.recommendation_service import recommend_employees
from app.schemas import Employee, Job, RecommendationRequest, RecommendationResponse
from backend.database import engine


app = FastAPI(
    title="SkillMatch AI",
    version="0.1.0",
    description="Human-reviewed workforce matching recommendations.",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/v1/health")
def health_check_v1() -> dict[str, str]:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        database_status = "ok"
    except Exception:
        database_status = "unavailable"

    return {
        "status": "ok" if database_status == "ok" else "degraded",
        "database": database_status,
    }


@app.get("/api/v1/employees", response_model=list[Employee])
def list_employees() -> list[Employee]:
    return get_employees()


@app.get("/api/v1/employees/{employee_id}", response_model=Employee)
def retrieve_employee(employee_id: str) -> Employee:
    employee = get_employee(employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@app.get("/api/v1/jobs/{job_id}", response_model=Job)
def retrieve_job(job_id: str) -> Job:
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@app.post(
    "/api/v1/jobs/{job_id}/recommendations",
    response_model=RecommendationResponse,
)
def create_recommendations(
    job_id: str, request: RecommendationRequest
) -> RecommendationResponse:
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return RecommendationResponse(
        jobId=job.id,
        recommendations=recommend_employees(
            job,
            request.candidate_employee_ids,
            request.top_k,
            request.minimum_score,
            request.include_missing_skills,
        ),
    )
