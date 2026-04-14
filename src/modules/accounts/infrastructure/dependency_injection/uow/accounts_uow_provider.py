from __future__ import annotations

from src.modules.accounts.application.interfaces.unit_of_work import IAccountsUnitOfWork
from src.modules.accounts.infrastructure.sqlalchemy.unit_of_work import SqlAlchemyAccountsUnitOfWork
from src.libs.database import async_session_maker


async def get_accounts_uow() -> IAccountsUnitOfWork:
    async with async_session_maker() as session:
        return SqlAlchemyAccountsUnitOfWork(session)
