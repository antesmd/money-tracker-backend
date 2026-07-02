from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from src.libs.database import async_session_maker, get_session_context
from src.modules.budgets.domain.entities import BudgetReadModel
from src.modules.budgets.infrastructure.sqlalchemy.read_model_repository import (
    SqlAlchemyBudgetReadModelRepository,
)

if TYPE_CHECKING:
    from src.modules.budgets.domain.entities import Budget
    from src.modules.transactions.domain.events import (
        TransactionCreatedEvent,
        TransactionDeletedEvent,
        TransactionUpdatedEvent,
    )

logger = logging.getLogger(__name__)


async def handle_budget_created(budget: Budget) -> None:
    async with get_session_context(async_session_maker) as session:
        repository = SqlAlchemyBudgetReadModelRepository(session)
        read_model = BudgetReadModel.from_budget(budget)

        await repository.save(read_model)
        await session.commit()


async def handle_transaction_created(event: TransactionCreatedEvent) -> None:
    if event.transaction_type != "expense" or event.category_id is None:
        return

    async with get_session_context(async_session_maker) as session:
        repository = SqlAlchemyBudgetReadModelRepository(session)

        read_model = await repository.get_by_category_and_date(
            category_id=event.category_id,
            user_id=event.user_id,
            date=event.date,
        )

        if read_model:
            read_model.apply_transaction(event.amount)
            await repository.save(read_model)
            await session.commit()

            logger.info(
                f"Updated read model for budget {read_model.budget_id} "
                f"after transaction {event.transaction_id}",
            )

async def handle_transaction_updated(event: TransactionUpdatedEvent) -> None:
    if event.transaction_type != "expense" or event.category_id is None:
        return

    async with get_session_context(async_session_maker) as session:
        repository = SqlAlchemyBudgetReadModelRepository(session)

        if event.old_category_id != event.category_id:
            if event.old_category_id is not None:
                old_read_model = await repository.get_by_category_and_date(
                    category_id=event.old_category_id,
                    user_id=event.user_id,
                    date=event.date,
                )
                if old_read_model:
                    old_read_model.reverse_transaction(event.old_amount)
                    await repository.save(old_read_model)

            new_read_model = await repository.get_by_category_and_date(
                category_id=event.category_id,
                user_id=event.user_id,
                date=event.date,
            )
            if new_read_model:
                new_read_model.apply_transaction(event.amount)
                await repository.save(new_read_model)
        else:
            read_model = await repository.get_by_category_and_date(
                category_id=event.category_id,
                user_id=event.user_id,
                date=event.date,
            )
            if read_model:
                diff = event.amount - event.old_amount
                read_model.spent += diff
                read_model.remaining = read_model.amount - read_model.spent
                await repository.save(read_model)

        await session.commit()
        logger.info(f"Updated read model after transaction {event.transaction_id} update")


async def handle_transaction_deleted(event: TransactionDeletedEvent) -> None:
    if event.transaction_type != "expense" or event.category_id is None:
        return

    async with get_session_context(async_session_maker) as session:
        repository = SqlAlchemyBudgetReadModelRepository(session)

        read_model = await repository.get_by_category_and_date(
            category_id=event.category_id,
            user_id=event.user_id,
            date=event.date,
        )

        if read_model:
            read_model.reverse_transaction(event.amount)
            await repository.save(read_model)
            await session.commit()

            logger.info(
                f"Reversed transaction {event.transaction_id} "
                f"from read model {read_model.budget_id}",
            )

async def handle_budget_updated(budget: Budget) -> None:
    async with get_session_context(async_session_maker) as session:
        repository = SqlAlchemyBudgetReadModelRepository(session)

        read_model = await repository.get_by_id(budget.budget_id)
        if read_model:
            read_model.update_amount(budget.amount)
            await repository.save(read_model)
            await session.commit()

            logger.info(f"Updated read model for budget {budget.budget_id}")


async def handle_budget_deleted(budget_id: str) -> None:
    async with get_session_context(async_session_maker) as session:
        repository = SqlAlchemyBudgetReadModelRepository(session)

        await repository.delete(budget_id)
        await session.commit()

        logger.info(f"Deleted read model for budget {budget_id}")
