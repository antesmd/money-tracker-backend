from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import timedelta


class AbstractTokenService(ABC):
    @abstractmethod
    def create_access_token(
        self,
        payload: str,
        expires_delta: timedelta | None = None,
    ) -> str:
        pass

    @abstractmethod
    def decode_token(self, token: str) -> str | None:
        pass
