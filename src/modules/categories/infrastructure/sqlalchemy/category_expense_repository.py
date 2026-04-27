from __future__ import annotations

from typing import TYPE_CHECKING, final

from sqlalchemy import delete, select

from src.modules.categories.application.interfaces.repositories import (
    ICategoryExpenseRepository,
)
from src.modules.categories.domain.entities import CategoryExpenseReadModel
from src.modules.categories.infrastructure.sqlalchemy.orm_models import CategoryExpenseORM

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@final
class SqlAlchemyCategoryExpenseRepository(ICategoryExpenseRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_user_and_category(
        self,
        user_id: str,
        category_id: str,
    ) -> CategoryExpenseReadModel | None:
        result = await self._session.execute(
            select(CategoryExpenseORM).where(
                CategoryExpenseORM.user_id == user_id,
                CategoryExpenseORM.category_id == category_id,
            ),
        )
        orm = result.scalar_one_or_none()
        if not orm:
            return None
        return self._to_domain(orm)

    async def get_by_user_id(self, user_id: str) -> list[CategoryExpenseReadModel]:
        result = await self._session.execute(
            select(CategoryExpenseORM).where(CategoryExpenseORM.user_id == user_id),
        )
        return [self._to_domain(orm) for orm in result.scalars().all()]

    async def save(self, read_model: CategoryExpenseReadModel) -> None:
        result = await self._session.execute(
            select(CategoryExpenseORM).where(
                CategoryExpenseORM.user_id == read_model.user_id,
                CategoryExpenseORM.category_id == read_model.category_id,
            ),
        )
        orm = result.scalar_one_or_none()

        if orm:
            orm.category_name = read_model.category_name
            orm.total_amount = read_model.total_amount
            orm.transaction_count = read_model.transaction_count
            orm.last_updated = read_model.last_updated
        else:
            orm = CategoryExpenseORM(
                user_id=read_model.user_id,
                category_id=read_model.category_id,
                category_name=read_model.category_name,
                total_amount=read_model.total_amount,
                transaction_count=read_model.transaction_count,
                last_updated=read_model.last_updated,
            )
            self._session.add(orm)

    async def delete(self, user_id: str, category_id: str) -> None:
        await self._session.execute(
            delete(CategoryExpenseORM).where(
                CategoryExpenseORM.user_id == user_id,
                CategoryExpenseORM.category_id == category_id,
            ),
        )

    def _to_domain(self, orm: CategoryExpenseORM) -> CategoryExpenseReadModel:
        return CategoryExpenseReadModel(
            user_id=orm.user_id,
            category_id=orm.category_id,
            category_name=orm.category_name,
            total_amount=orm.total_amount,
            transaction_count=orm.transaction_count,
            last_updated=orm.last_updated,
        )
