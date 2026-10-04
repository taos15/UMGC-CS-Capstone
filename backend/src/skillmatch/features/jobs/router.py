from fastapi import APIRouter, HTTPException

from skillmatch.features.jobs.repository import get_job
from skillmatch.features.jobs.schemas import Job


router = APIRouter()


@router.get("/api/v1/jobs/{job_id}", response_model=Job)
def retrieve_job(job_id: str) -> Job:
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
