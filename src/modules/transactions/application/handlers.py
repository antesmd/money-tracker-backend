from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import uuid4

from src.libs.utils import DateTimeUtils
from src.modules.transactions.application.exceptions import TransactionNotFoundError
from src.modules.transactions.domain.entities import Transaction

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


async def handle_create_transaction(
    command: CreateTransactionCommand,
    unit_of_work: ITransactionsUnitOfWork,
) -> Transaction:
    transaction = Transaction(
        transaction_id=str(uuid4()),
        user_id=command.user_id,
        account_id=command.account_id,
        category_id=command.category_id,
        type=command.type,
        amount=command.amount,
        description=command.description,
        date=command.date or DateTimeUtils.utc_now(),
    )
    unit_of_work.transactions.add(transaction)
    await unit_of_work.commit()
    return transaction


async def handle_update_transaction(
    command: UpdateTransactionCommand,
    unit_of_work: ITransactionsUnitOfWork,
) -> Transaction:
    transaction = await unit_of_work.transactions.get_by_id(command.transaction_id)
    if not transaction:
        raise TransactionNotFoundError

    transaction.account_id = command.account_id
    transaction.category_id = command.category_id
    transaction.type = command.type
    transaction.amount = command.amount
    transaction.description = command.description
    transaction.date = command.date or transaction.date
    transaction.updated_at = DateTimeUtils.utc_now()
    await unit_of_work.transactions.update(transaction)
    await unit_of_work.commit()
    return transaction


async def handle_delete_transaction(
    command: DeleteTransactionCommand,
    unit_of_work: ITransactionsUnitOfWork,
) -> None:
    transaction = await unit_of_work.transactions.get_by_id(command.transaction_id)
    if not transaction:
        raise TransactionNotFoundError

    await unit_of_work.transactions.delete(command.transaction_id)
    await unit_of_work.commit()


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
    return await unit_of_work.transactions.get_by_account_id(
        command.account_id,
        limit=command.limit,
        offset=command.offset,
    )


async def handle_get_transactions_by_date_range(
    command: GetTransactionsByDateRangeCommand,
    unit_of_work: ITransactionsUnitOfWork,
) -> list[Transaction]:
    return await unit_of_work.transactions.get_by_date_range(
        command.user_id,
        command.start_date,
        command.end_date,
    )
