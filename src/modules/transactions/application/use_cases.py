from __future__ import annotations

from typing import TYPE_CHECKING

from src.modules.transactions.application import handlers

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
    from src.modules.transactions.domain.entities import Transaction


async def create_transaction_use_case(
    command: CreateTransactionCommand,
    unit_of_work: ITransactionsUnitOfWork,
) -> Transaction:
    return await handlers.handle_create_transaction(command, unit_of_work)


async def update_transaction_use_case(
    command: UpdateTransactionCommand,
    unit_of_work: ITransactionsUnitOfWork,
) -> Transaction:
    return await handlers.handle_update_transaction(command, unit_of_work)


async def delete_transaction_use_case(
    command: DeleteTransactionCommand,
    unit_of_work: ITransactionsUnitOfWork,
) -> None:
    await handlers.handle_delete_transaction(command, unit_of_work)


async def get_user_transactions_use_case(
    command: GetUserTransactionsCommand,
    unit_of_work: ITransactionsUnitOfWork,
) -> list[Transaction]:
    return await handlers.handle_get_user_transactions(command, unit_of_work)


async def get_account_transactions_use_case(
    command: GetAccountTransactionsCommand,
    unit_of_work: ITransactionsUnitOfWork,
) -> list[Transaction]:
    return await handlers.handle_get_account_transactions(command, unit_of_work)


async def get_transactions_by_date_range_use_case(
    command: GetTransactionsByDateRangeCommand,
    unit_of_work: ITransactionsUnitOfWork,
) -> list[Transaction]:
    return await handlers.handle_get_transactions_by_date_range(command, unit_of_work)
