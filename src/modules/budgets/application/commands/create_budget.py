from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.modules.budgets.domain.entities import Budget

if TYPE_CHECKING:
    from datetime import datetime
    from decimal import Decimal

    from src.modules.budgets.application.interfaces.unit_of_work import IBudgetsUnitOfWork


@dataclass
class CreateBudgetCommand:
    user_id: str
    category_id: str
    amount: Decimal
    period_start: datetime
    period_end: datetime


async def handle_create_budget(
    command: CreateBudgetCommand,
    uow: IBudgetsUnitOfWork,
) -> Budget:
    budget = Budget.create(
        user_id=command.user_id,
        category_id=command.category_id,
        amount=command.amount,
        period_start=command.period_start,
        period_end=command.period_end,
    )

    async with uow:
        await uow.budgets.add(budget)
        await uow.commit()

    return budget
