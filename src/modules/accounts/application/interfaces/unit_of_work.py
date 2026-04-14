from __future__ import annotations

from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from types import TracebackType

    from src.modules.accounts.application.interfaces.repositories import IAccountRepository


class IAccountsUnitOfWork(AbstractAsyncContextManager["IAccountsUnitOfWork"], ABC):
    @property
    @abstractmethod
    def accounts(self) -> IAccountRepository:
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
