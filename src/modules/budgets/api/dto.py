from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class CreateBudgetRequest(BaseModel):
    category_id: str = Field(description="ID категории для бюджета")
    amount: Decimal = Field(ge=0, description="Сумма бюджета")
    period_start: datetime = Field(description="Начало периода")
    period_end: datetime = Field(description="Конец периода")


class UpdateBudgetRequest(BaseModel):
    amount: Decimal | None = Field(None, ge=0, description="Новая сумма бюджета")
    period_start: datetime | None = Field(None, description="Новое начало периода")
    period_end: datetime | None = Field(None, description="Новый конец периода")


class BudgetResponse(BaseModel):
    budget_id: str
    user_id: str
    category_id: str
    amount: Decimal
    period_start: datetime
    period_end: datetime
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BudgetReadModelResponse(BaseModel):
    budget_id: str
    user_id: str
    category_id: str
    amount: Decimal
    spent: Decimal
    remaining: Decimal
    transaction_count: int
    period_start: datetime
    period_end: datetime
    last_updated: datetime

    class Config:
        from_attributes = True
