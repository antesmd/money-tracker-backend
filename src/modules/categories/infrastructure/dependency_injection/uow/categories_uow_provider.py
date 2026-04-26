from __future__ import annotations

from collections.abc import AsyncIterator

from src.libs.database import async_session_maker
from src.modules.categories.application.interfaces.unit_of_work import ICategoriesUnitOfWork
from src.modules.categories.infrastructure.sqlalchemy.unit_of_work import (
    SqlAlchemyCategoriesUnitOfWork,
)


async def get_categories_uow() -> AsyncIterator[ICategoriesUnitOfWork]:
    async with async_session_maker() as session:
        uow = SqlAlchemyCategoriesUnitOfWork(session)
        yield uow
