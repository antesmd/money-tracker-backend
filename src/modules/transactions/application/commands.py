from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from datetime import datetime
    from decimal import Decimal

    from src.modules.transactions.domain.entities import TransactionType


class CreateTransactionCommand(NamedTuple):
    user_id: str
    account_id: str
    category_id: str | None
    transaction_type: TransactionType
    amount: Decimal
    description: str | None = None
    date: datetime | None = None


class UpdateTransactionCommand(NamedTuple):
    transaction_id: str
    user_id: str
    account_id: str
    category_id: str | None
    transaction_type: TransactionType
    amount: Decimal
    description: str | None = None
    date: datetime | None = None


class DeleteTransactionCommand(NamedTuple):
    transaction_id: str
    user_id: str


class GetUserTransactionsCommand(NamedTuple):
    user_id: str
    limit: int | None = None
    offset: int | None = None


class GetAccountTransactionsCommand(NamedTuple):
    account_id: str
    user_id: str
    limit: int | None = None
    offset: int | None = None


class GetTransactionsByDateRangeCommand(NamedTuple):
    user_id: str
    start_date: datetime
    end_date: datetime
