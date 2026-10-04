from fastapi import APIRouter, HTTPException

from skillmatch.features.auth.dependencies import ADMIN_ROLES, READ_ROLES, role_access

from skillmatch.features.jobs.repository import get_job
from skillmatch.features.jobs.schemas import Job


router = APIRouter()


@router.get("/api/v1/jobs/{job_id}", response_model=Job,
         **role_access(*READ_ROLES),
         description="Allowed roles: ADMIN, SUPERVISOR, VIEWER.")
def retrieve_job(job_id: str) -> Job:
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

UNIMPLEMENTED = {501: {'description': 'Endpoint is not implemented yet.',
    'content': {'application/problem+json': {'schema': {'$ref': '#/components/schemas/ProblemDetails'}}}}}


@router.get('/api/v1/jobs', tags=['jobs'], responses=UNIMPLEMENTED, status_code=501,
            **role_access(*READ_ROLES), description='Allowed roles: ADMIN, SUPERVISOR, VIEWER.')
def list_jobs():
    raise HTTPException(status_code=501, detail='Not implemented')


@router.post('/api/v1/jobs', tags=['jobs'], responses=UNIMPLEMENTED, status_code=501,
             **role_access(*ADMIN_ROLES), description='Allowed roles: ADMIN.')
def create_job():
    raise HTTPException(status_code=501, detail='Not implemented')


@router.put('/api/v1/jobs/{job_id}', tags=['jobs'], responses=UNIMPLEMENTED, status_code=501,
            **role_access(*ADMIN_ROLES), description='Allowed roles: ADMIN.')
def update_job(job_id: str):
    raise HTTPException(status_code=501, detail='Not implemented')
