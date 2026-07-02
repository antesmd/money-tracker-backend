from __future__ import annotations

from typing import TYPE_CHECKING, final

from sqlalchemy import select, update

from src.modules.identity.application.interfaces.repositories import IUserRepository
from src.modules.identity.domain.entities import User
from src.modules.identity.domain.roles import Role
from src.modules.identity.infrastructure.sqlalchemy.orm_models import UserORM

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@final
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
            role=user.role.value,
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
            role=Role(user.role),
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
            role=Role(user.role),
            created_at=user.created_at,
        )

    async def list_all(self) -> list[User]:
        query = select(UserORM)
        result = await self.__session.execute(query)
        orms = result.scalars().all()

        return [
            User(
                user_id=orm.user_id,
                email=orm.email,
                username=orm.username,
                hashed_password=orm.hashed_password,
                role=Role(orm.role),
                created_at=orm.created_at,
            )
            for orm in orms
        ]

    async def set_role(self, user_id: str, role: Role) -> None:
        stmt = update(UserORM).where(UserORM.user_id == user_id).values(role=role.value)
        await self.__session.execute(stmt)
