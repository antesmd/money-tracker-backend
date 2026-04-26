from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING, Any

from src.libs.utils import DateTimeUtils

if TYPE_CHECKING:
    from collections.abc import Mapping
    from decimal import Decimal


class AccountType(str, Enum):
    CASH = "cash"
    CARD = "card"
    DEPOSIT = "deposit"
    SAVINGS = "savings"
    INVESTMENT = "investment"


@dataclass
class Account:
    account_id: str
    user_id: str
    name: str
    account_type: AccountType
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def to_event(self) -> Mapping[str, Any]:
        return {
            "type": "AccountCreated",
            "account_id": self.account_id,
            "user_id": self.user_id,
            "name": self.name,
            "account_type": self.account_type.value,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class AccountReadModel:
    account_id: str
    user_id: str
    name: str
    account_type: AccountType
    balance: Decimal
    total_inflow: Decimal
    total_outflow: Decimal
    transaction_count: int
    last_updated: datetime

    @classmethod
    def from_account(cls, account: Account, initial_balance: Decimal = Decimal("0.0")) -> AccountReadModel:
        return cls(
            account_id=account.account_id,
            user_id=account.user_id,
            name=account.name,
            account_type=account.account_type,
            balance=initial_balance,
            total_inflow=Decimal("0.0"),
            total_outflow=Decimal("0.0"),
            transaction_count=0,
            last_updated=DateTimeUtils.utc_now(),
        )

    def apply_transaction(self, transaction_type: str, amount: Decimal) -> None:
        tx_type = transaction_type.value if hasattr(transaction_type, "value") else transaction_type
        if tx_type == "income":
            self.balance += amount
            self.total_inflow += amount
        else:
            self.balance -= amount
            self.total_outflow += amount

        self.transaction_count += 1
        self.last_updated = DateTimeUtils.utc_now()

    def reverse_transaction(self, transaction_type: str, amount: Decimal) -> None:
        tx_type = transaction_type.value if hasattr(transaction_type, "value") else transaction_type
        if tx_type == "income":
            self.balance -= amount
            self.total_inflow -= amount
        else:
            self.balance += amount
            self.total_outflow -= amount

        self.transaction_count -= 1
        self.last_updated = DateTimeUtils.utc_now()

    def update_account(
        self,
        name: str | None,
        account_type: AccountType | None,
    ) -> None:
        if name is not None:
            self.name = name
        if account_type is not None:
            self.account_type = account_type
        self.last_updated = DateTimeUtils.utc_now()
