from __future__ import annotations

from typing import TYPE_CHECKING, final

from sqlalchemy import delete, select, update

from src.modules.categories.application.interfaces.repositories import ICategoryRepository
from src.modules.categories.domain.entities import Category
from src.modules.categories.infrastructure.sqlalchemy.orm_models import CategoryORM

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@final
class SqlAlchemyCategoryRepository(ICategoryRepository):
    __session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    def add(self, category: Category) -> None:
        orm = CategoryORM(
            category_id=category.category_id,
            user_id=category.user_id,
            name=category.name,
            type=category.type,
            created_at=category.created_at,
            updated_at=category.updated_at,
        )
        self.__session.add(orm)

    async def get_by_id(self, category_id: str) -> Category | None:
        query = select(CategoryORM).where(CategoryORM.category_id == category_id)
        orm = await self.__session.scalar(query)
        if not orm:
            return None

        return Category(
            category_id=orm.category_id,
            user_id=orm.user_id,
            name=orm.name,
            type=orm.type,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    async def get_by_user_id(self, user_id: str) -> list[Category]:
        query = select(CategoryORM).where(CategoryORM.user_id == user_id)
        result = await self.__session.execute(query)
        orms = result.scalars().all()

        return [
            Category(
                category_id=orm.category_id,
                user_id=orm.user_id,
                name=orm.name,
                type=orm.type,
                created_at=orm.created_at,
                updated_at=orm.updated_at,
            )
            for orm in orms
        ]

    async def update(self, category: Category) -> None:
        stmt = (
            update(CategoryORM)
            .where(CategoryORM.category_id == category.category_id)
            .values(
                name=category.name,
                updated_at=category.updated_at,
            )
        )
        await self.__session.execute(stmt)

    async def delete(self, category_id: str) -> None:
        stmt = delete(CategoryORM).where(CategoryORM.category_id == category_id)
        await self.__session.execute(stmt)
