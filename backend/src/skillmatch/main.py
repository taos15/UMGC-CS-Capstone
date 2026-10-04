from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from starlette.exceptions import HTTPException as StarletteHTTPException

from skillmatch.core.errors import (
    ProblemDetails, ProblemError, RequestIDMiddleware, http_error_handler,
    problem_handler, validation_handler,
)
from skillmatch.features.auth.dependencies import get_authenticated_user
from sqlalchemy import text

from skillmatch.db.session import engine
from skillmatch.features.auth.router import router as auth_router
from skillmatch.features.skills.router import router as skills_router
from skillmatch.features.feedback.router import router as feedback_router
from skillmatch.features.employees.router import router as employees_router
from skillmatch.features.jobs.router import router as jobs_router
from skillmatch.features.recommendations.router import router as recommendations_router


app = FastAPI(
    title="SkillMatch AI",
    version="0.1.0",
    description="Human-reviewed workforce matching recommendations.",
    responses={status: {"description": "Problem response",
                        "content": {"application/problem+json": {
                            "schema": {"$ref": "#/components/schemas/ProblemDetails"}}}}
               for status in (400, 401, 403, 404, 405, 409, 422, 429, 500, 503)},
)


app.add_middleware(RequestIDMiddleware)
app.add_exception_handler(ProblemError, problem_handler)
app.add_exception_handler(StarletteHTTPException, http_error_handler)
app.add_exception_handler(RequestValidationError, validation_handler)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/v1/health", openapi_extra={"x-role-policy": "unspecified"},
         description="Operations endpoint; role policy is unspecified in the design specification.")
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


AUTH_REQUIRED_RESPONSE = {
    401: {"description": "Authentication required", "content": {
        "application/problem+json": {"schema": {"$ref": "#/components/schemas/ProblemDetails"}}}}
}

for protected_router in (employees_router, jobs_router, recommendations_router,
                         skills_router, feedback_router):
    app.include_router(protected_router, dependencies=[Depends(get_authenticated_user)],
                       responses=AUTH_REQUIRED_RESPONSE)


app.include_router(auth_router)


def custom_openapi() -> dict:
    if app.openapi_schema is None:
        schema = get_openapi(title=app.title, version=app.version,
                             description=app.description, routes=app.routes)
        problem_schema = ProblemDetails.model_json_schema(
            ref_template="#/components/schemas/{model}"
        )
        components = schema.setdefault(
            "components", {}).setdefault("schemas", {})
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
