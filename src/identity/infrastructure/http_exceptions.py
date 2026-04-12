from __future__ import annotations

from fastapi import HTTPException, status


class InvalidCredentialsHTTPException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials provided.",
        )

