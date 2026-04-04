from __future__ import annotations

from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Environ:
    @staticmethod
    def get(name: str, *, default_value: str | None = None) -> str:
        value = getenv(name)
        if value is not None:
            return value
        if default_value is not None:
            return default_value

        msg = f"Environment variable '{name}' is not set."
        raise ValueError(msg)
