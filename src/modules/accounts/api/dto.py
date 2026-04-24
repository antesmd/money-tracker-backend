from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from src.modules.accounts.domain.entities import AccountType


class CreateAccountRequest(BaseModel):
    name: str
    account_type: AccountType
    balance: Decimal


class UpdateAccountRequest(BaseModel):
    name: str
    account_type: AccountType


class UpdateAccountBalanceRequest(BaseModel):
    balance: Decimal


class AccountResponse(BaseModel):
    account_id: str
    user_id: str
    name: str
    account_type: AccountType
    balance: Decimal
    created_at: datetime
    updated_at: datetime
