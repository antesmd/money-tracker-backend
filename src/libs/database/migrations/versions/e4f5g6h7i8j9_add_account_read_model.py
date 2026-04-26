"""Add account_read_model table for CQRS

Revision ID: e4f5g6h7i8j9
Revises: c3d4e5f6g7h8
Create Date: 2025-12-20 15:00:00.000000
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op

if TYPE_CHECKING:
    from collections.abc import Sequence

revision: str = "e4f5g6h7i8j9"
down_revision: str | Sequence[str] | None = "c3d4e5f6g7h8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "account_read_model",
        sa.Column("account_id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("account_type", sa.String(), nullable=False),
        sa.Column("balance", sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column("total_inflow", sa.Numeric(precision=15, scale=2), nullable=False, server_default="0"),
        sa.Column("total_outflow", sa.Numeric(precision=15, scale=2), nullable=False, server_default="0"),
        sa.Column("transaction_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_updated", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("account_id"),
        schema="accounts",
    )


def downgrade() -> None:
    op.drop_table("account_read_model", schema="accounts")
