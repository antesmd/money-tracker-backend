from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select

from src.identity.application.interfaces.repositories import IUserRepository
from src.identity.domain.entities import User
from src.identity.infrastructure.sqlalchemy.orm_models import UserORM

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class SqlAlchemyUserRepository(IUserRepository):
    __session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    def add(self, user: User) -> None:
        orm = UserORM(
            user_id=user.user_id,
            email=user.email,
            username=user.username,
            hashed_password=user.hashed_password,
            created_at=user.created_at,
        )
        self.__session.add(orm)

    async def get_by_id(self, user_id: str) -> User | None:
        query = select(UserORM).where(UserORM.user_id == user_id)
        user = await self.__session.scalar(query)
        if not user:
            return None

        return User(
            user_id=user.user_id,
            email=user.email,
            username=user.username,
            hashed_password=user.hashed_password,
            created_at=user.created_at,
        )

    async def get_by_email(self, email: str) -> User | None:
        query = select(UserORM).where(UserORM.email == email)
        user = await self.__session.scalar(query)
        if not user:
            return None

        return User(
            user_id=user.user_id,
            email=user.email,
            username=user.username,
            hashed_password=user.hashed_password,
            created_at=user.created_at,
        )
