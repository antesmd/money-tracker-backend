from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.accounts.domain.entities import AccountReadModel


class IAccountReadModelRepository(ABC):
    @abstractmethod
    async def get_by_id(self, account_id: str) -> AccountReadModel | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_user_id(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 100,
    ) -> list[AccountReadModel]:
        raise NotImplementedError

    @abstractmethod
    async def save(self, read_model: AccountReadModel) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, account_id: str) -> None:
        raise NotImplementedError
