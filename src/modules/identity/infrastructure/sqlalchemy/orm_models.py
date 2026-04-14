from __future__ import annotations

from datetime import datetime
from typing import TypedDict, Unpack

from sqlalchemy import DateTime, MetaData, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    metadata = MetaData(schema="identity")


class UserORMConstructorFields(TypedDict):
    user_id: str
    email: str
    username: str
    hashed_password: str
    created_at: datetime


class UserORM(Base):
    __tablename__ = "users"

    def __init__(self, **kwargs: Unpack[UserORMConstructorFields]) -> None:
        super().__init__(**kwargs)

    user_id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
    )
    email: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )
    username: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )
