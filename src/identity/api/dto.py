from __future__ import annotations

from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    email: str
    username: str
    password: str


class AuthenticateUserRequest(BaseModel):
    email: str
    password: str
