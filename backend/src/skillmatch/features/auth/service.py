"""Local credential exchange; unknown users and wrong passwords fail alike."""

from skillmatch.core.errors import ProblemError
from skillmatch.core.security import DUMMY_PASSWORD_HASH, issue_token, verify_password
from skillmatch.features.auth.repository import AuthSettings
from skillmatch.features.auth.schemas import LoginRequest, TokenResponse


def login(credentials: LoginRequest, settings: AuthSettings) -> TokenResponse:
    user = settings.users.get(credentials.username)
    encoded = user.password_hash.get_secret_value() if user else DUMMY_PASSWORD_HASH
    valid = verify_password(credentials.password.get_secret_value(), encoded)
    if not valid or user is None:
        raise ProblemError(401, 'AUTH_INVALID_CREDENTIALS', 'Invalid username or password.')
    return TokenResponse(access_token=issue_token(str(user.user_id), user.role, settings.secret.get_secret_value()))
