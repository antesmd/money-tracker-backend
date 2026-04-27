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
class Category:
    category_id: str
    user_id: str
    name: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def to_event(self) -> Mapping[str, Any]:
        return {
            "type": "CategoryCreated",
            "category_id": self.category_id,
            "user_id": self.user_id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class CategoryExpenseReadModel:
    user_id: str
    category_id: str
    category_name: str
    total_amount: Decimal
    transaction_count: int
    last_updated: datetime

    @classmethod
    def create(cls, user_id: str, category_id: str, category_name: str) -> CategoryExpenseReadModel:
        return cls(
            user_id=user_id,
            category_id=category_id,
            category_name=category_name,
            total_amount=Decimal("0.0"),
            transaction_count=0,
            last_updated=DateTimeUtils.utc_now(),
        )

    def apply_transaction(self, amount: Decimal) -> None:
        self.total_amount += amount
        self.transaction_count += 1
        self.last_updated = DateTimeUtils.utc_now()

    def reverse_transaction(self, amount: Decimal) -> None:
        self.total_amount -= amount
        self.transaction_count -= 1
        self.last_updated = DateTimeUtils.utc_now()

    def update_category_name(self, category_name: str) -> None:
        self.category_name = category_name
        self.last_updated = DateTimeUtils.utc_now()
