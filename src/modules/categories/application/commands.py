from __future__ import annotations

from typing import NamedTuple

from src.modules.categories.domain.entities import TransactionType


class CreateCategoryCommand(NamedTuple):
    user_id: str
    name: str
    type: TransactionType


class UpdateCategoryCommand(NamedTuple):
    category_id: str
    name: str


class DeleteCategoryCommand(NamedTuple):
    category_id: str


class GetUserCategoriesCommand(NamedTuple):
    user_id: str
