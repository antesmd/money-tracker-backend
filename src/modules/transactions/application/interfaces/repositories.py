from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime

    from src.modules.transactions.domain.entities import Transaction


class ITransactionRepository(ABC):
    @abstractmethod
    def add(self, transaction: Transaction) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, transaction_id: str) -> Transaction | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_user_id(
        self,
        user_id: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[Transaction]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_account_id(
        self,
        account_id: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[Transaction]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_date_range(
        self,
        user_id: str,
        start_date: datetime,
        end_date: datetime,
    ) -> list[Transaction]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, transaction: Transaction) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, transaction_id: str) -> None:
        raise NotImplementedError
