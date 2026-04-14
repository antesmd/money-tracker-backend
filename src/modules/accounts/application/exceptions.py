from __future__ import annotations


class BaseAccountsError(Exception):
    pass


class AccountNotFoundError(BaseAccountsError):
    def __init__(self) -> None:
        super().__init__("Account not found.")
