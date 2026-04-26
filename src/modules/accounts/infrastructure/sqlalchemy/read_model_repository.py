from __future__ import annotations

from typing import TYPE_CHECKING, final

from sqlalchemy import select

from src.modules.accounts.application.interfaces import IAccountReadModelRepository
from src.modules.accounts.domain.entities import AccountReadModel
from src.modules.accounts.infrastructure.sqlalchemy.orm_models import AccountReadModelORM

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@final
class SqlAlchemyAccountReadModelRepository(IAccountReadModelRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, account_id: str) -> AccountReadModel | None:
        result = await self._session.execute(
            select(AccountReadModelORM).where(AccountReadModelORM.account_id == account_id),
        )
        orm = result.scalar_one_or_none()
        if not orm:
            return None
        return self._to_domain(orm)

    async def get_by_user_id(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 100,
    ) -> list[AccountReadModel]:
        result = await self._session.execute(
            select(AccountReadModelORM)
            .where(AccountReadModelORM.user_id == user_id)
            .offset(skip)
            .limit(limit),
        )
        return [self._to_domain(orm) for orm in result.scalars().all()]

    async def save(self, read_model: AccountReadModel) -> None:
        result = await self._session.execute(
            select(AccountReadModelORM).where(
                AccountReadModelORM.account_id == read_model.account_id,
            ),
        )
        orm = result.scalar_one_or_none()

        if orm:
            orm.name = read_model.name
            orm.account_type = read_model.account_type
            orm.balance = read_model.balance
            orm.total_inflow = read_model.total_inflow
            orm.total_outflow = read_model.total_outflow
            orm.transaction_count = read_model.transaction_count
            orm.last_updated = read_model.last_updated
        else:
            orm = AccountReadModelORM(
                account_id=read_model.account_id,
                user_id=read_model.user_id,
                name=read_model.name,
                account_type=read_model.account_type,
                balance=read_model.balance,
                total_inflow=read_model.total_inflow,
                total_outflow=read_model.total_outflow,
                transaction_count=read_model.transaction_count,
                last_updated=read_model.last_updated,
            )
            self._session.add(orm)

    async def delete(self, account_id: str) -> None:
        result = await self._session.execute(
            select(AccountReadModelORM).where(
                AccountReadModelORM.account_id == account_id,
            ),
        )
        orm = result.scalar_one_or_none()
        if orm:
            await self._session.delete(orm)

    def _to_domain(self, orm: AccountReadModelORM) -> AccountReadModel:
        return AccountReadModel(
            account_id=orm.account_id,
            user_id=orm.user_id,
            name=orm.name,
            account_type=orm.account_type,
            balance=orm.balance,
            total_inflow=orm.total_inflow,
            total_outflow=orm.total_outflow,
            transaction_count=orm.transaction_count,
            last_updated=orm.last_updated,
        )
