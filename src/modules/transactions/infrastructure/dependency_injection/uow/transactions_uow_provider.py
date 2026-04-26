from __future__ import annotations

from collections.abc import AsyncIterator

from src.libs.database import async_session_maker
from src.modules.transactions.application.interfaces.unit_of_work import ITransactionsUnitOfWork
from src.modules.transactions.infrastructure.sqlalchemy.unit_of_work import (
    SqlAlchemyTransactionsUnitOfWork,
)


async def get_transactions_uow() -> AsyncIterator[ITransactionsUnitOfWork]:
    async with async_session_maker() as session:
        uow = SqlAlchemyTransactionsUnitOfWork(session)
        yield uow
