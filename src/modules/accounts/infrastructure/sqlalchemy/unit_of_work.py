from __future__ import annotations

from typing import TYPE_CHECKING, Self, final

from src.modules.accounts.application.interfaces.unit_of_work import IAccountsUnitOfWork
from src.modules.accounts.infrastructure.sqlalchemy.repository import SqlAlchemyAccountRepository

if TYPE_CHECKING:
    from types import TracebackType

    from sqlalchemy.ext.asyncio import AsyncSession


@final
class SqlAlchemyAccountsUnitOfWork(IAccountsUnitOfWork):
    _accounts: SqlAlchemyAccountRepository

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self._accounts = SqlAlchemyAccountRepository(session)

    @property
    def accounts(self) -> SqlAlchemyAccountRepository:
        return self._accounts

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
