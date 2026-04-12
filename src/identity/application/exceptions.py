from __future__ import annotations


class BaseIdentityApplicationError(Exception):
    """Базовое исключение для модуля identity."""


class InvalidCredentialsError(BaseIdentityApplicationError):
    def __init__(self) -> None:
        super().__init__("Invalid credentials")
