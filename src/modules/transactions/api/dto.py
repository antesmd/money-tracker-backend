from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, NaiveDatetime

from src.modules.transactions.domain.entities import TransactionType


class CreateTransactionRequest(BaseModel):
    account_id: str
    category_id: str | None = None
    transaction_type: TransactionType
    amount: Decimal = Field(
        gt=Decimal("0.0"),
        le=Decimal("1000000.0"),
        decimal_places=2,
        max_digits=10,
    )
    description: str | None = None
    date: NaiveDatetime | None = None


class UpdateTransactionRequest(BaseModel):
    account_id: str
    category_id: str | None = None
    transaction_type: TransactionType
    amount: Decimal = Field(
        gt=Decimal("0.0"),
        le=Decimal("1000000.0"),
        decimal_places=2,
        max_digits=10,
    )
    description: str | None = None
    date: NaiveDatetime | None = None


class TransactionResponse(BaseModel):
    transaction_id: str
    user_id: str
    account_id: str
    category_id: str | None
    transaction_type: TransactionType
    amount: Decimal = Field(
        gt=Decimal("0.0"),
        le=Decimal("1000000.0"),
        decimal_places=2,
        max_digits=10,
    )
    description: str | None
    date: datetime
    created_at: datetime
    updated_at: datetime


class TransactionTypeDistribution(BaseModel):
    income: Decimal = Field(decimal_places=2, max_digits=10)
    expense: Decimal = Field(decimal_places=2, max_digits=10)


class DashboardStatisticsResponse(BaseModel):
    transaction_distribution: TransactionTypeDistribution
