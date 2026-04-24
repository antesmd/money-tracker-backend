from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Mapping


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


@dataclass
class Category:
    category_id: str
    user_id: str  # Ссылка на пользователя без FK - слабая связь между доменами
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
