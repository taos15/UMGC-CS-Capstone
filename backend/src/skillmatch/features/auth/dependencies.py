"""Central bearer validation and reusable route-role authorization."""

from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from pydantic import ValidationError

from skillmatch.core.errors import ProblemError
from skillmatch.core.security import decode_token
from skillmatch.features.auth.repository import get_auth_settings
from skillmatch.features.auth.schemas import AuthenticatedUser, Role

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


READ_ROLES: tuple[Role, ...] = ('ADMIN', 'SUPERVISOR', 'VIEWER')
ADMIN_ROLES: tuple[Role, ...] = ('ADMIN',)
SUPERVISOR_ROLES: tuple[Role, ...] = ('ADMIN', 'SUPERVISOR')


def require_roles(*allowed_roles: Role):
    """Authorize a trusted caller before route logic or protected data access."""
    if not allowed_roles or any(role not in READ_ROLES for role in allowed_roles):
        raise ValueError('A protected route must declare valid allowed roles')

    def authorize(
        user: Annotated[AuthenticatedUser, Depends(get_authenticated_user)],
    ) -> AuthenticatedUser:
        if user.role not in allowed_roles:
            raise ProblemError(403, 'FORBIDDEN', 'You do not have permission to perform this action.')
        return user

    authorize.allowed_roles = allowed_roles
    return authorize


def role_access(*allowed_roles: Role) -> dict:
    """One role declaration drives the dependency and its OpenAPI annotation."""
    return {
        'dependencies': [Depends(require_roles(*allowed_roles))],
        'openapi_extra': {'x-allowed-roles': list(allowed_roles)},
    }
