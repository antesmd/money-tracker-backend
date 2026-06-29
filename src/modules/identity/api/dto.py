from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class CreateUserRequest(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=72)


class AuthenticateUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
