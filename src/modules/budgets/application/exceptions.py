from __future__ import annotations


class BudgetNotFoundError(Exception):
    def __init__(self, budget_id: str) -> None:
        self.budget_id = budget_id
        super().__init__(f"Budget with id {budget_id} not found")


class UnauthorizedBudgetAccessError(Exception):
    def __init__(self, budget_id: str) -> None:
        self.budget_id = budget_id
        super().__init__(f"Unauthorized access to budget {budget_id}")
