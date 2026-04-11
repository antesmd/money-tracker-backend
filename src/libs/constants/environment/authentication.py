from __future__ import annotations

from typing import Final

from src.libs.utils import Environ

AUTHENTICATION_JWT_PRIVATE_KEY: Final[str] = Environ.get(
    "JWT_AUTHENTICATION_PRIVATE_KEY",
)
AUTHENTICATION_JWT_PUBLIC_KEY: Final[str] = Environ.get(
    "JWT_AUTHENTICATION_PUBLIC_KEY",
)
AUTHENTICATION_JWT_ACCESS_EXPIRATION_SECONDS: Final[int] = int(
    Environ.get(
        "JWT_AUTHENTICATION_EXPIRATION_SECONDS",
        default_value="300",
    ),
)
AUTHENTICATION_JWT_REFRESH_EXPIRATION_SECONDS: Final[int] = int(
    Environ.get(
        "JWT_REFRESH_EXPIRATION_SECONDS",
        default_value="3600",
    ),
)
