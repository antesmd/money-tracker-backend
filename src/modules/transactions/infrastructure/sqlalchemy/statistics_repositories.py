from __future__ import annotations

from typing import TYPE_CHECKING, final

from sqlalchemy import select

from src.modules.transactions.application.interfaces import (
    IDashboardStatisticsRepository,
)
from src.modules.transactions.domain.entities import DashboardStatisticsReadModel
from src.modules.transactions.infrastructure.sqlalchemy.orm_models import (
    DashboardStatisticsORM,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@final
class SqlAlchemyDashboardStatisticsRepository(IDashboardStatisticsRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_user_id(self, user_id: str) -> DashboardStatisticsReadModel | None:
        result = await self._session.execute(
            select(DashboardStatisticsORM).where(DashboardStatisticsORM.user_id == user_id),
        )
        orm = result.scalar_one_or_none()
        if not orm:
            return None
        return self._to_domain(orm)

    async def save(self, read_model: DashboardStatisticsReadModel) -> None:
        result = await self._session.execute(
            select(DashboardStatisticsORM).where(
                DashboardStatisticsORM.user_id == read_model.user_id,
            ),
        )
        orm = result.scalar_one_or_none()

        if orm:
            orm.total_income = read_model.total_income
            orm.total_expense = read_model.total_expense
            orm.last_updated = read_model.last_updated
        else:
            orm = DashboardStatisticsORM(
                user_id=read_model.user_id,
                total_income=read_model.total_income,
                total_expense=read_model.total_expense,
                last_updated=read_model.last_updated,
            )
            self._session.add(orm)

    def _to_domain(self, orm: DashboardStatisticsORM) -> DashboardStatisticsReadModel:
        return DashboardStatisticsReadModel(
            user_id=orm.user_id,
            total_income=orm.total_income,
            total_expense=orm.total_expense,
            last_updated=orm.last_updated,
        )
