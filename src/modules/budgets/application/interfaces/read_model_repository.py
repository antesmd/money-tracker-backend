from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from datetime import datetime

    from src.modules.budgets.domain.entities import BudgetReadModel


class IBudgetReadModelRepository(Protocol):
    """Repository interface for read model"""

    async def get_by_id(self, budget_id: str) -> BudgetReadModel | None:
        """Get read model by budget ID"""
        ...

    async def get_by_user_id(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 100,
    ) -> list[BudgetReadModel]:
        """Get user's read models"""
        ...

    async def get_by_category_and_date(
        self,
        category_id: str,
        user_id: str,
        date: datetime,
    ) -> BudgetReadModel | None:
        """Get active budget by category and date"""
        ...

    async def get_active_budgets(
        self,
        user_id: str,
        current_date: datetime,
    ) -> list[BudgetReadModel]:
        """Get all active read models"""
        ...

    async def save(self, read_model: BudgetReadModel) -> None:
        """Save or update read model"""
        ...

    async def delete(self, budget_id: str) -> None:
        """Delete read model"""
        ...
