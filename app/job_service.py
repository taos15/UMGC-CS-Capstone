from app.data import JOBS
from app.schemas import Job


def get_job(job_id: str) -> Job | None:
    return next((job for job in JOBS if job.id == job_id), None)
