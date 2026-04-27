from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from sqlalchemy import select

from src.libs.database import async_session_maker, get_session_context
from src.modules.categories.domain.entities import CategoryExpenseReadModel
from src.modules.categories.infrastructure.sqlalchemy.category_expense_repository import (
    SqlAlchemyCategoryExpenseRepository,
)
from src.modules.categories.infrastructure.sqlalchemy.orm_models import CategoryORM
from src.modules.transactions.domain.entities import DashboardStatisticsReadModel
from src.modules.transactions.infrastructure.sqlalchemy.statistics_repositories import (
    SqlAlchemyDashboardStatisticsRepository,
)

if TYPE_CHECKING:
    from src.modules.transactions.domain.events import (
        TransactionCreatedEvent,
        TransactionDeletedEvent,
        TransactionUpdatedEvent,
    )

logger = logging.getLogger(__name__)


async def handle_transaction_created(event: TransactionCreatedEvent) -> None:
    async with get_session_context(async_session_maker) as session:
        # Create repositories
        dashboard_repo = SqlAlchemyDashboardStatisticsRepository(session)
        category_repo = SqlAlchemyCategoryExpenseRepository(session)

        # Update dashboard statistics
        dashboard_stats = await dashboard_repo.get_by_user_id(event.user_id)

        if not dashboard_stats:
            dashboard_stats = DashboardStatisticsReadModel.create(event.user_id)

        dashboard_stats.apply_transaction(event.transaction_type, event.amount)
        await dashboard_repo.save(dashboard_stats)

        # Update category expenses if it's an expense with category
        if event.transaction_type.lower() == "expense" and event.category_id:
            category_expense = await category_repo.get_by_user_and_category(
                event.user_id,
                event.category_id,
            )

            if not category_expense:
                # Need to fetch category name
                result = await session.execute(
                    select(CategoryORM).where(
                        CategoryORM.category_id == event.category_id,
                    ),
                )
                category_orm = result.scalar_one_or_none()
                category_name = category_orm.name if category_orm else "Unknown"

                category_expense = CategoryExpenseReadModel.create(
                    event.user_id,
                    event.category_id,
                    category_name,
                )

            category_expense.apply_transaction(event.amount)
            await category_repo.save(category_expense)

        await session.commit()
        logger.info(
            "Updated statistics for transaction %s",
            event.transaction_id,
        )


async def handle_transaction_updated(event: TransactionUpdatedEvent) -> None:
    """Update statistics when a transaction is updated."""
    async with get_session_context(async_session_maker) as session:
        # Create repositories
        dashboard_repo = SqlAlchemyDashboardStatisticsRepository(session)
        category_repo = SqlAlchemyCategoryExpenseRepository(session)

        # Update dashboard statistics
        dashboard_stats = await dashboard_repo.get_by_user_id(event.user_id)

        if dashboard_stats:
            dashboard_stats.update_transaction(
                event.old_transaction_type,
                event.transaction_type,
                event.old_amount,
                event.amount,
            )
            await dashboard_repo.save(dashboard_stats)

        # Update category expenses
        # Handle old category
        if event.old_transaction_type.lower() == "expense" and event.old_category_id:
            old_category_expense = await category_repo.get_by_user_and_category(
                event.user_id,
                event.old_category_id,
            )
            if old_category_expense:
                old_category_expense.reverse_transaction(event.old_amount)
                await category_repo.save(old_category_expense)

        # Handle new category
        if event.transaction_type.lower() == "expense" and event.category_id:
            new_category_expense = await category_repo.get_by_user_and_category(
                event.user_id,
                event.category_id,
            )

            if not new_category_expense:
                result = await session.execute(
                    select(CategoryORM).where(
                        CategoryORM.category_id == event.category_id,
                    ),
                )
                category_orm = result.scalar_one_or_none()
                category_name = category_orm.name if category_orm else "Unknown"

                new_category_expense = CategoryExpenseReadModel.create(
                    event.user_id,
                    event.category_id,
                    category_name,
                )

            new_category_expense.apply_transaction(event.amount)
            await category_repo.save(new_category_expense)

        await session.commit()
        logger.info(
            "Updated statistics after transaction %s update",
            event.transaction_id,
        )


async def handle_transaction_deleted(event: TransactionDeletedEvent) -> None:
    """Update statistics when a transaction is deleted."""
    async with get_session_context(async_session_maker) as session:
        dashboard_repo = SqlAlchemyDashboardStatisticsRepository(session)
        category_repo = SqlAlchemyCategoryExpenseRepository(session)

        dashboard_stats = await dashboard_repo.get_by_user_id(event.user_id)

        if dashboard_stats:
            dashboard_stats.reverse_transaction(event.transaction_type, event.amount)
            await dashboard_repo.save(dashboard_stats)

        if event.transaction_type.lower() == "expense" and event.category_id:
            category_expense = await category_repo.get_by_user_and_category(
                event.user_id,
                event.category_id,
            )

            if category_expense:
                category_expense.reverse_transaction(event.amount)
                await category_repo.save(category_expense)

        await session.commit()
        logger.info(
            "Reversed statistics for deleted transaction %s",
            event.transaction_id,
        )

