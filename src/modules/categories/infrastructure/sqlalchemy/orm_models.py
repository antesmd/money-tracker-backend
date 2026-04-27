from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TypedDict, Unpack

from sqlalchemy import DateTime, ForeignKey, Integer, MetaData, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.libs.utils import DateTimeUtils


class Base(DeclarativeBase):
    metadata = MetaData(schema="categories")


class CategoryORMConstructorFields(TypedDict):
    category_id: str
    user_id: str
    name: str
    created_at: datetime
    updated_at: datetime


class CategoryORM(Base):
    __tablename__ = "categories"

    def __init__(self, **kwargs: Unpack[CategoryORMConstructorFields]) -> None:
        super().__init__(**kwargs)

    category_id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
    )
    user_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=DateTimeUtils.utc_now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=DateTimeUtils.utc_now,
        onupdate=DateTimeUtils.utc_now,
    )


class CategoryExpenseORMConstructorFields(TypedDict):
    user_id: str
    category_id: str
    category_name: str
    total_amount: Decimal
    transaction_count: int
    last_updated: datetime


class CategoryExpenseORM(Base):
    __tablename__ = "category_expenses"

    def __init__(self, **kwargs: Unpack[CategoryExpenseORMConstructorFields]) -> None:
        super().__init__(**kwargs)

    user_id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        index=True,
    )
    category_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("categories.category_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
    category_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=15, scale=2),
        nullable=False,
        default=0,
    )
    transaction_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    last_updated: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )
