from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any

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
    balance: Decimal
    currency: str = "RUB"
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def to_event(self) -> Mapping[str, Any]:
        return {
            "type": "AccountCreated",
            "account_id": self.account_id,
            "user_id": self.user_id,
            "name": self.name,
            "account_type": self.account_type.value,
            "balance": str(self.balance),
            "currency": self.currency,
            "created_at": self.created_at.isoformat(),
        }
