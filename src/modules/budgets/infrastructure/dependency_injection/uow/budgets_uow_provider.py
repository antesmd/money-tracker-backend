from __future__ import annotations

from collections.abc import AsyncIterator

from src.libs.database import async_session_maker
from src.modules.budgets.application.interfaces.unit_of_work import IBudgetsUnitOfWork
from src.modules.budgets.infrastructure.sqlalchemy.unit_of_work import SqlAlchemyBudgetsUnitOfWork


async def get_budgets_uow() -> AsyncIterator[IBudgetsUnitOfWork]:
    async with async_session_maker() as session:
        uow = SqlAlchemyBudgetsUnitOfWork(session)
        yield uow
