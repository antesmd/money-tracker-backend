from __future__ import annotations

from collections.abc import AsyncIterator

from src.libs.database import async_session_maker
from src.modules.categories.application.interfaces.repositories import (
    ICategoryExpenseRepository,
)
from src.modules.categories.infrastructure.sqlalchemy.category_expense_repository import (
    SqlAlchemyCategoryExpenseRepository,
)


class CategoryExpenseRepositoryProvider:
    @staticmethod
    async def get_category_expense_repository() -> AsyncIterator[ICategoryExpenseRepository]:
        async with async_session_maker() as session:
            repository = SqlAlchemyCategoryExpenseRepository(session)
            yield repository
