from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TypedDict, Unpack

from sqlalchemy import DateTime, Enum, MetaData, Numeric, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.modules.transactions.domain.entities import TransactionType


class Base(DeclarativeBase):
    metadata = MetaData(schema="transactions")


class TransactionORMConstructorFields(TypedDict):
    transaction_id: str
    user_id: str
    account_id: str
    category_id: str
    type: TransactionType
    amount: Decimal
    description: str | None
    date: datetime
    created_at: datetime
    updated_at: datetime


class TransactionORM(Base):
    __tablename__ = "transactions"

    def __init__(self, **kwargs: Unpack[TransactionORMConstructorFields]) -> None:
        super().__init__(**kwargs)

    transaction_id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
    )
    # No FK - weak coupling between domains
    user_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )
    account_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )
    category_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )
    type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType, native_enum=False),
        nullable=False,
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=15, scale=2),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
