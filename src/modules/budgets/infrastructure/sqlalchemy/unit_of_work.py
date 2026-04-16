from __future__ import annotations

from typing import TYPE_CHECKING, Self, final

from src.modules.budgets.application.interfaces.unit_of_work import IBudgetsUnitOfWork
from src.modules.budgets.infrastructure.sqlalchemy.repository import SqlAlchemyBudgetRepository

if TYPE_CHECKING:
    from types import TracebackType

    from sqlalchemy.ext.asyncio import AsyncSession

    from src.modules.budgets.application.interfaces.repositories import IBudgetRepository


@final
class SqlAlchemyBudgetsUnitOfWork(IBudgetsUnitOfWork):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def __aenter__(self) -> Self:
        self.budgets: IBudgetRepository = SqlAlchemyBudgetRepository(self._session)
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
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
