from __future__ import annotations

from collections.abc import AsyncIterator

from src.libs.database import async_session_maker
from src.modules.accounts.application.interfaces.unit_of_work import IAccountsUnitOfWork
from src.modules.accounts.infrastructure.sqlalchemy.unit_of_work import SqlAlchemyAccountsUnitOfWork


async def get_accounts_uow() -> AsyncIterator[IAccountsUnitOfWork]:
    async with async_session_maker() as session:
        uow = SqlAlchemyAccountsUnitOfWork(session)
        yield uow
