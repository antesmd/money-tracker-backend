from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime

    from src.modules.budgets.application.interfaces.unit_of_work import IBudgetsUnitOfWork
    from src.modules.budgets.domain.entities import Budget


@dataclass
class GetActiveBudgetsQuery:
    user_id: str
    current_date: datetime


async def handle_get_active_budgets(
    command: GetActiveBudgetsQuery,
    uow: IBudgetsUnitOfWork,
) -> list[Budget]:
    async with uow:
        return await uow.budgets.get_active_budgets(
            command.user_id,
            command.current_date,
        )
