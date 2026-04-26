from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime

    from src.modules.budgets.application.interfaces import IBudgetReadModelRepository
    from src.modules.budgets.domain.entities import BudgetReadModel

@dataclass
class GetActiveBudgetsReadModelQuery:
    user_id: str
    current_date: datetime


async def handle_get_active_budgets_read_model(
    query: GetActiveBudgetsReadModelQuery,
    repository: IBudgetReadModelRepository,
) -> list[BudgetReadModel]:
    return await repository.get_active_budgets(
        user_id=query.user_id,
        current_date=query.current_date,
    )
