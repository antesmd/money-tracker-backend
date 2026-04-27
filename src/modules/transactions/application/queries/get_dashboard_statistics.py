from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.transactions.application.interfaces import (
        IDashboardStatisticsRepository,
    )
    from src.modules.transactions.domain.entities import DashboardStatisticsReadModel


@dataclass
class GetDashboardStatisticsQuery:
    user_id: str


async def handle_get_dashboard_statistics(
    query: GetDashboardStatisticsQuery,
    dashboard_repo: IDashboardStatisticsRepository,
) -> DashboardStatisticsReadModel | None:
    return await dashboard_repo.get_by_user_id(query.user_id)
