from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.accounts.domain.entities import Account


class IAccountRepository(ABC):
    @abstractmethod
    def add(self, account: Account) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, account_id: str) -> Account | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_user_id(self, user_id: str) -> list[Account]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, account: Account) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, account_id: str) -> None:
        raise NotImplementedError
