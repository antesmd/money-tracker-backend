from __future__ import annotations

from src.identity.application.interfaces.unit_of_work import IIdentityUnitOfWork
from src.identity.infrastructure.sqlalchemy.unit_of_work import SqlAlchemyIdentityUnitOfWork
from src.libs.database import async_session_maker


async def get_identity_uow() -> IIdentityUnitOfWork:
    async with async_session_maker() as session:
        return SqlAlchemyIdentityUnitOfWork(session)
