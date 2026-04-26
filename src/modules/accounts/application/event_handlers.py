from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from src.libs.database import async_session_maker, get_session_context
from src.libs.utils import DateTimeUtils
from src.modules.accounts.domain.entities import AccountReadModel
from src.modules.accounts.infrastructure.sqlalchemy.read_model_repository import (
    SqlAlchemyAccountReadModelRepository,
)

if TYPE_CHECKING:
    from src.modules.accounts.domain.entities import Account
    from src.modules.transactions.domain.events import (
        TransactionCreatedEvent,
        TransactionDeletedEvent,
        TransactionUpdatedEvent,
    )

logger = logging.getLogger(__name__)


async def handle_account_created(account: Account) -> None:
    async with get_session_context(async_session_maker) as session:
        repository = SqlAlchemyAccountReadModelRepository(session)
        read_model = AccountReadModel.from_account(account)
        await repository.save(read_model)
        await session.commit()


async def handle_account_updated(account: Account) -> None:
    async with get_session_context(async_session_maker) as session:
        repository = SqlAlchemyAccountReadModelRepository(session)
        read_model = await repository.get_by_id(account.account_id)
        if read_model:
            read_model.update_account(account.name, account.account_type, account.balance)
            await repository.save(read_model)
            await session.commit()


async def handle_account_deleted(account_id: str) -> None:
    async with get_session_context(async_session_maker) as session:
        repository = SqlAlchemyAccountReadModelRepository(session)
        await repository.delete(account_id)
        await session.commit()


async def handle_transaction_created(event: TransactionCreatedEvent) -> None:
    async with get_session_context(async_session_maker) as session:
        repository = SqlAlchemyAccountReadModelRepository(session)
        read_model = await repository.get_by_id(event.account_id)
        if not read_model:
            logger.warning(
                "Account read model not found for transaction",
                extra={"account_id": event.account_id},
            )
            return

        read_model.apply_transaction(event.transaction_type, event.amount)
        await repository.save(read_model)
        await session.commit()


async def handle_transaction_updated(event: TransactionUpdatedEvent) -> None:
    async with get_session_context(async_session_maker) as session:
        repository = SqlAlchemyAccountReadModelRepository(session)
        read_model = await repository.get_by_id(event.account_id)
        if not read_model:
            logger.warning(
                "Account read model not found for transaction update",
                extra={"account_id": event.account_id},
            )
            return

        diff = event.amount - event.old_amount
        tx_type = (
            event.transaction_type.value
            if hasattr(event.transaction_type, "value")
            else str(event.transaction_type)
        )
        if tx_type == "income":
            read_model.balance += diff
            read_model.total_inflow += diff
        else:
            read_model.balance -= diff
            read_model.total_outflow += diff

        read_model.last_updated = DateTimeUtils.utc_now()
        await repository.save(read_model)
        await session.commit()


async def handle_transaction_deleted(event: TransactionDeletedEvent) -> None:
    async with get_session_context(async_session_maker) as session:
        repository = SqlAlchemyAccountReadModelRepository(session)
        read_model = await repository.get_by_id(event.account_id)
        if not read_model:
            logger.warning(
                "Account read model not found for transaction delete",
                extra={"account_id": event.account_id},
            )
            return

        read_model.reverse_transaction(event.transaction_type, event.amount)
        await repository.save(read_model)
        await session.commit()
