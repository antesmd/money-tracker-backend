from __future__ import annotations

from typing import Final

from src.libs.utils import Environ

ADMIN_EMAIL: Final[str] = Environ.get("ADMIN_EMAIL", default_value="")
