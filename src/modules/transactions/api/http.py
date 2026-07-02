from __future__ import annotations

from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from pydantic import NaiveDatetime

from src.libs.authentication.authentication_client import authenticate
from src.modules.accounts.application.interfaces.unit_of_work import IAccountsUnitOfWork
from src.modules.accounts.infrastructure.dependency_injection.uow.accounts_uow_provider import (
    get_accounts_uow,
)
from src.modules.categories.application.interfaces.unit_of_work import ICategoriesUnitOfWork
from src.modules.categories.infrastructure.dependency_injection.uow.categories_uow_provider import (
    get_categories_uow,
)
from src.modules.transactions.application.commands import (
    CreateTransactionCommand,
    DeleteTransactionCommand,
    GetAccountTransactionsCommand,
    GetTransactionsByDateRangeCommand,
    GetUserTransactionsCommand,
    UpdateTransactionCommand,
)
from src.modules.transactions.application.exceptions import TransactionNotFoundError
from src.modules.transactions.application.interfaces.repositories import (
    IDashboardStatisticsRepository,
)
from src.modules.transactions.application.interfaces.unit_of_work import (
    ITransactionsUnitOfWork,
)
from src.modules.transactions.application.queries import (
    GetDashboardStatisticsQuery,
    handle_get_dashboard_statistics,
)
from src.modules.transactions.application.use_cases import (
    create_transaction_use_case,
    delete_transaction_use_case,
    get_account_transactions_use_case,
    get_transactions_by_date_range_use_case,
    get_user_transactions_use_case,
    update_transaction_use_case,
)
from src.modules.transactions.infrastructure.dependency_injection import (
    get_dashboard_statistics_repository,
    get_transactions_uow,
)

from .dto import (
    CreateTransactionRequest,
    DashboardStatisticsResponse,
    TransactionResponse,
    TransactionTypeDistribution,
    UpdateTransactionRequest,
)
from .ownership import ensure_account_and_category_ownership

router = APIRouter()

_get_dashboard_statistics_repository = get_dashboard_statistics_repository
_get_transactions_uow = get_transactions_uow


@router.post(path="/transactions", status_code=status.HTTP_201_CREATED)
async def create_transaction(
    user_id: Annotated[str, Depends(authenticate)],
    body: Annotated[CreateTransactionRequest, Body()],
    unit_of_work: Annotated[ITransactionsUnitOfWork, Depends(_get_transactions_uow)],
    accounts_uow: Annotated[IAccountsUnitOfWork, Depends(get_accounts_uow)],
    categories_uow: Annotated[ICategoriesUnitOfWork, Depends(get_categories_uow)],
) -> TransactionResponse:
    await ensure_account_and_category_ownership(
        user_id=user_id,
        account_id=body.account_id,
        category_id=body.category_id,
        accounts_uow=accounts_uow,
        categories_uow=categories_uow,
    )
    command = CreateTransactionCommand(
        user_id=user_id,
        account_id=body.account_id,
        category_id=body.category_id,
        transaction_type=body.transaction_type,
        amount=body.amount,
        description=body.description,
        date=body.date,
    )
    transaction = await create_transaction_use_case(command, unit_of_work=unit_of_work)
    return TransactionResponse(
        transaction_id=transaction.transaction_id,
        user_id=transaction.user_id,
        account_id=transaction.account_id,
        category_id=transaction.category_id,
        transaction_type=transaction.transaction_type,
        amount=transaction.amount,
        description=transaction.description,
        date=transaction.date,
        created_at=transaction.created_at,
        updated_at=transaction.updated_at,
    )


@router.get(path="/transactions")
async def get_user_transactions(
    user_id: Annotated[str, Depends(authenticate)],
    unit_of_work: Annotated[ITransactionsUnitOfWork, Depends(_get_transactions_uow)],
    limit: Annotated[int | None, Query(ge=0, le=100)] = None,
    offset: Annotated[int | None, Query(ge=0, le=1000)] = None,
) -> list[TransactionResponse]:
    command = GetUserTransactionsCommand(user_id=user_id, limit=limit, offset=offset)
    transactions = await get_user_transactions_use_case(command, unit_of_work=unit_of_work)
    return [
        TransactionResponse(
            transaction_id=t.transaction_id,
            user_id=t.user_id,
            account_id=t.account_id,
            category_id=t.category_id,
            transaction_type=t.transaction_type,
            amount=t.amount,
            description=t.description,
            date=t.date,
            created_at=t.created_at,
            updated_at=t.updated_at,
        )
        for t in transactions
    ]


