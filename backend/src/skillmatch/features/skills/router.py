"""Endpoint stubs; role annotations are documentation only."""

from fastapi import APIRouter, HTTPException

router = APIRouter()

READ = {'x-allowed-roles': ['ADMIN', 'SUPERVISOR', 'VIEWER']}
ADMIN = {'x-allowed-roles': ['ADMIN']}
UNIMPLEMENTED = {501: {'description': 'Endpoint is not implemented yet.',
    'content': {'application/problem+json': {'schema': {'$ref': '#/components/schemas/ProblemDetails'}}}}}


@router.get('/api/v1/skills', tags=['skills'], responses=UNIMPLEMENTED, status_code=501,
            openapi_extra=READ, description='Allowed roles: ADMIN, SUPERVISOR, VIEWER.')
def list_skills():
    raise HTTPException(status_code=501, detail='Not implemented')


@router.post('/api/v1/skills', tags=['skills'], responses=UNIMPLEMENTED, status_code=501,
             openapi_extra=ADMIN, description='Allowed roles: ADMIN.')
def create_skill():
    raise HTTPException(status_code=501, detail='Not implemented')
