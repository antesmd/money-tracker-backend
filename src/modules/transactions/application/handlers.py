from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import uuid4

from src.libs.message_bus import global_message_bus
from src.libs.utils import DateTimeUtils
from src.modules.transactions.application.exceptions import TransactionNotFoundError
from src.modules.transactions.domain.entities import Transaction
from src.modules.transactions.domain.events import (
    TransactionCreatedEvent,
    TransactionDeletedEvent,
    TransactionUpdatedEvent,
)

if TYPE_CHECKING:
    from src.modules.transactions.application.commands import (
        CreateTransactionCommand,
        DeleteTransactionCommand,
        GetAccountTransactionsCommand,
        GetTransactionsByDateRangeCommand,
        GetUserTransactionsCommand,
        UpdateTransactionCommand,
    )
    from src.modules.transactions.application.interfaces.unit_of_work import ITransactionsUnitOfWork

message_bus = global_message_bus


async def handle_create_transaction(
    command: CreateTransactionCommand,
    unit_of_work: ITransactionsUnitOfWork,
) -> Transaction:
    transaction = Transaction(
        transaction_id=str(uuid4()),
        user_id=command.user_id,
        account_id=command.account_id,
        category_id=command.category_id,
        transaction_type=command.transaction_type,
        amount=command.amount,
        description=command.description,
        date=command.date or DateTimeUtils.utc_now(),
    )
    unit_of_work.transactions.add(transaction)
    await unit_of_work.commit()

    event = TransactionCreatedEvent(
        transaction_id=transaction.transaction_id,
        user_id=transaction.user_id,
        account_id=transaction.account_id,
        category_id=transaction.category_id,
        transaction_type=transaction.transaction_type,
        amount=transaction.amount,
        description=transaction.description,
        date=transaction.date,
        created_at=transaction.created_at,
    )
    await message_bus.dispatch(event)

    return transaction


async def handle_update_transaction(
    command: UpdateTransactionCommand,
    unit_of_work: ITransactionsUnitOfWork,
) -> Transaction:
    transaction = await unit_of_work.transactions.get_by_id(command.transaction_id)
    if not transaction or transaction.user_id != command.user_id:
        raise TransactionNotFoundError

    old_category_id = transaction.category_id
    old_amount = transaction.amount
    old_transaction_type = transaction.transaction_type

    transaction.account_id = command.account_id
    transaction.category_id = command.category_id
    transaction.transaction_type = command.transaction_type
    transaction.amount = command.amount
    transaction.description = command.description
    transaction.date = command.date or transaction.date
    transaction.updated_at = DateTimeUtils.utc_now()
    await unit_of_work.transactions.update(transaction)
    await unit_of_work.commit()

    event = TransactionUpdatedEvent(
        transaction_id=transaction.transaction_id,
        user_id=transaction.user_id,
        account_id=transaction.account_id,
        category_id=transaction.category_id,
        transaction_type=transaction.transaction_type,
        amount=transaction.amount,
        description=transaction.description,
        date=transaction.date,
        updated_at=transaction.updated_at,
        old_category_id=old_category_id,
        old_amount=old_amount,
        old_transaction_type=old_transaction_type,
    )
    await message_bus.dispatch(event)

    return transaction


async def handle_delete_transaction(
    command: DeleteTransactionCommand,
    unit_of_work: ITransactionsUnitOfWork,
) -> None:
    transaction = await unit_of_work.transactions.get_by_id(command.transaction_id)
    if not transaction or transaction.user_id != command.user_id:
        raise TransactionNotFoundError

    event = TransactionDeletedEvent(
        transaction.transaction_id,
        transaction.user_id,
        transaction.account_id,
        transaction.category_id,
        transaction.transaction_type,
        transaction.amount,
        transaction.date,
    )

    await unit_of_work.transactions.delete(command.transaction_id)
    await unit_of_work.commit()

    await message_bus.dispatch(event)


async def handle_get_user_transactions(
    command: GetUserTransactionsCommand,
    unit_of_work: ITransactionsUnitOfWork,
) -> list[Transaction]:
    return await unit_of_work.transactions.get_by_user_id(
        command.user_id,
        limit=command.limit,
        offset=command.offset,
    )


async def handle_get_account_transactions(
    command: GetAccountTransactionsCommand,
    unit_of_work: ITransactionsUnitOfWork,
) -> list[Transaction]:
    transactions = await unit_of_work.transactions.get_by_account_id(
        command.account_id,
        limit=command.limit,
        offset=command.offset,
    )
    return [t for t in transactions if t.user_id == command.user_id]


async def handle_get_transactions_by_date_range(
    command: GetTransactionsByDateRangeCommand,
    unit_of_work: ITransactionsUnitOfWork,
) -> list[Transaction]:
    return await unit_of_work.transactions.get_by_date_range(
        command.user_id,
        command.start_date,
        command.end_date,
    )
