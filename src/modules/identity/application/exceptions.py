from __future__ import annotations


class BaseIdentityApplicationError(Exception):
    pass


class InvalidCredentialsError(BaseIdentityApplicationError):
    def __init__(self) -> None:
        super().__init__("Invalid credentials")
