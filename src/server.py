from __future__ import annotations

from fastapi import FastAPI

from src.modules.accounts.api.http import router as accounts_router
from src.modules.budgets.api.http import budgets_router
from src.modules.categories.api.http import router as categories_router
from src.modules.identity.api.http import router as identity_router
from src.modules.transactions.api.http import router as transactions_router

app = FastAPI()

app.include_router(identity_router, prefix="/identity", tags=["identity"])
app.include_router(categories_router, prefix="/categories", tags=["categories"])
app.include_router(accounts_router, prefix="/accounts", tags=["accounts"])
app.include_router(transactions_router, prefix="/transactions", tags=["transactions"])
app.include_router(budgets_router, prefix="/budgets", tags=["budgets"])
