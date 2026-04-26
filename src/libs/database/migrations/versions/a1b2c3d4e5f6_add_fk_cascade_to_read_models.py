"""add fk cascade to read models

Revision ID: a1b2c3d4e5f6
Revises: c3d4e5f6g7h8
Create Date: 2025-12-20
"""
from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from alembic import op

if TYPE_CHECKING:
    from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: str | Sequence[str] | None = "e4f5g6h7i8j9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_foreign_key(
        "fk_account_read_model_account_id_accounts",
        "account_read_model",
        "accounts",
        ["account_id"],
        ["account_id"],
        source_schema="accounts",
        referent_schema="accounts",
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_budget_read_model_budget_id_budgets",
        "budget_read_model",
        "budgets",
        ["budget_id"],
        ["budget_id"],
        source_schema="budgets",
        referent_schema="budgets",
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_account_read_model_account_id_accounts",
        "account_read_model",
        type_="foreignkey",
        schema="accounts",
    )
    op.drop_constraint(
        "fk_budget_read_model_budget_id_budgets",
        "budget_read_model",
        type_="foreignkey",
        schema="budgets",
    )
