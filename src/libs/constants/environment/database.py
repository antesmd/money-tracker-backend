from __future__ import annotations

from typing import Final

from src.libs.utils import Environ

DB_USER: Final[str] = Environ.get("DB_USER")
DB_PASSWORD: Final[str] = Environ.get("DB_PASSWORD")
DB_HOST: Final[str] = Environ.get("DB_HOST")
DB_PORT: Final[str] = Environ.get("DB_PORT")
DB_NAME: Final[str] = Environ.get("DB_NAME")
DB_ENGINE: Final[str] = Environ.get("DB_ENGINE")
