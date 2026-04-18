from __future__ import annotations

from typing import TYPE_CHECKING

from src.modules.categories.application import handlers

if TYPE_CHECKING:
    from src.modules.categories.application.commands import (
        CreateCategoryCommand,
        DeleteCategoryCommand,
        GetUserCategoriesCommand,
        UpdateCategoryCommand,
    )
    from src.modules.categories.application.interfaces.unit_of_work import ICategoriesUnitOfWork
    from src.modules.categories.domain.entities import Category


async def create_category_use_case(
    command: CreateCategoryCommand,
    unit_of_work: ICategoriesUnitOfWork,
) -> Category:
    return await handlers.handle_create_category(command, unit_of_work)


async def update_category_use_case(
    command: UpdateCategoryCommand,
    unit_of_work: ICategoriesUnitOfWork,
) -> Category:
    return await handlers.handle_update_category(command, unit_of_work)


async def delete_category_use_case(
    command: DeleteCategoryCommand,
    unit_of_work: ICategoriesUnitOfWork,
) -> None:
    await handlers.handle_delete_category(command, unit_of_work)


async def get_user_categories_use_case(
    command: GetUserCategoriesCommand,
    unit_of_work: ICategoriesUnitOfWork,
) -> list[Category]:
    return await handlers.handle_get_user_categories(command, unit_of_work)
