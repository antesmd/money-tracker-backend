from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Mapping

@dataclass
class User:
    user_id: str
    email: str
    username: str
    hashed_password: str
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_event(self) -> Mapping[str, Any]:
        return {
            "type": "UserCreated",
            "user_id": self.user_id,
            "email": self.email,
            "username": self.username,
            "created_at": self.created_at.isoformat(),
        }
