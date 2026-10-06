"""Local hashed accounts loaded from deployment configuration."""

import os

from uuid import UUID

from pydantic import BaseModel, SecretStr, TypeAdapter, ValidationError, field_validator

from skillmatch.core.errors import ProblemError
from skillmatch.core.security import parse_password_hash
from skillmatch.features.auth.schemas import Role


class LocalUser(BaseModel):
    user_id: UUID
    role: Role
    password_hash: SecretStr

    @field_validator('password_hash')
    @classmethod
    def valid_hash(cls, value: SecretStr) -> SecretStr:
        parse_password_hash(value.get_secret_value())
        return value


class AuthSettings(BaseModel):
    secret: SecretStr
    users: dict[str, LocalUser]


def get_auth_settings() -> AuthSettings:
    try:
        secret = os.environ['SKILLMATCH_JWT_SECRET']
        if len(secret.encode()) < 32:
            raise ValueError('Signing secret is too short')
        users = TypeAdapter(dict[str, LocalUser]).validate_json(os.environ['SKILLMATCH_LOCAL_USERS'])
        if not users or any(not 1 <= len(username) <= 128 for username in users):
            raise ValueError('Invalid local accounts')
        if len({user.user_id for user in users.values()}) != len(users):
            raise ValueError('Duplicate account IDs')
        return AuthSettings(secret=secret, users=users)
    except (KeyError, ValueError, ValidationError):
        raise ProblemError(503, 'AUTH_UNAVAILABLE', 'Authentication is unavailable.') from None
