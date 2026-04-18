from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.categories.domain.entities import Category


class ICategoryRepository(ABC):
    @abstractmethod
    def add(self, category: Category) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, category_id: str) -> Category | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_user_id(self, user_id: str) -> list[Category]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, category: Category) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, category_id: str) -> None:
        raise NotImplementedError
