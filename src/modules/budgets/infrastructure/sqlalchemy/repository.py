from __future__ import annotations

from typing import TYPE_CHECKING, final

from sqlalchemy import select

from src.modules.budgets.application.interfaces.repositories import IBudgetRepository
from src.modules.budgets.domain.entities import Budget
from src.modules.budgets.infrastructure.sqlalchemy.orm_models import BudgetORM

if TYPE_CHECKING:
    from datetime import datetime

    from sqlalchemy.ext.asyncio import AsyncSession


@final
class SqlAlchemyBudgetRepository(IBudgetRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, budget: Budget) -> None:
        budget_orm = BudgetORM(
            budget_id=budget.budget_id,
            user_id=budget.user_id,
            category_id=budget.category_id,
            amount=budget.amount,
            period_start=budget.period_start,
            period_end=budget.period_end,
            created_at=budget.created_at,
            updated_at=budget.updated_at,
        )
        self._session.add(budget_orm)

    async def get_by_id(self, budget_id: str) -> Budget | None:
        result = await self._session.execute(
            select(BudgetORM).where(BudgetORM.budget_id == budget_id),
        )
        budget_orm = result.scalar_one_or_none()
        if not budget_orm:
            return None

        return Budget(
            budget_id=budget_orm.budget_id,
            user_id=budget_orm.user_id,
            category_id=budget_orm.category_id,
            amount=budget_orm.amount,
            period_start=budget_orm.period_start,
            period_end=budget_orm.period_end,
            created_at=budget_orm.created_at,
            updated_at=budget_orm.updated_at,
        )

    async def get_by_user_id(self, user_id: str, skip: int = 0, limit: int = 100) -> list[Budget]:
        result = await self._session.execute(
            select(BudgetORM).where(BudgetORM.user_id == user_id).offset(skip).limit(limit),
        )
        budget_orms = result.scalars().all()

        return [
            Budget(
                budget_id=b.budget_id,
                user_id=b.user_id,
                category_id=b.category_id,
                amount=b.amount,
                period_start=b.period_start,
                period_end=b.period_end,
                created_at=b.created_at,
                updated_at=b.updated_at,
            )
            for b in budget_orms
        ]

    async def get_by_category_id(self, category_id: str) -> list[Budget]:
        result = await self._session.execute(
            select(BudgetORM).where(BudgetORM.category_id == category_id),
        )
        budget_orms = result.scalars().all()

        return [
            Budget(
                budget_id=b.budget_id,
                user_id=b.user_id,
                category_id=b.category_id,
                amount=b.amount,
                period_start=b.period_start,
                period_end=b.period_end,
                created_at=b.created_at,
                updated_at=b.updated_at,
            )
            for b in budget_orms
        ]

    async def get_active_budgets(
        self,
        user_id: str,
        current_date: datetime,
    ) -> list[Budget]:
        result = await self._session.execute(
            select(BudgetORM)
            .where(BudgetORM.user_id == user_id)
            .where(BudgetORM.period_start <= current_date)
            .where(BudgetORM.period_end >= current_date),
        )
        budget_orms = result.scalars().all()

        return [
            Budget(
                budget_id=b.budget_id,
                user_id=b.user_id,
                category_id=b.category_id,
                amount=b.amount,
                period_start=b.period_start,
                period_end=b.period_end,
                created_at=b.created_at,
                updated_at=b.updated_at,
            )
            for b in budget_orms
        ]

    async def update(self, budget: Budget) -> None:
        result = await self._session.execute(
            select(BudgetORM).where(BudgetORM.budget_id == budget.budget_id),
        )
        budget_orm = result.scalar_one_or_none()
        if budget_orm:
            budget_orm.amount = budget.amount
            budget_orm.period_start = budget.period_start
            budget_orm.period_end = budget.period_end
            budget_orm.updated_at = budget.updated_at

    async def delete(self, budget_id: str) -> None:
        result = await self._session.execute(
            select(BudgetORM).where(BudgetORM.budget_id == budget_id),
        )
        budget_orm = result.scalar_one_or_none()
        if budget_orm:
            await self._session.delete(budget_orm)
