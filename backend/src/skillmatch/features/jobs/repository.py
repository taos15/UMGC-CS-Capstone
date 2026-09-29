from skillmatch.features.jobs.seed import JOBS
from skillmatch.features.jobs.schemas import Job


def get_job(job_id: str) -> Job | None:
    return next((job for job in JOBS if job.id == job_id), None)
