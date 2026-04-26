from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, NaiveDatetime

from src.modules.transactions.domain.entities import TransactionType


class CreateTransactionRequest(BaseModel):
    account_id: str
    category_id: str
    transaction_type: TransactionType
    amount: Decimal
    description: str | None = None
    date: NaiveDatetime | None = None


class UpdateTransactionRequest(BaseModel):
    account_id: str
    category_id: str
    transaction_type: TransactionType
    amount: Decimal
    description: str | None = None
    date: NaiveDatetime | None = None


class TransactionResponse(BaseModel):
    transaction_id: str
    user_id: str
    account_id: str
    category_id: str
    transaction_type: TransactionType
    amount: Decimal
    description: str | None
    date: datetime
    created_at: datetime
    updated_at: datetime
