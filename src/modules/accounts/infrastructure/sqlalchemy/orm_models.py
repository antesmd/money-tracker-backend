from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TypedDict, Unpack

from sqlalchemy import DateTime, Enum, MetaData, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.modules.accounts.domain.entities import AccountType


class Base(DeclarativeBase):
    metadata = MetaData(schema="accounts")


class AccountORMConstructorFields(TypedDict):
    account_id: str
    user_id: str
    name: str
    account_type: AccountType
    balance: Decimal
    created_at: datetime
    updated_at: datetime


class AccountORM(Base):
    __tablename__ = "accounts"

    def __init__(self, **kwargs: Unpack[AccountORMConstructorFields]) -> None:
        super().__init__(**kwargs)

    account_id: Mapped[str] = mapped_column(
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
    account_type: Mapped[AccountType] = mapped_column(
        Enum(AccountType, native_enum=False),
        nullable=False,
    )
    balance: Mapped[Decimal] = mapped_column(
        Numeric(precision=15, scale=2),
        nullable=False,
        default=0,
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
