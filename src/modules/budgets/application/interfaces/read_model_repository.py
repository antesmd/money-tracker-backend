from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from datetime import datetime

    from src.modules.budgets.domain.entities import BudgetReadModel


class IBudgetReadModelRepository(Protocol):
    async def get_by_id(self, budget_id: str) -> BudgetReadModel | None:
        ...

    async def get_by_user_id(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 100,
    ) -> list[BudgetReadModel]:
        ...

    async def get_by_category_and_date(
        self,
        category_id: str,
        user_id: str,
        date: datetime,
    ) -> BudgetReadModel | None:
        ...

    async def get_active_budgets(
        self,
        user_id: str,
        current_date: datetime,
    ) -> list[BudgetReadModel]:
        ...

    async def save(self, read_model: BudgetReadModel) -> None:
        ...

    async def delete(self, budget_id: str) -> None:
        ...
