from __future__ import annotations

from collections.abc import AsyncIterator

from src.libs.database import async_session_maker
from src.modules.budgets.infrastructure.sqlalchemy.read_model_repository import (
    SqlAlchemyBudgetReadModelRepository,
)


async def get_budget_read_model_repository() -> AsyncIterator[SqlAlchemyBudgetReadModelRepository]:
    async with async_session_maker() as session:
        repository = SqlAlchemyBudgetReadModelRepository(session)
        yield repository
