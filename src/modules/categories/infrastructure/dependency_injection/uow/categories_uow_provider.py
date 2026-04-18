from __future__ import annotations

from src.modules.categories.application.interfaces.unit_of_work import ICategoriesUnitOfWork
from src.modules.categories.infrastructure.sqlalchemy.unit_of_work import SqlAlchemyCategoriesUnitOfWork
from src.libs.database import async_session_maker


async def get_categories_uow() -> ICategoriesUnitOfWork:
    async with async_session_maker() as session:
        return SqlAlchemyCategoriesUnitOfWork(session)
