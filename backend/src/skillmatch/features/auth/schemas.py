"""Approved local-login request and token response."""

from typing import Annotated, Literal

from uuid import UUID

from pydantic import BaseModel, Field, SecretStr

Role = Literal['ADMIN', 'SUPERVISOR', 'VIEWER']


class LoginRequest(BaseModel):
    username: Annotated[str, Field(min_length=1, max_length=128)]
    password: Annotated[SecretStr, Field(min_length=1, max_length=1024)]


class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal['bearer'] = 'bearer'
    expires_in: int = 900


class AuthenticatedUser(BaseModel):
    user_id: UUID
    role: Role
