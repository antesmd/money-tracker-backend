from __future__ import annotations

from typing import TYPE_CHECKING

from src.modules.accounts.application import handlers
from src.modules.accounts.application.event_handlers import (
    handle_account_created,
    handle_account_deleted,
    handle_account_updated,
)

if TYPE_CHECKING:
    from src.modules.accounts.application.commands import (
        CreateAccountCommand,
        DeleteAccountCommand,
        GetUserAccountsCommand,
        UpdateAccountCommand,
    )
    from src.modules.accounts.application.interfaces.unit_of_work import IAccountsUnitOfWork
    from src.modules.accounts.domain.entities import Account


async def create_account_use_case(
    command: CreateAccountCommand,
    unit_of_work: IAccountsUnitOfWork,
) -> Account:
    account = await handlers.handle_create_account(command, unit_of_work)
    await handle_account_created(account, initial_balance=command.initial_balance)
    return account


async def update_account_use_case(
    command: UpdateAccountCommand,
    unit_of_work: IAccountsUnitOfWork,
) -> Account:
    account = await handlers.handle_update_account(command, unit_of_work)
    await handle_account_updated(account)
    return account


async def delete_account_use_case(
    command: DeleteAccountCommand,
    unit_of_work: IAccountsUnitOfWork,
) -> None:
    await handlers.handle_delete_account(command, unit_of_work)
    await handle_account_deleted(command.account_id)


async def get_user_accounts_use_case(
    command: GetUserAccountsCommand,
    unit_of_work: IAccountsUnitOfWork,
) -> list[Account]:
    return await handlers.handle_get_user_accounts(command, unit_of_work)
