"""Endpoint stubs protected by bearer authentication and role checks."""

from fastapi import APIRouter, HTTPException

from skillmatch.features.auth.dependencies import ADMIN_ROLES, READ_ROLES, role_access

router = APIRouter()

UNIMPLEMENTED = {501: {'description': 'Endpoint is not implemented yet.',
    'content': {'application/problem+json': {'schema': {'$ref': '#/components/schemas/ProblemDetails'}}}}}


@router.get('/api/v1/skills', tags=['skills'], responses=UNIMPLEMENTED, status_code=501,
            **role_access(*READ_ROLES), description='Allowed roles: ADMIN, SUPERVISOR, VIEWER.')
def list_skills():
    raise HTTPException(status_code=501, detail='Not implemented')


@router.post('/api/v1/skills', tags=['skills'], responses=UNIMPLEMENTED, status_code=501,
             **role_access(*ADMIN_ROLES), description='Allowed roles: ADMIN.')
def create_skill():
    raise HTTPException(status_code=501, detail='Not implemented')
