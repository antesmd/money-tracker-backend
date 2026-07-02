"""Add role to users

Revision ID: f5a6b7c8d9e0
Revises: 70e808eb24e7
Create Date: 2026-07-02 14:00:00.000000
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op

if TYPE_CHECKING:
    from collections.abc import Sequence

revision: str = "f5a6b7c8d9e0"
down_revision: str | Sequence[str] | None = "70e808eb24e7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("role", sa.String(), nullable=False, server_default="user"),
        schema="identity",
    )


def downgrade() -> None:
    op.drop_column("users", "role", schema="identity")
