from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.budgets.application.interfaces.unit_of_work import IBudgetsUnitOfWork

from src.modules.budgets.application.exceptions import (
    BudgetNotFoundError,
    UnauthorizedBudgetAccessError,
)


@dataclass
class DeleteBudgetCommand:
    budget_id: str
    user_id: str


async def handle_delete_budget(command: DeleteBudgetCommand, uow: IBudgetsUnitOfWork) -> None:
    async with uow:
        budget = await uow.budgets.get_by_id(command.budget_id)
        if not budget:
            raise BudgetNotFoundError(command.budget_id)

        if budget.user_id != command.user_id:
            raise UnauthorizedBudgetAccessError(command.budget_id)

        await uow.budgets.delete(command.budget_id)
        await uow.commit()
