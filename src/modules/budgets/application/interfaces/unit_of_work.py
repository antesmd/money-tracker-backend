from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from types import TracebackType

    from src.modules.budgets.application.interfaces.repositories import IBudgetRepository


class IBudgetsUnitOfWork(ABC):
    budgets: IBudgetRepository

    @abstractmethod
    async def __aenter__(self) -> IBudgetsUnitOfWork:
        pass

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass
