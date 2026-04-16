from __future__ import annotations

from typing import TYPE_CHECKING, final

from sqlalchemy import delete, select, update

from src.modules.transactions.application.interfaces.repositories import ITransactionRepository
from src.modules.transactions.domain.entities import Transaction
from src.modules.transactions.infrastructure.sqlalchemy.orm_models import TransactionORM

if TYPE_CHECKING:
    from datetime import datetime

    from sqlalchemy.ext.asyncio import AsyncSession


@final
class SqlAlchemyTransactionRepository(ITransactionRepository):
    __session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    def add(self, transaction: Transaction) -> None:
        orm = TransactionORM(
            transaction_id=transaction.transaction_id,
            user_id=transaction.user_id,
            account_id=transaction.account_id,
            category_id=transaction.category_id,
            type=transaction.type,
            amount=transaction.amount,
            description=transaction.description,
            date=transaction.date,
            created_at=transaction.created_at,
            updated_at=transaction.updated_at,
        )
        self.__session.add(orm)

    async def get_by_id(self, transaction_id: str) -> Transaction | None:
        query = select(TransactionORM).where(TransactionORM.transaction_id == transaction_id)
        orm = await self.__session.scalar(query)
        if not orm:
            return None

        return Transaction(
            transaction_id=orm.transaction_id,
            user_id=orm.user_id,
            account_id=orm.account_id,
            category_id=orm.category_id,
            type=orm.type,
            amount=orm.amount,
            description=orm.description,
            date=orm.date,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    async def get_by_user_id(
        self,
        user_id: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[Transaction]:
        query = (
            select(TransactionORM)
            .where(TransactionORM.user_id == user_id)
            .order_by(TransactionORM.date.desc())
        )
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)

        result = await self.__session.execute(query)
        orms = result.scalars().all()

        return [
            Transaction(
                transaction_id=orm.transaction_id,
                user_id=orm.user_id,
                account_id=orm.account_id,
                category_id=orm.category_id,
                type=orm.type,
                amount=orm.amount,
                description=orm.description,
                date=orm.date,
                created_at=orm.created_at,
                updated_at=orm.updated_at,
            )
            for orm in orms
        ]

    async def get_by_account_id(
        self,
        account_id: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[Transaction]:
        query = (
            select(TransactionORM)
            .where(TransactionORM.account_id == account_id)
            .order_by(TransactionORM.date.desc())
        )
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)

        result = await self.__session.execute(query)
        orms = result.scalars().all()

        return [
            Transaction(
                transaction_id=orm.transaction_id,
                user_id=orm.user_id,
                account_id=orm.account_id,
                category_id=orm.category_id,
                type=orm.type,
                amount=orm.amount,
                description=orm.description,
                date=orm.date,
                created_at=orm.created_at,
                updated_at=orm.updated_at,
            )
            for orm in orms
        ]

    async def get_by_date_range(
        self,
        user_id: str,
        start_date: datetime,
        end_date: datetime,
    ) -> list[Transaction]:
        query = (
            select(TransactionORM)
            .where(
                TransactionORM.user_id == user_id,
                TransactionORM.date >= start_date,
                TransactionORM.date <= end_date,
            )
            .order_by(TransactionORM.date.desc())
        )

        result = await self.__session.execute(query)
        orms = result.scalars().all()

        return [
            Transaction(
                transaction_id=orm.transaction_id,
                user_id=orm.user_id,
                account_id=orm.account_id,
                category_id=orm.category_id,
                type=orm.type,
                amount=orm.amount,
                description=orm.description,
                date=orm.date,
                created_at=orm.created_at,
                updated_at=orm.updated_at,
            )
            for orm in orms
        ]

    async def update(self, transaction: Transaction) -> None:
        stmt = (
            update(TransactionORM)
            .where(TransactionORM.transaction_id == transaction.transaction_id)
            .values(
                account_id=transaction.account_id,
                category_id=transaction.category_id,
                type=transaction.type,
                amount=transaction.amount,
                description=transaction.description,
                date=transaction.date,
                updated_at=transaction.updated_at,
            )
        )
        await self.__session.execute(stmt)

    async def delete(self, transaction_id: str) -> None:
        stmt = delete(TransactionORM).where(TransactionORM.transaction_id == transaction_id)
        await self.__session.execute(stmt)
