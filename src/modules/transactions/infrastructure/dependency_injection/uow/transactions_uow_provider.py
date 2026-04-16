from __future__ import annotations

from src.libs.database import async_session_maker
from src.modules.transactions.application.interfaces.unit_of_work import ITransactionsUnitOfWork
from src.modules.transactions.infrastructure.sqlalchemy.unit_of_work import SqlAlchemyTransactionsUnitOfWork


async def get_transactions_uow() -> ITransactionsUnitOfWork:
    async with async_session_maker() as session:
        return SqlAlchemyTransactionsUnitOfWork(session)
