from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Mapping


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


@dataclass
class Transaction:
    transaction_id: str
    user_id: str  # No FK - weak coupling
    account_id: str  # Reference to accounts module - no FK
    category_id: str  # Reference to categories module - no FK
    type: TransactionType
    amount: Decimal
    description: str | None = None
    date: datetime = field(default_factory=datetime.utcnow)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def to_event(self) -> Mapping[str, Any]:
        return {
            "type": "TransactionCreated",
            "transaction_id": self.transaction_id,
            "user_id": self.user_id,
            "account_id": self.account_id,
            "category_id": self.category_id,
            "transaction_type": self.type.value,
            "amount": str(self.amount),
            "description": self.description,
            "date": self.date.isoformat(),
            "created_at": self.created_at.isoformat(),
        }
