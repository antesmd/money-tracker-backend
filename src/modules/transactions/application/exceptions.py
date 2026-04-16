from __future__ import annotations


class BaseTransactionsError(Exception):
    pass


class TransactionNotFoundError(BaseTransactionsError):
    def __init__(self) -> None:
        super().__init__("Transaction not found.")
