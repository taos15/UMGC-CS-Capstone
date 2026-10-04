"""Section 5 endpoint placeholders with documentation-only role annotations.

These annotations do not enforce authorization. Stubs return 501 until their
feature implementation and authentication dependencies are available.
"""

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix='/api/v1')
READ = {'x-allowed-roles': ['ADMIN', 'SUPERVISOR', 'VIEWER']}
ADMIN = {'x-allowed-roles': ['ADMIN']}
SUPERVISE = {'x-allowed-roles': ['ADMIN', 'SUPERVISOR']}
UNIMPLEMENTED = {501: {'description': 'Endpoint is not implemented yet.'}}


@router.post('/auth/login', tags=['auth'], responses=UNIMPLEMENTED, status_code=501,
             openapi_extra={'x-allowed-roles': [], 'security': []}, description='Public.')
def login():
    raise HTTPException(status_code=501, detail='Not implemented')


@router.get('/skills', tags=['skills'], responses=UNIMPLEMENTED, status_code=501,
            openapi_extra=READ, description='Allowed roles: ADMIN, SUPERVISOR, VIEWER.')
def list_skills():
    raise HTTPException(status_code=501, detail='Not implemented')


@router.post('/skills', tags=['skills'], responses=UNIMPLEMENTED, status_code=501,
             openapi_extra=ADMIN, description='Allowed roles: ADMIN.')
def create_skill():
    raise HTTPException(status_code=501, detail='Not implemented')


@router.post('/employees', tags=['employees'], responses=UNIMPLEMENTED, status_code=501,
             openapi_extra=ADMIN, description='Allowed roles: ADMIN.')
def create_employee():
    raise HTTPException(status_code=501, detail='Not implemented')


@router.put('/employees/{employee_id}', tags=['employees'], responses=UNIMPLEMENTED, status_code=501,
            openapi_extra=ADMIN, description='Allowed roles: ADMIN.')
def update_employee(employee_id: str):
    raise HTTPException(status_code=501, detail='Not implemented')


@router.get('/jobs', tags=['jobs'], responses=UNIMPLEMENTED, status_code=501,
            openapi_extra=READ, description='Allowed roles: ADMIN, SUPERVISOR, VIEWER.')
def list_jobs():
    raise HTTPException(status_code=501, detail='Not implemented')


@router.post('/jobs', tags=['jobs'], responses=UNIMPLEMENTED, status_code=501,
             openapi_extra=ADMIN, description='Allowed roles: ADMIN.')
def create_job():
    raise HTTPException(status_code=501, detail='Not implemented')


@router.put('/jobs/{job_id}', tags=['jobs'], responses=UNIMPLEMENTED, status_code=501,
            openapi_extra=ADMIN, description='Allowed roles: ADMIN.')
def update_job(job_id: str):
    raise HTTPException(status_code=501, detail='Not implemented')


@router.get('/match-runs/{match_run_id}', tags=['match-runs'], responses=UNIMPLEMENTED, status_code=501,
            openapi_extra=READ,
            description='Allowed roles: ADMIN, SUPERVISOR, VIEWER, within authorized run scope.')
def retrieve_match_run(match_run_id: str):
    raise HTTPException(status_code=501, detail='Not implemented')


@router.post('/match-runs/{match_run_id}/feedback', tags=['feedback'], responses=UNIMPLEMENTED, status_code=501,
             openapi_extra=SUPERVISE, description='Allowed roles: ADMIN, SUPERVISOR.')
def create_feedback(match_run_id: str):
    raise HTTPException(status_code=501, detail='Not implemented')
