from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime

    from src.modules.budgets.domain.entities import Budget


class IBudgetRepository(ABC):
    @abstractmethod
    async def add(self, budget: Budget) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, budget_id: str) -> Budget | None:
        pass

    @abstractmethod
    async def get_by_user_id(
        self, user_id: str, skip: int = 0, limit: int = 100,
    ) -> list[Budget]:
        pass

    @abstractmethod
    async def get_by_category_id(self, category_id: str) -> list[Budget]:
        pass

    @abstractmethod
    async def get_active_budgets(
        self, user_id: str, current_date: datetime,
    ) -> list[Budget]:
        pass

    @abstractmethod
    async def update(self, budget: Budget) -> None:
        pass

    @abstractmethod
    async def delete(self, budget_id: str) -> None:
        pass
