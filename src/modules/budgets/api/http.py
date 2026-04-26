from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.libs.authentication.authentication_client import authenticate
from src.libs.utils import DateTimeUtils
from src.modules.budgets.api.dto import (
    BudgetReadModelResponse,
    BudgetResponse,
    CreateBudgetRequest,
    UpdateBudgetRequest,
)
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
    GetActiveBudgetsReadModelQuery,
    GetBudgetReadModelByIdQuery,
    GetUserBudgetsQuery,
    GetUserBudgetsReadModelQuery,
    handle_get_active_budgets_read_model,
    handle_get_budget_read_model_by_id,
    handle_get_user_budgets_read_model,
)
from src.modules.budgets.application.use_cases import (
    create_budget,
    delete_budget,
    get_active_budgets,
    get_user_budgets,
    update_budget,
)
from src.modules.budgets.infrastructure.dependency_injection.read_model_repository_provider import (
    get_budget_read_model_repository,
)
from src.modules.budgets.infrastructure.dependency_injection.uow.budgets_uow_provider import (
    get_budgets_uow,
)
from src.modules.budgets.infrastructure.http_exceptions import (
    handle_budget_not_found,
    handle_unauthorized_budget_access,
)
from src.modules.budgets.infrastructure.sqlalchemy.read_model_repository import (
    SqlAlchemyBudgetReadModelRepository,
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


# ===== Read Model Endpoints =====

@budgets_router.get(
    path="/budgets/read-model",
    status_code=status.HTTP_200_OK,
    summary="Get budgets with spending data (Read Model)",
    description="Returns budgets with pre-calculated spent and remaining values",
)
async def get_budgets_read_model_endpoint(
    user_id: Annotated[str, Depends(authenticate)],
    repository: Annotated[
        SqlAlchemyBudgetReadModelRepository,
        Depends(get_budget_read_model_repository),
    ],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> list[BudgetReadModelResponse]:
    query = GetUserBudgetsReadModelQuery(
        user_id=user_id,
        skip=skip,
        limit=limit,
    )
    budgets = await handle_get_user_budgets_read_model(query, repository)

    return [
        BudgetReadModelResponse(
            budget_id=budget.budget_id,
            user_id=budget.user_id,
            category_id=budget.category_id,
            amount=budget.amount,
            spent=budget.spent,
            remaining=budget.remaining,
            transaction_count=budget.transaction_count,
            period_start=budget.period_start,
            period_end=budget.period_end,
            last_updated=budget.last_updated,
        )
        for budget in budgets
    ]


@budgets_router.get(
    path="/budgets/read-model/active",
    status_code=status.HTTP_200_OK,
    summary="Get active budgets with spending data",
    description="Returns only active budgets with spent and remaining",
)
async def get_active_budgets_read_model_endpoint(
    user_id: Annotated[str, Depends(authenticate)],
    repository: Annotated[
        SqlAlchemyBudgetReadModelRepository,
        Depends(get_budget_read_model_repository),
    ],
) -> list[BudgetReadModelResponse]:
    query = GetActiveBudgetsReadModelQuery(
        user_id=user_id,
        current_date=DateTimeUtils.utc_now(),
    )
    active_budgets = await handle_get_active_budgets_read_model(query, repository)

    return [
        BudgetReadModelResponse(
            budget_id=active_budget.budget_id,
            user_id=active_budget.user_id,
            category_id=active_budget.category_id,
            amount=active_budget.amount,
            spent=active_budget.spent,
            remaining=active_budget.remaining,
            transaction_count=active_budget.transaction_count,
            period_start=active_budget.period_start,
            period_end=active_budget.period_end,
            last_updated=active_budget.last_updated,
        )
        for active_budget in active_budgets
    ]


@budgets_router.get(
    path="/budgets/read-model/{budget_id}",
    status_code=status.HTTP_200_OK,
    summary="Get budget by ID with spending data",
    description="Returns specific budget from read model",
)
async def get_budget_read_model_by_id_endpoint(
    budget_id: str,
    user_id: Annotated[str, Depends(authenticate)],
    repository: Annotated[
        SqlAlchemyBudgetReadModelRepository,
        Depends(get_budget_read_model_repository),
    ],
) -> BudgetReadModelResponse:
    query = GetBudgetReadModelByIdQuery(budget_id=budget_id)
    budget = await handle_get_budget_read_model_by_id(query, repository)

    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found",
        )

    if budget.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    return BudgetReadModelResponse(
        budget_id=budget.budget_id,
        user_id=budget.user_id,
        category_id=budget.category_id,
        amount=budget.amount,
        spent=budget.spent,
        remaining=budget.remaining,
        transaction_count=budget.transaction_count,
        period_start=budget.period_start,
        period_end=budget.period_end,
        last_updated=budget.last_updated,
    )
