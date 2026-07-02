from __future__ import annotations

from typing import NamedTuple


class CreateCategoryCommand(NamedTuple):
    user_id: str
    name: str


class UpdateCategoryCommand(NamedTuple):
    category_id: str
    user_id: str
    name: str


class DeleteCategoryCommand(NamedTuple):
    category_id: str
    user_id: str


class GetUserCategoriesCommand(NamedTuple):
    user_id: str
