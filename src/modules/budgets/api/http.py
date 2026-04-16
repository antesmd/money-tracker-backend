from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from src.libs.authentication.authentication_client import authenticate
from src.libs.utils import DateTimeUtils
from src.modules.budgets.api.dto import BudgetResponse, CreateBudgetRequest, UpdateBudgetRequest
from src.modules.budgets.application.commands import (
    CreateBudgetCommand,
    DeleteBudgetCommand,
    UpdateBudgetCommand,
)
from src.modules.budgets.application.exceptions import (
    BudgetNotFoundError,
    UnauthorizedBudgetAccessError,
)
from src.modules.budgets.application.interfaces.unit_of_work import IBudgetsUnitOfWork
from src.modules.budgets.application.queries import (
    GetActiveBudgetsQuery,
    GetUserBudgetsQuery,
)
from src.modules.budgets.application.use_cases import (
    create_budget,
    delete_budget,
    get_active_budgets,
    get_user_budgets,
    update_budget,
)
from src.modules.budgets.infrastructure.dependency_injection.uow.budgets_uow_provider import (
    get_budgets_uow,
)
from src.modules.budgets.infrastructure.http_exceptions import (
    handle_budget_not_found,
    handle_unauthorized_budget_access,
)

budgets_router = APIRouter()


@budgets_router.post(
    path="/budgets",
    status_code=status.HTTP_201_CREATED,
)
async def create_budget_endpoint(
    request: CreateBudgetRequest,
    user_id: Annotated[str, Depends(authenticate)],
    uow: Annotated[IBudgetsUnitOfWork, Depends(get_budgets_uow)],
) -> BudgetResponse:
    command = CreateBudgetCommand(
        user_id=user_id,
        category_id=request.category_id,
        amount=request.amount,
        period_start=request.period_start,
        period_end=request.period_end,
    )
    budget = await create_budget(command, uow=uow)

    return BudgetResponse(
        budget_id=budget.budget_id,
        user_id=budget.user_id,
        category_id=budget.category_id,
        amount=budget.amount,
        period_start=budget.period_start,
        period_end=budget.period_end,
        is_active=budget.is_active(DateTimeUtils.utc_now()),
        created_at=budget.created_at,
        updated_at=budget.updated_at,
    )


@budgets_router.get(
    path="/budgets",
    status_code=status.HTTP_200_OK,
)
async def get_budgets_endpoint(
    user_id: Annotated[str, Depends(authenticate)],
    uow: Annotated[IBudgetsUnitOfWork, Depends(get_budgets_uow)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> list[BudgetResponse]:
    budgets = await get_user_budgets(
        query=GetUserBudgetsQuery(
            user_id=user_id,
            skip=skip,
            limit=limit,
        ),
        uow=uow,
    )

    current_date = DateTimeUtils.utc_now()
    return [
        BudgetResponse(
            budget_id=b.budget_id,
            user_id=b.user_id,
            category_id=b.category_id,
            amount=b.amount,
            period_start=b.period_start,
            period_end=b.period_end,
            is_active=b.is_active(current_date),
            created_at=b.created_at,
            updated_at=b.updated_at,
        )
        for b in budgets
    ]


@budgets_router.get(
    path="/budgets/active",
    status_code=status.HTTP_200_OK,
)
async def get_active_budgets_endpoint(
    user_id: Annotated[str, Depends(authenticate)],
    uow: Annotated[IBudgetsUnitOfWork, Depends(get_budgets_uow)],
) -> list[BudgetResponse]:
    current_date = DateTimeUtils.utc_now()
    budgets = await get_active_budgets(
        query=GetActiveBudgetsQuery(
            user_id=user_id,
            current_date=current_date,
        ),
        uow=uow,
    )

    return [
        BudgetResponse(
            budget_id=b.budget_id,
            user_id=b.user_id,
            category_id=b.category_id,
            amount=b.amount,
            period_start=b.period_start,
            period_end=b.period_end,
            is_active=True,
            created_at=b.created_at,
            updated_at=b.updated_at,
        )
        for b in budgets
    ]


@budgets_router.patch(
    path="/budgets/{budget_id}",
    status_code=status.HTTP_200_OK,
)
async def update_budget_endpoint(
    budget_id: str,
    request: UpdateBudgetRequest,
    user_id: Annotated[str, Depends(authenticate)],
    uow: Annotated[IBudgetsUnitOfWork, Depends(get_budgets_uow)],
) -> BudgetResponse:
    command = UpdateBudgetCommand(
        budget_id=budget_id,
        user_id=user_id,
        amount=request.amount,
        period_start=request.period_start,
        period_end=request.period_end,
    )
    try:
        budget = await update_budget(command, uow=uow)

        return BudgetResponse(
            budget_id=budget.budget_id,
            user_id=budget.user_id,
            category_id=budget.category_id,
            amount=budget.amount,
            period_start=budget.period_start,
            period_end=budget.period_end,
            is_active=budget.is_active(DateTimeUtils.utc_now()),
            created_at=budget.created_at,
            updated_at=budget.updated_at,
        )
    except BudgetNotFoundError as e:
        raise handle_budget_not_found(e) from e
    except UnauthorizedBudgetAccessError as e:
        raise handle_unauthorized_budget_access(e) from e


@budgets_router.delete(
    path="/budgets/{budget_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_budget_endpoint(
    budget_id: str,
    user_id: Annotated[str, Depends(authenticate)],
    uow: Annotated[IBudgetsUnitOfWork, Depends(get_budgets_uow)],
) -> None:
    command = DeleteBudgetCommand(budget_id=budget_id, user_id=user_id)
    try:
        await delete_budget(command, uow=uow)
    except BudgetNotFoundError as e:
        raise handle_budget_not_found(e) from e
    except UnauthorizedBudgetAccessError as e:
        raise handle_unauthorized_budget_access(e) from e
