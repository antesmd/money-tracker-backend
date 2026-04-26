from __future__ import annotations

from typing import TYPE_CHECKING, final

from sqlalchemy import and_, select

from src.modules.budgets.domain.entities import BudgetReadModel
from src.modules.budgets.infrastructure.sqlalchemy.orm_models import BudgetReadModelORM

if TYPE_CHECKING:
    from datetime import datetime

    from sqlalchemy.ext.asyncio import AsyncSession


@final
class SqlAlchemyBudgetReadModelRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, budget_id: str) -> BudgetReadModel | None:
        result = await self._session.execute(
            select(BudgetReadModelORM).where(BudgetReadModelORM.budget_id == budget_id),
        )
        orm = result.scalar_one_or_none()
        if not orm:
            return None

        return self._to_domain(orm)

    async def get_by_user_id(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 100,
    ) -> list[BudgetReadModel]:
        result = await self._session.execute(
            select(BudgetReadModelORM)
            .where(BudgetReadModelORM.user_id == user_id)
            .offset(skip)
            .limit(limit),
        )
        orms = result.scalars().all()
        return [self._to_domain(orm) for orm in orms]

    async def get_by_category_and_date(
        self,
        category_id: str,
        user_id: str,
        date: datetime,
    ) -> BudgetReadModel | None:
        result = await self._session.execute(
            select(BudgetReadModelORM).where(
                and_(
                    BudgetReadModelORM.category_id == category_id,
                    BudgetReadModelORM.user_id == user_id,
                    BudgetReadModelORM.period_start <= date,
                    BudgetReadModelORM.period_end >= date,
                ),
            ),
        )
        orm = result.scalar_one_or_none()
        if not orm:
            return None

        return self._to_domain(orm)

    async def get_active_budgets(
        self,
        user_id: str,
        current_date: datetime,
    ) -> list[BudgetReadModel]:
        result = await self._session.execute(
            select(BudgetReadModelORM)
            .where(BudgetReadModelORM.user_id == user_id)
            .where(BudgetReadModelORM.period_start <= current_date)
            .where(BudgetReadModelORM.period_end >= current_date),
        )
        orms = result.scalars().all()
        return [self._to_domain(orm) for orm in orms]

    async def save(self, read_model: BudgetReadModel) -> None:
        result = await self._session.execute(
            select(BudgetReadModelORM).where(
                BudgetReadModelORM.budget_id == read_model.budget_id,
            ),
        )
        orm = result.scalar_one_or_none()

        if orm:
            orm.amount = read_model.amount
            orm.spent = read_model.spent
            orm.remaining = read_model.remaining
            orm.transaction_count = read_model.transaction_count
            orm.last_updated = read_model.last_updated
        else:
            orm = BudgetReadModelORM(
                budget_id=read_model.budget_id,
                user_id=read_model.user_id,
                category_id=read_model.category_id,
                amount=read_model.amount,
                spent=read_model.spent,
                remaining=read_model.remaining,
                transaction_count=read_model.transaction_count,
                period_start=read_model.period_start,
                period_end=read_model.period_end,
                last_updated=read_model.last_updated,
            )
            self._session.add(orm)

    async def delete(self, budget_id: str) -> None:
        result = await self._session.execute(
            select(BudgetReadModelORM).where(
                BudgetReadModelORM.budget_id == budget_id,
            ),
        )
        orm = result.scalar_one_or_none()
        if orm:
            await self._session.delete(orm)

    def _to_domain(self, orm: BudgetReadModelORM) -> BudgetReadModel:
        return BudgetReadModel(
            budget_id=orm.budget_id,
            user_id=orm.user_id,
            category_id=orm.category_id,
            amount=orm.amount,
            spent=orm.spent,
            remaining=orm.remaining,
            transaction_count=orm.transaction_count,
            period_start=orm.period_start,
            period_end=orm.period_end,
            last_updated=orm.last_updated,
        )
