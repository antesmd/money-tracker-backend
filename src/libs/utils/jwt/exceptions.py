from __future__ import annotations


class BaseJWTError(Exception):
    """
    Base for JWT module exceptions.
    """


class ExpiredTokenError(BaseJWTError):
    def __init__(self) -> None:
        super().__init__("JWT token has expired")


class InvalidTokenSignatureError(BaseJWTError):
    def __init__(self) -> None:
        super().__init__("JWT token signature is invalid")


class JWTBackendError(BaseJWTError):
    def __init__(self) -> None:
        super().__init__("JWT backend module error occurred")
