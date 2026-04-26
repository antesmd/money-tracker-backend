from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.budgets.application.interfaces import IBudgetReadModelRepository
    from src.modules.budgets.domain.entities import BudgetReadModel


@dataclass
class GetBudgetReadModelByIdQuery:
    budget_id: str


async def handle_get_budget_read_model_by_id(
    query: GetBudgetReadModelByIdQuery,
    repository: IBudgetReadModelRepository,
) -> BudgetReadModel | None:
    """Get budget by ID from read model"""
    return await repository.get_by_id(query.budget_id)
