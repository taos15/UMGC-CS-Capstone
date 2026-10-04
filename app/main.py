from fastapi import FastAPI, HTTPException

from app.endpoint_stubs import router as stub_router
from app.employee_service import get_employee, get_employees
from app.job_service import get_job
from app.recommendation_service import recommend_employees
from app.schemas import Employee, Job, RecommendationRequest, RecommendationResponse


app = FastAPI(
    title="SkillMatch AI",
    version="0.1.0",
    description="Human-reviewed workforce matching recommendations.",
)


@app.get("/health", include_in_schema=False)
@app.get("/api/v1/health", openapi_extra={"x-role-policy": "unspecified"},
         description="Operations endpoint; role policy is unspecified in the design specification.")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/v1/employees", response_model=list[Employee],
         openapi_extra={"x-allowed-roles": ["ADMIN", "SUPERVISOR", "VIEWER"]},
         description="Allowed roles: ADMIN, SUPERVISOR, VIEWER.")
def list_employees() -> list[Employee]:
    return get_employees()


@app.get("/api/v1/employees/{employee_id}", response_model=Employee,
         openapi_extra={"x-allowed-roles": ["ADMIN", "SUPERVISOR", "VIEWER"]},
         description="Allowed roles: ADMIN, SUPERVISOR, VIEWER.")
def retrieve_employee(employee_id: str) -> Employee:
    employee = get_employee(employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@app.get("/api/v1/jobs/{job_id}", response_model=Job,
         openapi_extra={"x-allowed-roles": ["ADMIN", "SUPERVISOR", "VIEWER"]},
         description="Allowed roles: ADMIN, SUPERVISOR, VIEWER.")
def retrieve_job(job_id: str) -> Job:
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@app.post(
    "/api/v1/jobs/{job_id}/recommendations",
    response_model=RecommendationResponse,
    openapi_extra={"x-allowed-roles": ["ADMIN", "SUPERVISOR"]},
    description="Allowed roles: ADMIN, SUPERVISOR. Supervisor retains final staffing authority.",
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


app.include_router(stub_router)
