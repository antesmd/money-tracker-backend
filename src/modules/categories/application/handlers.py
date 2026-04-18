from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import uuid4

from src.modules.categories.application.exceptions import CategoryNotFoundError
from src.modules.categories.domain.entities import Category
from src.libs.utils import DateTimeUtils

if TYPE_CHECKING:
    from src.modules.categories.application.commands import (
        CreateCategoryCommand,
        DeleteCategoryCommand,
        GetUserCategoriesCommand,
        UpdateCategoryCommand,
    )
    from src.modules.categories.application.interfaces.unit_of_work import ICategoriesUnitOfWork


async def handle_create_category(
    command: CreateCategoryCommand,
    unit_of_work: ICategoriesUnitOfWork,
) -> Category:
    category = Category(
        category_id=str(uuid4()),
        user_id=command.user_id,
        name=command.name,
        type=command.type,
    )
    unit_of_work.categories.add(category)
    await unit_of_work.commit()
    return category


async def handle_update_category(
    command: UpdateCategoryCommand,
    unit_of_work: ICategoriesUnitOfWork,
) -> Category:
    category = await unit_of_work.categories.get_by_id(command.category_id)
    if not category:
        raise CategoryNotFoundError

    category.name = command.name
    category.updated_at = DateTimeUtils.utc_now()
    await unit_of_work.categories.update(category)
    await unit_of_work.commit()
    return category


async def handle_delete_category(
    command: DeleteCategoryCommand,
    unit_of_work: ICategoriesUnitOfWork,
) -> None:
    category = await unit_of_work.categories.get_by_id(command.category_id)
    if not category:
        raise CategoryNotFoundError

    await unit_of_work.categories.delete(command.category_id)
    await unit_of_work.commit()


async def handle_get_user_categories(
    command: GetUserCategoriesCommand,
    unit_of_work: ICategoriesUnitOfWork,
) -> list[Category]:
    return await unit_of_work.categories.get_by_user_id(command.user_id)
