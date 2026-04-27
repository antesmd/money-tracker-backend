from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class CreateCategoryRequest(BaseModel):
    name: str


class UpdateCategoryRequest(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    category_id: str
    user_id: str
    name: str
    created_at: datetime
    updated_at: datetime


class CategoryExpenseResponse(BaseModel):
    category_id: str
    category_name: str
    amount: Decimal
    transaction_count: int
    last_updated: datetime
