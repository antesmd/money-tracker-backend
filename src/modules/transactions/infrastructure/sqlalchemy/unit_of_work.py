from __future__ import annotations

from typing import TYPE_CHECKING, Self, final

from src.modules.transactions.application.interfaces.unit_of_work import ITransactionsUnitOfWork
from src.modules.transactions.infrastructure.sqlalchemy.repository import (
    SqlAlchemyTransactionRepository,
)

if TYPE_CHECKING:
    from types import TracebackType

    from sqlalchemy.ext.asyncio import AsyncSession


@final
class SqlAlchemyTransactionsUnitOfWork(ITransactionsUnitOfWork):
    _transactions: SqlAlchemyTransactionRepository

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self._transactions = SqlAlchemyTransactionRepository(session)

    @property
    def transactions(self) -> SqlAlchemyTransactionRepository:
        return self._transactions

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
