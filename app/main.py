from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.errors import (ProblemDetails, RequestIDMiddleware, http_error_handler,
                        validation_error_handler)
from app.matching_engine import MODEL_VERSION

from app.employee_service import get_employee, get_employees
from app.job_service import get_job
from app.recommendation_service import recommend_employees
from app.schemas import Employee, Job, RecommendationRequest, RecommendationResponse


app = FastAPI(
    title="SkillMatch AI",
    version="0.1.0",
    description="Human-reviewed workforce matching recommendations.",
    responses={status: {"description": "Problem response",
                        "content": {"application/problem+json": {
                            "schema": {"$ref": "#/components/schemas/ProblemDetails"}}}}
               for status in (400, 401, 403, 404, 405, 409, 422, 429, 500, 501, 503)},
)


app.add_middleware(RequestIDMiddleware)
app.add_exception_handler(StarletteHTTPException, http_error_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


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
        match_run_id=str(uuid4()),
        model_version=MODEL_VERSION,
        recommendations=recommend_employees(
            job,
            request.candidate_employee_ids,
            request.top_k,
            request.minimum_score,
            request.include_missing_skills,
        ),
    )



def custom_openapi() -> dict:
    if app.openapi_schema is None:
        schema = get_openapi(title=app.title, version=app.version,
                             description=app.description, routes=app.routes)
        problem_schema = ProblemDetails.model_json_schema(
            ref_template="#/components/schemas/{model}"
        )
        components = schema.setdefault("components", {}).setdefault("schemas", {})
        components.update(problem_schema.pop("$defs", {}))
        components["ProblemDetails"] = problem_schema
        for path in schema["paths"].values():
            for operation in path.values():
                if not isinstance(operation, dict) or "responses" not in operation:
                    continue
                for response in operation["responses"].values():
                    response.setdefault("headers", {})["X-Request-ID"] = {
                        "description": "Request correlation identifier.",
                        "schema": {"type": "string"},
                    }
        app.openapi_schema = schema
    return app.openapi_schema


app.openapi = custom_openapi
