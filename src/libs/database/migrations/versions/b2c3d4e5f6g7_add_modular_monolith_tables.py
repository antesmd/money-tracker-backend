"""Add categories, accounts, transactions tables

Revision ID: b2c3d4e5f6g7
Revises: d9ed51eb70b3
Create Date: 2025-12-08 12:00:00.000000
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op

if TYPE_CHECKING:
    from collections.abc import Sequence

revision: str = "b2c3d4e5f6g7"
down_revision: str | Sequence[str] | None = "d9ed51eb70b3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS categories;")
    op.create_table(
        "categories",
        sa.Column("category_id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("category_id"),
        schema="categories",
    )

    op.execute("CREATE SCHEMA IF NOT EXISTS accounts;")
    op.create_table(
        "accounts",
        sa.Column("account_id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("account_type", sa.String(), nullable=False),
        sa.Column("balance", sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("account_id"),
        schema="accounts",
    )

    op.execute("CREATE SCHEMA IF NOT EXISTS transactions;")
    op.create_table(
        "transactions",
        sa.Column("transaction_id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("account_id", sa.String(), nullable=False),
        sa.Column("category_id", sa.String(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("amount", sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("transaction_id"),
        schema="transactions",
    )

    op.execute("CREATE SCHEMA IF NOT EXISTS budgets;")
    op.create_table(
        "budgets",
        sa.Column("budget_id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("category_id", sa.String(), nullable=False),
        sa.Column("amount", sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column("period_start", sa.DateTime(), nullable=False),
        sa.Column("period_end", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("budget_id"),
        schema="budgets",
    )


def downgrade() -> None:
    op.drop_table("budgets", schema="budgets")
    op.execute("DROP SCHEMA IF EXISTS budgets CASCADE;")

    op.drop_table("transactions", schema="transactions")
    op.execute("DROP SCHEMA IF EXISTS transactions CASCADE;")

    op.drop_table("accounts", schema="accounts")
    op.execute("DROP SCHEMA IF EXISTS accounts CASCADE;")

    op.drop_table("categories", schema="categories")
    op.execute("DROP SCHEMA IF EXISTS categories CASCADE;")
