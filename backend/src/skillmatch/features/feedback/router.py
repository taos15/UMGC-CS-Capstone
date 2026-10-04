"""Endpoint stubs; role annotations are documentation only."""

from fastapi import APIRouter, HTTPException

router = APIRouter()

SUPERVISE = {'x-allowed-roles': ['ADMIN', 'SUPERVISOR']}
UNIMPLEMENTED = {501: {'description': 'Endpoint is not implemented yet.',
    'content': {'application/problem+json': {'schema': {'$ref': '#/components/schemas/ProblemDetails'}}}}}


@router.post('/api/v1/match-runs/{match_run_id}/feedback', tags=['feedback'], responses=UNIMPLEMENTED, status_code=501,
             openapi_extra=SUPERVISE, description='Allowed roles: ADMIN, SUPERVISOR.')
def create_feedback(match_run_id: str):
    raise HTTPException(status_code=501, detail='Not implemented')
