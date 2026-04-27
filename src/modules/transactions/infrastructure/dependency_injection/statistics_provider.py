from __future__ import annotations

from collections.abc import AsyncIterator

from src.libs.database import async_session_maker
from src.modules.transactions.application.interfaces import (
    IDashboardStatisticsRepository,
)
from src.modules.transactions.infrastructure.sqlalchemy.statistics_repositories import (
    SqlAlchemyDashboardStatisticsRepository,
)


async def get_dashboard_statistics_repository() -> AsyncIterator[IDashboardStatisticsRepository]:
    async with async_session_maker() as session:
        repository = SqlAlchemyDashboardStatisticsRepository(session)
        yield repository
