from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import TYPE_CHECKING

from src.modules.budgets.application.exceptions import BudgetNotFoundError

if TYPE_CHECKING:
    from src.modules.budgets.application.interfaces.repositories import IBudgetRepository


@dataclass
class UpdateBudgetStatisticsCommand:
    budget_id: str
    total_spent: str
    transaction_count: int


class UpdateBudgetStatisticsCommandHandler:
    def __init__(self, budget_repository: IBudgetRepository) -> None:
        self.budget_repository = budget_repository

    async def handle(self, command: UpdateBudgetStatisticsCommand) -> None:
        budget = await self.budget_repository.get_by_id(command.budget_id)
        if not budget:
            raise BudgetNotFoundError(command.budget_id)

        budget.total_spent = Decimal(command.total_spent)
        budget.transaction_count = command.transaction_count
        await self.budget_repository.update(budget)
