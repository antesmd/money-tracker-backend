from __future__ import annotations

from typing import TYPE_CHECKING, final

from sqlalchemy import delete, select, update

from src.modules.accounts.application.interfaces.repositories import IAccountRepository
from src.modules.accounts.domain.entities import Account
from src.modules.accounts.infrastructure.sqlalchemy.orm_models import AccountORM

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@final
class SqlAlchemyAccountRepository(IAccountRepository):
    __session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    def add(self, account: Account) -> None:
        orm = AccountORM(
            account_id=account.account_id,
            user_id=account.user_id,
            name=account.name,
            account_type=account.account_type,
            created_at=account.created_at,
            updated_at=account.updated_at,
        )
        self.__session.add(orm)

    async def get_by_id(self, account_id: str) -> Account | None:
        query = select(AccountORM).where(AccountORM.account_id == account_id)
        orm = await self.__session.scalar(query)
        if not orm:
            return None

        return Account(
            account_id=orm.account_id,
            user_id=orm.user_id,
            name=orm.name,
            account_type=orm.account_type,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    async def get_by_user_id(self, user_id: str) -> list[Account]:
        query = select(AccountORM).where(AccountORM.user_id == user_id)
        result = await self.__session.execute(query)
        orms = result.scalars().all()

        return [
            Account(
                account_id=orm.account_id,
                user_id=orm.user_id,
                name=orm.name,
                account_type=orm.account_type,
                created_at=orm.created_at,
                updated_at=orm.updated_at,
            )
            for orm in orms
        ]

    async def update(self, account: Account) -> None:
        stmt = (
            update(AccountORM)
            .where(AccountORM.account_id == account.account_id)
            .values(
                name=account.name,
                account_type=account.account_type,
                updated_at=account.updated_at,
            )
        )
        await self.__session.execute(stmt)

    async def delete(self, account_id: str) -> None:
        stmt = delete(AccountORM).where(AccountORM.account_id == account_id)
        await self.__session.execute(stmt)
