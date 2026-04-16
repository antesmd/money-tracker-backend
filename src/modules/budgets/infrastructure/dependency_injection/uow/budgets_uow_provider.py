from __future__ import annotations

from src.modules.budgets.application.interfaces.unit_of_work import IBudgetsUnitOfWork
from src.modules.budgets.infrastructure.sqlalchemy.unit_of_work import SqlAlchemyBudgetsUnitOfWork
from src.libs.database import async_session_maker


async def get_budgets_uow() -> IBudgetsUnitOfWork:
    async with async_session_maker() as session:
        return SqlAlchemyBudgetsUnitOfWork(session)
