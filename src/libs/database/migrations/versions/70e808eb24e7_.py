"""empty message

Revision ID: 70e808eb24e7
Revises: cc2134ca90f7
Create Date: 2025-12-22 16:24:09.942390
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from alembic import op

if TYPE_CHECKING:
    from collections.abc import Sequence

revision: str = "70e808eb24e7"
down_revision: str | Sequence[str] | None = "cc2134ca90f7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_foreign_key(
        "fk_category_expenses_category_id",
        "category_expenses",
        "categories",
        ["category_id"],
        ["category_id"],
        source_schema="categories",
        referent_schema="categories",
        onupdate="CASCADE",
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_category_expenses_category_id",
        "category_expenses",
        schema="categories",
        type_="foreignkey",
    )
