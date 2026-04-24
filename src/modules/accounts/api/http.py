from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status

from src.modules.accounts.application.commands import (
    CreateAccountCommand,
    DeleteAccountCommand,
    GetUserAccountsCommand,
    UpdateAccountBalanceCommand,
    UpdateAccountCommand,
)
from src.modules.accounts.application.exceptions import AccountNotFoundError
from src.modules.accounts.application.interfaces.unit_of_work import IAccountsUnitOfWork
from src.modules.accounts.application.use_cases import (
    create_account_use_case,
    delete_account_use_case,
    get_user_accounts_use_case,
    update_account_balance_use_case,
    update_account_use_case,
)
from src.modules.accounts.infrastructure.dependency_injection.uow.accounts_uow_provider import (
    get_accounts_uow,
)
from src.libs.authentication.authentication_client import authenticate

from .dto import (
    AccountResponse,
    CreateAccountRequest,
    UpdateAccountBalanceRequest,
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
        balance=body.balance,
    )
    account = await create_account_use_case(command, unit_of_work=unit_of_work)
    return AccountResponse(
        account_id=account.account_id,
        user_id=account.user_id,
        name=account.name,
        account_type=account.account_type,
        balance=account.balance,
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
            balance=account.balance,
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
        balance=account.balance,
        created_at=account.created_at,
        updated_at=account.updated_at,
    )


@router.patch(path="/accounts/{account_id}/balance")
async def update_account_balance(
    account_id: str,
    _user_id: Annotated[str, Depends(authenticate)],
    body: Annotated[UpdateAccountBalanceRequest, Body()],
    unit_of_work: Annotated[IAccountsUnitOfWork, Depends(get_accounts_uow)],
) -> AccountResponse:
    command = UpdateAccountBalanceCommand(
        account_id=account_id,
        balance=body.balance,
    )
    try:
        account = await update_account_balance_use_case(command, unit_of_work=unit_of_work)
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
        balance=account.balance,
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
