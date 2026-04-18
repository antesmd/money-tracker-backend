from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from src.modules.categories.domain.entities import TransactionType


class CreateCategoryRequest(BaseModel):
    name: str
    type: TransactionType


class UpdateCategoryRequest(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    category_id: str
    user_id: str
    name: str
    type: TransactionType
    created_at: datetime
    updated_at: datetime
