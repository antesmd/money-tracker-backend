from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.budgets.application.interfaces import IBudgetReadModelRepository
    from src.modules.budgets.domain.entities import BudgetReadModel


@dataclass
class GetUserBudgetsReadModelQuery:
    user_id: str
    skip: int = 0
    limit: int = 100


async def handle_get_user_budgets_read_model(
    query: GetUserBudgetsReadModelQuery,
    repository: IBudgetReadModelRepository,
) -> list[BudgetReadModel]:
    return await repository.get_by_user_id(
        user_id=query.user_id,
        skip=query.skip,
        limit=query.limit,
    )
