from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.modules.budgets.application.exceptions import (
    BudgetNotFoundError,
    UnauthorizedBudgetAccessError,
)

if TYPE_CHECKING:
    from datetime import datetime
    from decimal import Decimal

    from src.modules.budgets.application.interfaces.unit_of_work import IBudgetsUnitOfWork
    from src.modules.budgets.domain.entities import Budget


@dataclass
class UpdateBudgetCommand:
    budget_id: str
    user_id: str
    amount: Decimal | None = None
    period_start: datetime | None = None
    period_end: datetime | None = None


async def handle_update_budget(
    command: UpdateBudgetCommand,
    uow: IBudgetsUnitOfWork,
) -> Budget:
    async with uow:
        budget = await uow.budgets.get_by_id(command.budget_id)
        if not budget:
            raise BudgetNotFoundError(command.budget_id)

        if budget.user_id != command.user_id:
            raise UnauthorizedBudgetAccessError(command.budget_id)

        if command.amount is not None:
            budget.update_amount(command.amount)

        if command.period_start is not None or command.period_end is not None:
            budget.update_period(
                command.period_start or budget.period_start,
                command.period_end or budget.period_end,
            )

        await uow.budgets.update(budget)
        await uow.commit()

    return budget