@router.get(path="/accounts/{account_id}/transactions")
async def get_account_transactions(
    account_id: str,
    user_id: Annotated[str, Depends(authenticate)],
    unit_of_work: Annotated[ITransactionsUnitOfWork, Depends(_get_transactions_uow)],
    limit: Annotated[int | None, Query(ge=0, le=100)] = None,
    offset: Annotated[int | None, Query(ge=0, le=1000)] = None,
) -> list[TransactionResponse]:
    command = GetAccountTransactionsCommand(
        account_id=account_id,
        user_id=user_id,
        limit=limit,
        offset=offset,
    )
    transactions = await get_account_transactions_use_case(command, unit_of_work=unit_of_work)
    return [
        TransactionResponse(
            transaction_id=t.transaction_id,
            user_id=t.user_id,
            account_id=t.account_id,
            category_id=t.category_id,
            transaction_type=t.transaction_type,
            amount=t.amount,
            description=t.description,
            date=t.date,
            created_at=t.created_at,
            updated_at=t.updated_at,
        )
        for t in transactions
    ]


@router.get(path="/transactions/date-range")
async def get_transactions_by_date_range(
    user_id: Annotated[str, Depends(authenticate)],
    unit_of_work: Annotated[ITransactionsUnitOfWork, Depends(_get_transactions_uow)],
    start_date: Annotated[NaiveDatetime, Query()],
    end_date: Annotated[NaiveDatetime, Query()],
) -> list[TransactionResponse]:
    command = GetTransactionsByDateRangeCommand(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
    )
    transactions = await get_transactions_by_date_range_use_case(command, unit_of_work=unit_of_work)
    return [
        TransactionResponse(
            transaction_id=t.transaction_id,
            user_id=t.user_id,
            account_id=t.account_id,
            category_id=t.category_id,
            transaction_type=t.transaction_type,
            amount=t.amount,
            description=t.description,
            date=t.date,
            created_at=t.created_at,
            updated_at=t.updated_at,
        )
        for t in transactions
    ]


@router.patch(path="/transactions/{transaction_id}")
async def update_transaction(
    transaction_id: str,
    user_id: Annotated[str, Depends(authenticate)],
    body: Annotated[UpdateTransactionRequest, Body()],
    unit_of_work: Annotated[ITransactionsUnitOfWork, Depends(_get_transactions_uow)],
    accounts_uow: Annotated[IAccountsUnitOfWork, Depends(get_accounts_uow)],
    categories_uow: Annotated[ICategoriesUnitOfWork, Depends(get_categories_uow)],
) -> TransactionResponse:
    await ensure_account_and_category_ownership(
        user_id=user_id,
        account_id=body.account_id,
        category_id=body.category_id,
        accounts_uow=accounts_uow,
        categories_uow=categories_uow,
    )
    command = UpdateTransactionCommand(
        transaction_id=transaction_id,
        user_id=user_id,
        account_id=body.account_id,
        category_id=body.category_id,
        transaction_type=body.transaction_type,
        amount=body.amount,
        description=body.description,
        date=body.date,
    )
    try:
        transaction = await update_transaction_use_case(command, unit_of_work=unit_of_work)
    except TransactionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        ) from exc

    return TransactionResponse(
        transaction_id=transaction.transaction_id,
        user_id=transaction.user_id,
        account_id=transaction.account_id,
        category_id=transaction.category_id,
        transaction_type=transaction.transaction_type,
        amount=transaction.amount,
        description=transaction.description,
        date=transaction.date,
        created_at=transaction.created_at,
        updated_at=transaction.updated_at,
    )


@router.get(path="/statistics/dashboard", response_model=DashboardStatisticsResponse)
async def get_dashboard_statistics_endpoint(
    user_id: Annotated[str, Depends(authenticate)],
    dashboard_repo: Annotated[
        IDashboardStatisticsRepository,
        Depends(_get_dashboard_statistics_repository),
    ],
) -> DashboardStatisticsResponse:
    query = GetDashboardStatisticsQuery(user_id=user_id)
    dashboard_stats = await handle_get_dashboard_statistics(query, dashboard_repo)

    total_income = dashboard_stats.total_income if dashboard_stats else Decimal("0.0")
    total_expense = dashboard_stats.total_expense if dashboard_stats else Decimal("0.0")

    return DashboardStatisticsResponse(
        transaction_distribution=TransactionTypeDistribution(
            income=total_income,
            expense=total_expense,
        ),
    )


@router.delete(path="/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: str,
    user_id: Annotated[str, Depends(authenticate)],
    unit_of_work: Annotated[ITransactionsUnitOfWork, Depends(get_transactions_uow)],
) -> None:
    command = DeleteTransactionCommand(transaction_id=transaction_id, user_id=user_id)
    try:
        await delete_transaction_use_case(command, unit_of_work=unit_of_work)
    except TransactionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        ) from exc
