from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.budgets.application.interfaces.unit_of_work import IBudgetsUnitOfWork
    from src.modules.budgets.domain.entities import Budget


@dataclass
class GetUserBudgetsQuery:
    user_id: str
    skip: int = 0
    limit: int = 10


async def handle_get_user_budgets(
    command: GetUserBudgetsQuery,
    uow: IBudgetsUnitOfWork,
) -> list[Budget]:
    async with uow:
        return await uow.budgets.get_by_user_id(
            command.user_id,
            command.skip,
            command.limit,
        )
