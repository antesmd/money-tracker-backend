from __future__ import annotations

from typing import TYPE_CHECKING, Self, final

from src.modules.identity.application.interfaces.unit_of_work import IIdentityUnitOfWork
from src.modules.identity.infrastructure.sqlalchemy.repository import SqlAlchemyUserRepository

if TYPE_CHECKING:
    from types import TracebackType

    from sqlalchemy.ext.asyncio import AsyncSession


@final
class SqlAlchemyIdentityUnitOfWork(IIdentityUnitOfWork):
    _users: SqlAlchemyUserRepository

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self._users = SqlAlchemyUserRepository(session)

    @property
    def users(self) -> SqlAlchemyUserRepository:
        return self._users

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
