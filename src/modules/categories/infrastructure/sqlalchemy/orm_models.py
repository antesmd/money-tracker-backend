from __future__ import annotations

from datetime import datetime
from typing import TypedDict, Unpack

from sqlalchemy import DateTime, Enum, MetaData, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.modules.categories.domain.entities import TransactionType
from src.libs.utils import DateTimeUtils


class Base(DeclarativeBase):
    metadata = MetaData(schema="categories")


class CategoryORMConstructorFields(TypedDict):
    category_id: str
    user_id: str
    name: str
    type: TransactionType
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
    type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType, native_enum=False),
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
