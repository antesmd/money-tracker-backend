from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.categories.application.interfaces.repositories import (
        ICategoryExpenseRepository,
    )
    from src.modules.categories.domain.entities import CategoryExpenseReadModel


@dataclass
class GetCategoryExpensesQuery:
    user_id: str


async def handle_get_category_expenses(
    query: GetCategoryExpensesQuery,
    category_repo: ICategoryExpenseRepository,
) -> list[CategoryExpenseReadModel]:
    return await category_repo.get_by_user_id(query.user_id)
