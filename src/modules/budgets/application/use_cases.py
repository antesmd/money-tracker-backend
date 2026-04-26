from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import uuid4

from src.modules.budgets.application.event_handlers import (
    handle_budget_created,
    handle_budget_deleted,
    handle_budget_updated,
)
from src.modules.budgets.application.exceptions import (
    BudgetNotFoundError,
    UnauthorizedBudgetAccessError,
)
from src.modules.budgets.domain.entities import Budget

if TYPE_CHECKING:
    from src.modules.budgets.application.commands import (
        CreateBudgetCommand,
        DeleteBudgetCommand,
        UpdateBudgetCommand,
    )
    from src.modules.budgets.application.interfaces.unit_of_work import IBudgetsUnitOfWork
    from src.modules.budgets.application.queries import (
        GetActiveBudgetsQuery,
        GetUserBudgetsQuery,
    )


async def create_budget(
    command: CreateBudgetCommand,
    uow: IBudgetsUnitOfWork,
) -> Budget:
    async with uow as transaction:
        budget = Budget(
            budget_id=str(uuid4()),
            user_id=command.user_id,
            category_id=command.category_id,
            amount=command.amount,
            period_start=command.period_start,
            period_end=command.period_end,
        )
        await transaction.budgets.add(budget)

    await handle_budget_created(budget)

    return budget


async def update_budget(
    command: UpdateBudgetCommand,
    uow: IBudgetsUnitOfWork,
) -> Budget:
    async with uow as transaction:
        budget = await transaction.budgets.get_by_id(command.budget_id)
        if not budget:
            raise BudgetNotFoundError(command.budget_id)
        if budget.user_id != command.user_id:
            raise UnauthorizedBudgetAccessError(command.user_id)

        if command.amount is not None:
            budget.amount = command.amount
        if command.period_start is not None:
            budget.period_start = command.period_start
        if command.period_end is not None:
            budget.period_end = command.period_end

        await transaction.budgets.update(budget)

    await handle_budget_updated(budget)

    return budget


async def delete_budget(
    command: DeleteBudgetCommand,
    uow: IBudgetsUnitOfWork,
) -> None:
    async with uow as transaction:
        budget = await transaction.budgets.get_by_id(command.budget_id)
        if not budget:
            raise BudgetNotFoundError(command.budget_id)
        if budget.user_id != command.user_id:
            raise UnauthorizedBudgetAccessError(command.user_id)

        budget_id = budget.budget_id
        await transaction.budgets.delete(budget_id)

    await handle_budget_deleted(budget_id)


async def get_user_budgets(
    query: GetUserBudgetsQuery,
    uow: IBudgetsUnitOfWork,
) -> list[Budget]:
    async with uow as transaction:
        return await transaction.budgets.get_by_user_id(
            user_id=query.user_id,
            skip=query.skip,
            limit=query.limit,
        )


async def get_active_budgets(
    query: GetActiveBudgetsQuery,
    uow: IBudgetsUnitOfWork,
) -> list[Budget]:
    async with uow as transaction:
        return await transaction.budgets.get_active_budgets(
            user_id=query.user_id,
            current_date=query.current_date,
        )
