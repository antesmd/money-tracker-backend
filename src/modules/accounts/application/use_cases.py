from __future__ import annotations

from typing import TYPE_CHECKING

from src.modules.accounts.application import handlers

if TYPE_CHECKING:
    from src.modules.accounts.application.commands import (
        CreateAccountCommand,
        DeleteAccountCommand,
        GetUserAccountsCommand,
        UpdateAccountBalanceCommand,
        UpdateAccountCommand,
    )
    from src.modules.accounts.application.interfaces.unit_of_work import IAccountsUnitOfWork
    from src.modules.accounts.domain.entities import Account


async def create_account_use_case(
    command: CreateAccountCommand,
    unit_of_work: IAccountsUnitOfWork,
) -> Account:
    return await handlers.handle_create_account(command, unit_of_work)


async def update_account_use_case(
    command: UpdateAccountCommand,
    unit_of_work: IAccountsUnitOfWork,
) -> Account:
    return await handlers.handle_update_account(command, unit_of_work)


async def update_account_balance_use_case(
    command: UpdateAccountBalanceCommand,
    unit_of_work: IAccountsUnitOfWork,
) -> Account:
    return await handlers.handle_update_account_balance(command, unit_of_work)


async def delete_account_use_case(
    command: DeleteAccountCommand,
    unit_of_work: IAccountsUnitOfWork,
) -> None:
    await handlers.handle_delete_account(command, unit_of_work)


async def get_user_accounts_use_case(
    command: GetUserAccountsCommand,
    unit_of_work: IAccountsUnitOfWork,
) -> list[Account]:
    return await handlers.handle_get_user_accounts(command, unit_of_work)
