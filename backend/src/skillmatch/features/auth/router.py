"""Public local-login endpoint."""

from typing import Annotated

from fastapi import APIRouter, Depends, Response

from skillmatch.features.auth.repository import AuthSettings, get_auth_settings
from skillmatch.features.auth.schemas import LoginRequest, TokenResponse
from skillmatch.features.auth.service import login as exchange_credentials

router = APIRouter()

PROBLEM_RESPONSES = {
    status: {'description': description, 'content': {'application/problem+json': {
        'schema': {'$ref': '#/components/schemas/ProblemDetails'}}}}
    for status, description in [(401, 'Invalid credentials'), (422, 'Invalid request'), (503, 'Authentication unavailable')]
}


@router.post('/api/v1/auth/login', tags=['auth'], response_model=TokenResponse,
             responses=PROBLEM_RESPONSES, openapi_extra={'x-allowed-roles': [], 'security': []},
             description='Public. Exchange local credentials for a 15-minute bearer token.')
def login(credentials: LoginRequest, response: Response,
          settings: Annotated[AuthSettings, Depends(get_auth_settings)]) -> TokenResponse:
    token = exchange_credentials(credentials, settings)
    response.headers['Cache-Control'] = 'no-store'
    response.headers['Pragma'] = 'no-cache'
    return token
