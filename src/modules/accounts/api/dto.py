from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from src.modules.accounts.domain.entities import AccountType


class CreateAccountRequest(BaseModel):
    name: str
    account_type: AccountType
    initial_balance: Decimal = Field(
        default=Decimal("0.0"),
        decimal_places=2,
        max_digits=10,
        ge=Decimal("0.0"),
        le=Decimal("1000000.0"),
    )


class UpdateAccountRequest(BaseModel):
    name: str
    account_type: AccountType


class AccountResponse(BaseModel):
    account_id: str
    user_id: str
    name: str
    account_type: AccountType
    created_at: datetime
    updated_at: datetime


class AccountReadModelResponse(BaseModel):
    account_id: str
    user_id: str
    name: str
    account_type: AccountType
    balance: Decimal
    total_inflow: Decimal
    total_outflow: Decimal
    transaction_count: int
    last_updated: datetime
