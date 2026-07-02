from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import uuid4

from src.modules.accounts.application.exceptions import AccountNotFoundError
from src.modules.accounts.domain.entities import Account
from src.libs.utils import DateTimeUtils

if TYPE_CHECKING:
    from src.modules.accounts.application.commands import (
        CreateAccountCommand,
        DeleteAccountCommand,
        GetUserAccountsCommand,
        UpdateAccountCommand,
    )
    from src.modules.accounts.application.interfaces.unit_of_work import IAccountsUnitOfWork


async def handle_create_account(
    command: CreateAccountCommand,
    unit_of_work: IAccountsUnitOfWork,
) -> Account:
    account = Account(
        account_id=str(uuid4()),
        user_id=command.user_id,
        name=command.name,
        account_type=command.account_type,
    )
    unit_of_work.accounts.add(account)
    await unit_of_work.commit()
    return account


async def handle_update_account(
    command: UpdateAccountCommand,
    unit_of_work: IAccountsUnitOfWork,
) -> Account:
    account = await unit_of_work.accounts.get_by_id(command.account_id)
    if not account or account.user_id != command.user_id:
        raise AccountNotFoundError

    account.name = command.name
    account.account_type = command.account_type
    account.updated_at = DateTimeUtils.utc_now()
    await unit_of_work.accounts.update(account)
    await unit_of_work.commit()
    return account


async def handle_delete_account(
    command: DeleteAccountCommand,
    unit_of_work: IAccountsUnitOfWork,
) -> None:
    account = await unit_of_work.accounts.get_by_id(command.account_id)
    if not account or account.user_id != command.user_id:
        raise AccountNotFoundError

    await unit_of_work.accounts.delete(command.account_id)
    await unit_of_work.commit()


async def handle_get_user_accounts(
    command: GetUserAccountsCommand,
    unit_of_work: IAccountsUnitOfWork,
) -> list[Account]:
    return await unit_of_work.accounts.get_by_user_id(command.user_id)
