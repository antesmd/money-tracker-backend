from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status

from src.libs.authentication.authentication_client import authenticate
from src.modules.accounts.application.commands import (
    CreateAccountCommand,
    DeleteAccountCommand,
    GetUserAccountsCommand,
    UpdateAccountCommand,
)
from src.modules.accounts.application.exceptions import AccountNotFoundError
from src.modules.accounts.application.interfaces import (
    IAccountReadModelRepository,
)
from src.modules.accounts.application.interfaces.unit_of_work import IAccountsUnitOfWork
from src.modules.accounts.application.queries import (
    GetAccountReadModelByIdQuery,
    GetUserAccountsReadModelQuery,
    handle_get_account_read_model_by_id,
    handle_get_user_accounts_read_model,
)
from src.modules.accounts.application.use_cases import (
    create_account_use_case,
    delete_account_use_case,
    get_user_accounts_use_case,
    update_account_use_case,
)
from src.modules.accounts.infrastructure.dependency_injection import (
    read_model_repository_provider,
)
from src.modules.accounts.infrastructure.dependency_injection.uow.accounts_uow_provider import (
    get_accounts_uow,
)

from .dto import (
    AccountReadModelResponse,
    AccountResponse,
    CreateAccountRequest,
    UpdateAccountRequest,
)

router = APIRouter()


@router.post(path="/accounts", status_code=status.HTTP_201_CREATED)
async def create_account(
    user_id: Annotated[str, Depends(authenticate)],
    body: Annotated[CreateAccountRequest, Body()],
    unit_of_work: Annotated[IAccountsUnitOfWork, Depends(get_accounts_uow)],
) -> AccountResponse:
    command = CreateAccountCommand(
        user_id=user_id,
        name=body.name,
        account_type=body.account_type,
        initial_balance=body.initial_balance,
    )
    account = await create_account_use_case(command, unit_of_work=unit_of_work)
    return AccountResponse(
        account_id=account.account_id,
        user_id=account.user_id,
        name=account.name,
        account_type=account.account_type,
        created_at=account.created_at,
        updated_at=account.updated_at,
    )


@router.get(path="/accounts")
async def get_user_accounts(
    user_id: Annotated[str, Depends(authenticate)],
    unit_of_work: Annotated[IAccountsUnitOfWork, Depends(get_accounts_uow)],
) -> list[AccountResponse]:
    command = GetUserAccountsCommand(user_id=user_id)
    accounts = await get_user_accounts_use_case(command, unit_of_work=unit_of_work)
    return [
        AccountResponse(
            account_id=account.account_id,
            user_id=account.user_id,
            name=account.name,
            account_type=account.account_type,
            created_at=account.created_at,
            updated_at=account.updated_at,
        )
        for account in accounts
    ]


@router.patch(path="/accounts/{account_id}")
async def update_account(
    account_id: str,
    _user_id: Annotated[str, Depends(authenticate)],
    body: Annotated[UpdateAccountRequest, Body()],
    unit_of_work: Annotated[IAccountsUnitOfWork, Depends(get_accounts_uow)],
) -> AccountResponse:
    command = UpdateAccountCommand(
        account_id=account_id,
        name=body.name,
        account_type=body.account_type,
    )
    try:
        account = await update_account_use_case(command, unit_of_work=unit_of_work)
    except AccountNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        ) from exc

    return AccountResponse(
        account_id=account.account_id,
        user_id=account.user_id,
        name=account.name,
        account_type=account.account_type,
        created_at=account.created_at,
        updated_at=account.updated_at,
    )


@router.delete(path="/accounts/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    account_id: str,
    _user_id: Annotated[str, Depends(authenticate)],
    unit_of_work: Annotated[IAccountsUnitOfWork, Depends(get_accounts_uow)],
) -> None:
    command = DeleteAccountCommand(account_id=account_id)
    try:
        await delete_account_use_case(command, unit_of_work=unit_of_work)
    except AccountNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        ) from exc


@router.get(
    path="/accounts/read-model",
    status_code=status.HTTP_200_OK,
    summary="Get accounts with aggregated balance",
)
async def get_accounts_read_model_endpoint(
    user_id: Annotated[str, Depends(authenticate)],
    repository: Annotated[
        IAccountReadModelRepository,
        Depends(read_model_repository_provider.get_account_read_model_repository),
    ],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> list[AccountReadModelResponse]:
    query = GetUserAccountsReadModelQuery(
        user_id=user_id,
        skip=skip,
        limit=limit,
    )
    accounts = await handle_get_user_accounts_read_model(query, repository)

    return [
        AccountReadModelResponse(
            account_id=account.account_id,
            user_id=account.user_id,
            name=account.name,
            account_type=account.account_type,
            balance=account.balance,
            total_inflow=account.total_inflow,
            total_outflow=account.total_outflow,
            transaction_count=account.transaction_count,
            last_updated=account.last_updated,
        )
        for account in accounts
    ]


@router.get(
    path="/accounts/read-model/{account_id}",
    status_code=status.HTTP_200_OK,
    summary="Get account by ID with balance aggregation",
)
async def get_account_read_model_by_id_endpoint(
    account_id: str,
    user_id: Annotated[str, Depends(authenticate)],
    repository: Annotated[
        IAccountReadModelRepository,
        Depends(read_model_repository_provider.get_account_read_model_repository),
    ],
) -> AccountReadModelResponse:
    query = GetAccountReadModelByIdQuery(account_id=account_id)
    account = await handle_get_account_read_model_by_id(query, repository)

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )

    if account.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    return AccountReadModelResponse(
        account_id=account.account_id,
        user_id=account.user_id,
        name=account.name,
        account_type=account.account_type,
        balance=account.balance,
        total_inflow=account.total_inflow,
        total_outflow=account.total_outflow,
        transaction_count=account.transaction_count,
        last_updated=account.last_updated,
    )
