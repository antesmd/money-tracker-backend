from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from decimal import Decimal

    from src.modules.accounts.domain.entities import AccountType


class CreateAccountCommand(NamedTuple):
    user_id: str
    name: str
    account_type: AccountType
    balance: Decimal
    currency: str = "RUB"


class UpdateAccountCommand(NamedTuple):
    account_id: str
    name: str
    account_type: AccountType


class UpdateAccountBalanceCommand(NamedTuple):
    account_id: str
    balance: Decimal


class DeleteAccountCommand(NamedTuple):
    account_id: str


class GetUserAccountsCommand(NamedTuple):
    user_id: str
