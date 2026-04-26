from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import uuid4

from src.libs.utils import DateTimeUtils

if TYPE_CHECKING:
    from datetime import datetime


@dataclass
class Budget:
    budget_id: str
    user_id: str
    category_id: str
    amount: Decimal
    period_start: datetime
    period_end: datetime
    created_at: datetime = field(default_factory=DateTimeUtils.utc_now)
    updated_at: datetime = field(default_factory=DateTimeUtils.utc_now)
    total_spent: Decimal = field(default=Decimal("0.0"))
    transaction_count: int = field(default=0)

    @classmethod
    def create(
        cls,
        user_id: str,
        category_id: str,
        amount: Decimal,
        period_start: datetime,
        period_end: datetime,
    ) -> Budget:
        return cls(
            budget_id=str(uuid4()),
            user_id=user_id,
            category_id=category_id,
            amount=amount,
            period_start=period_start,
            period_end=period_end,
            created_at=DateTimeUtils.utc_now(),
            updated_at=DateTimeUtils.utc_now(),
        )

    def is_active(self, current_date: datetime | None = None) -> bool:
        now = current_date or DateTimeUtils.utc_now()
        return self.period_start <= now <= self.period_end

    def update_amount(self, amount: Decimal) -> None:
        self.amount = amount
        self.updated_at = DateTimeUtils.utc_now()

    def update_period(self, period_start: datetime, period_end: datetime) -> None:
        self.period_start = period_start
        self.period_end = period_end
        self.updated_at = DateTimeUtils.utc_now()

    def to_event(self) -> dict[str, str]:
        return {
            "type": "BudgetCreated",
            "budget_id": self.budget_id,
            "user_id": self.user_id,
            "category_id": self.category_id,
            "amount": str(self.amount),
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat(),
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class BudgetReadModel:
    budget_id: str
    user_id: str
    category_id: str
    amount: Decimal
    spent: Decimal
    remaining: Decimal
    transaction_count: int
    period_start: datetime
    period_end: datetime
    last_updated: datetime

    @classmethod
    def from_budget(cls, budget: Budget) -> BudgetReadModel:
        return cls(
            budget_id=budget.budget_id,
            user_id=budget.user_id,
            category_id=budget.category_id,
            amount=budget.amount,
            spent=Decimal("0.0"),
            remaining=budget.amount,
            transaction_count=0,
            period_start=budget.period_start,
            period_end=budget.period_end,
            last_updated=DateTimeUtils.utc_now(),
        )

    def apply_transaction(self, amount: Decimal) -> None:
        self.spent += amount
        self.remaining = self.amount - self.spent
        self.transaction_count += 1
        self.last_updated = DateTimeUtils.utc_now()

    def reverse_transaction(self, amount: Decimal) -> None:
        self.spent -= amount
        self.remaining = self.amount - self.spent
        self.transaction_count -= 1
        self.last_updated = DateTimeUtils.utc_now()

    def update_amount(self, new_amount: Decimal) -> None:
        self.amount = new_amount
        self.remaining = self.amount - self.spent
        self.last_updated = DateTimeUtils.utc_now()
