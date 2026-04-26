from __future__ import annotations

from collections.abc import AsyncIterator

from src.libs.database import async_session_maker
from src.modules.identity.application.interfaces.unit_of_work import IIdentityUnitOfWork
from src.modules.identity.infrastructure.sqlalchemy.unit_of_work import SqlAlchemyIdentityUnitOfWork


async def get_identity_uow() -> AsyncIterator[IIdentityUnitOfWork]:
    async with async_session_maker() as session:
        uow = SqlAlchemyIdentityUnitOfWork(session)
        yield uow
