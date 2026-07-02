from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.identity.domain.entities import User
    from src.modules.identity.domain.roles import Role


class IUserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[User]:
        raise NotImplementedError

    @abstractmethod
    async def set_role(self, user_id: str, role: Role) -> None:
        raise NotImplementedError
