from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status

from src.libs.authentication.authentication_client import authenticate
from src.modules.categories.application.commands import (
    CreateCategoryCommand,
    DeleteCategoryCommand,
    GetUserCategoriesCommand,
    UpdateCategoryCommand,
)
from src.modules.categories.application.exceptions import CategoryNotFoundError
from src.modules.categories.application.interfaces.repositories import (
    ICategoryExpenseRepository,
)
from src.modules.categories.application.interfaces.unit_of_work import ICategoriesUnitOfWork
from src.modules.categories.application.queries import (
    GetCategoryExpensesQuery,
    handle_get_category_expenses,
)
from src.modules.categories.application.use_cases import (
    create_category_use_case,
    delete_category_use_case,
    get_user_categories_use_case,
    update_category_use_case,
)
from src.modules.categories.infrastructure.dependency_injection.category_expense_provider import (
    CategoryExpenseRepositoryProvider,
)
from src.modules.categories.infrastructure.dependency_injection.uow.categories_uow_provider import (
    get_categories_uow,
)

from .dto import (
    CategoryExpenseResponse,
    CategoryResponse,
    CreateCategoryRequest,
    UpdateCategoryRequest,
)

router = APIRouter()


@router.post(path="/categories", status_code=status.HTTP_201_CREATED)
async def create_category(
    user_id: Annotated[str, Depends(authenticate)],
    body: Annotated[CreateCategoryRequest, Body()],
    unit_of_work: Annotated[ICategoriesUnitOfWork, Depends(get_categories_uow)],
) -> CategoryResponse:
    command = CreateCategoryCommand(
        user_id=user_id,
        name=body.name,
    )
    category = await create_category_use_case(command, unit_of_work=unit_of_work)
    return CategoryResponse(
        category_id=category.category_id,
        user_id=category.user_id,
        name=category.name,
        created_at=category.created_at,
        updated_at=category.updated_at,
    )


@router.get(path="/categories")
async def get_user_categories(
    user_id: Annotated[str, Depends(authenticate)],
    unit_of_work: Annotated[ICategoriesUnitOfWork, Depends(get_categories_uow)],
) -> list[CategoryResponse]:
    command = GetUserCategoriesCommand(user_id=user_id)
    categories = await get_user_categories_use_case(command, unit_of_work=unit_of_work)
    return [
        CategoryResponse(
            category_id=category.category_id,
            user_id=category.user_id,
            name=category.name,
            created_at=category.created_at,
            updated_at=category.updated_at,
        )
        for category in categories
    ]


@router.get(path="/categories/statistics/expenses", response_model=list[CategoryExpenseResponse])
async def get_category_expenses(
    user_id: Annotated[str, Depends(authenticate)],
    category_repo: Annotated[
        ICategoryExpenseRepository,
        Depends(CategoryExpenseRepositoryProvider.get_category_expense_repository),
    ],
) -> list[CategoryExpenseResponse]:
    query = GetCategoryExpensesQuery(user_id=user_id)
    expenses = await handle_get_category_expenses(query, category_repo)

    return [
        CategoryExpenseResponse(
            category_id=expense.category_id,
            category_name=expense.category_name,
            amount=expense.total_amount,
            transaction_count=expense.transaction_count,
            last_updated=expense.last_updated,
        )
        for expense in expenses
    ]


@router.patch(path="/categories/{category_id}")
async def update_category(
    category_id: str,
    user_id: Annotated[str, Depends(authenticate)],
    body: Annotated[UpdateCategoryRequest, Body()],
    unit_of_work: Annotated[ICategoriesUnitOfWork, Depends(get_categories_uow)],
) -> CategoryResponse:
    command = UpdateCategoryCommand(
        category_id=category_id,
        user_id=user_id,
        name=body.name,
    )
    try:
        category = await update_category_use_case(command, unit_of_work=unit_of_work)
    except CategoryNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        ) from exc

    return CategoryResponse(
        category_id=category.category_id,
        user_id=category.user_id,
        name=category.name,
        created_at=category.created_at,
        updated_at=category.updated_at,
    )


@router.delete(path="/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: str,
    user_id: Annotated[str, Depends(authenticate)],
    unit_of_work: Annotated[ICategoriesUnitOfWork, Depends(get_categories_uow)],
) -> None:
    command = DeleteCategoryCommand(category_id=category_id, user_id=user_id)
    try:
        await delete_category_use_case(command, unit_of_work=unit_of_work)
    except CategoryNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        ) from exc
