"""empty message

Revision ID: cc2134ca90f7
Revises: a1b2c3d4e5f6
Create Date: 2025-12-21 01:24:41.426745
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op

if TYPE_CHECKING:
    from collections.abc import Sequence

revision: str = "cc2134ca90f7"
down_revision: str | Sequence[str] | None = "a1b2c3d4e5f6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "category_expenses",
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("category_id", sa.String(), nullable=False),
        sa.Column("category_name", sa.String(length=100), nullable=False),
        sa.Column("total_amount", sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column("transaction_count", sa.Integer(), nullable=False),
        sa.Column("last_updated", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("user_id", "category_id"),
        schema="categories",
    )
    op.create_table(
        "dashboard_statistics",
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("total_income", sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column("total_expense", sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column("last_updated", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("user_id"),
        schema="transactions",
    )


def downgrade() -> None:
    op.drop_table("dashboard_statistics", schema="transactions")
    op.drop_table("category_expenses", schema="categories")
