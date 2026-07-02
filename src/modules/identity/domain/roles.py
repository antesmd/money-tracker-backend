from __future__ import annotations

from enum import Enum


class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"
