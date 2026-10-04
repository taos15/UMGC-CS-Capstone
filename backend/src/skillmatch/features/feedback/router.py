"""Endpoint stubs protected by bearer authentication and role checks."""

from fastapi import APIRouter, HTTPException

from skillmatch.features.auth.dependencies import SUPERVISOR_ROLES, role_access

router = APIRouter()

UNIMPLEMENTED = {501: {'description': 'Endpoint is not implemented yet.',
    'content': {'application/problem+json': {'schema': {'$ref': '#/components/schemas/ProblemDetails'}}}}}


@router.post('/api/v1/match-runs/{match_run_id}/feedback', tags=['feedback'], responses=UNIMPLEMENTED, status_code=501,
             **role_access(*SUPERVISOR_ROLES), description='Allowed roles: ADMIN, SUPERVISOR.')
def create_feedback(match_run_id: str):
    raise HTTPException(status_code=501, detail='Not implemented')
