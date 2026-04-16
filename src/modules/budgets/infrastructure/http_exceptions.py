from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import HTTPException, status

if TYPE_CHECKING:
    from ..application.exceptions import BudgetNotFoundError, UnauthorizedBudgetAccessError


def handle_budget_not_found(error: BudgetNotFoundError) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Budget with id {error.budget_id} not found",
    )


def handle_unauthorized_budget_access(
    error: UnauthorizedBudgetAccessError,
) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"You don't have access to budget {error.budget_id}",
    )
