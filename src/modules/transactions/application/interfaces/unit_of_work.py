from __future__ import annotations

from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from types import TracebackType

    from src.modules.transactions.application.interfaces.repositories import ITransactionRepository


class ITransactionsUnitOfWork(AbstractAsyncContextManager["ITransactionsUnitOfWork"], ABC):
    @property
    @abstractmethod
    def transactions(self) -> ITransactionRepository:
        ...

    @abstractmethod
    async def __aenter__(self) -> Self:
        ...

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        ...

    @abstractmethod
    async def commit(self) -> None:
        ...

    @abstractmethod
    async def rollback(self) -> None:
        ...
