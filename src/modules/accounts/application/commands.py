from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from decimal import Decimal

    from src.modules.accounts.domain.entities import AccountType


class CreateAccountCommand(NamedTuple):
    user_id: str
    name: str
    account_type: AccountType
    initial_balance: Decimal


class UpdateAccountCommand(NamedTuple):
    account_id: str
    name: str
    account_type: AccountType


class DeleteAccountCommand(NamedTuple):
    account_id: str


class GetUserAccountsCommand(NamedTuple):
    user_id: str
