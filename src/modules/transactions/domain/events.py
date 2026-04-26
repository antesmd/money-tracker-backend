from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime
    from decimal import Decimal

    from src.modules.transactions.domain.entities import TransactionType


@dataclass(frozen=True)
class TransactionCreatedEvent:
    """Событие создания транзакции"""
    transaction_id: str
    user_id: str
    account_id: str
    category_id: str
    transaction_type: TransactionType
    amount: Decimal
    description: str | None
    date: datetime
    created_at: datetime


@dataclass(frozen=True)
class TransactionUpdatedEvent:
    """Событие обновления транзакции"""
    transaction_id: str
    user_id: str
    account_id: str
    category_id: str
    transaction_type: TransactionType
    amount: Decimal
    description: str | None
    date: datetime
    updated_at: datetime
    old_category_id: str
    old_amount: Decimal


@dataclass(frozen=True)
class TransactionDeletedEvent:
    """Событие удаления транзакции"""
    transaction_id: str
    user_id: str
    account_id: str
    category_id: str
    transaction_type: TransactionType
    amount: Decimal
    date: datetime
