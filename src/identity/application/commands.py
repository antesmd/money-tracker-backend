from __future__ import annotations

from typing import NamedTuple


class CreateUserCommand(NamedTuple):
    username: str
    email: str
    password: str


class AuthenticateUserCommand(NamedTuple):
    email: str
    password: str


class RefreshTokenCommand(NamedTuple):
    refresh_token: str
