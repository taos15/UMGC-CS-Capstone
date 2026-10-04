"""Bearer validation for workforce routes; role authorization is AUTH-002."""

from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from pydantic import ValidationError

from skillmatch.core.errors import ProblemError
from skillmatch.core.security import decode_token
from skillmatch.features.auth.repository import get_auth_settings
from skillmatch.features.auth.schemas import AuthenticatedUser

bearer = HTTPBearer(auto_error=False)


def get_authenticated_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
) -> AuthenticatedUser:
    if credentials is None:
        raise ProblemError(401, 'AUTH_REQUIRED', 'A valid bearer token is required.')
    settings = get_auth_settings()
    try:
        claims = decode_token(credentials.credentials, settings.secret.get_secret_value())
        user = AuthenticatedUser(user_id=claims['sub'], role=claims['role'])
        if not any(account.user_id == user.user_id and account.role == user.role
                   for account in settings.users.values()):
            raise ValueError('Unknown account')
        return user
    except (InvalidTokenError, ValidationError, ValueError):
        raise ProblemError(401, 'AUTH_REQUIRED', 'A valid bearer token is required.') from None
