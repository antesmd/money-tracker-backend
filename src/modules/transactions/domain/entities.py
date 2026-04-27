from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING, Any

from src.libs.utils import DateTimeUtils

if TYPE_CHECKING:
    from collections.abc import Mapping


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


@dataclass
class Transaction:
    transaction_id: str
    user_id: str
    account_id: str
    category_id: str | None
    transaction_type: TransactionType
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
            "transaction_type": self.transaction_type.value,
            "amount": str(self.amount),
            "description": self.description,
            "date": self.date.isoformat(),
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class DashboardStatisticsReadModel:
    user_id: str
    total_income: Decimal
    total_expense: Decimal
    last_updated: datetime

    @classmethod
    def create(cls, user_id: str) -> DashboardStatisticsReadModel:
        return cls(
            user_id=user_id,
            total_income=Decimal("0.0"),
            total_expense=Decimal("0.0"),
            last_updated=DateTimeUtils.utc_now(),
        )

    def apply_transaction(self, transaction_type: str, amount: Decimal) -> None:
        tx_type = transaction_type.value if hasattr(transaction_type, "value") else transaction_type
        if tx_type.lower() == "income":
            self.total_income += amount
        elif tx_type.lower() == "expense":
            self.total_expense += amount
        self.last_updated = DateTimeUtils.utc_now()

    def reverse_transaction(self, transaction_type: str, amount: Decimal) -> None:
        tx_type = transaction_type.value if hasattr(transaction_type, "value") else transaction_type
        if tx_type.lower() == "income":
            self.total_income -= amount
        elif tx_type.lower() == "expense":
            self.total_expense -= amount
        self.last_updated = DateTimeUtils.utc_now()

    def update_transaction(
        self,
        old_type: str,
        new_type: str,
        old_amount: Decimal,
        new_amount: Decimal,
    ) -> None:
        self.reverse_transaction(old_type, old_amount)
        self.apply_transaction(new_type, new_amount)
