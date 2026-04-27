from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.categories.domain.entities import Category, CategoryExpenseReadModel


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


class ICategoryExpenseRepository(ABC):
    @abstractmethod
    async def get_by_user_and_category(
        self,
        user_id: str,
        category_id: str,
    ) -> CategoryExpenseReadModel | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_user_id(self, user_id: str) -> list[CategoryExpenseReadModel]:
        raise NotImplementedError

    @abstractmethod
    async def save(self, read_model: CategoryExpenseReadModel) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user_id: str, category_id: str) -> None:
        raise NotImplementedError
