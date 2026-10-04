from fastapi import FastAPI
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
)


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


app.include_router(employees_router)
app.include_router(jobs_router)
app.include_router(recommendations_router)

app.include_router(auth_router)
app.include_router(skills_router)
app.include_router(feedback_router)
