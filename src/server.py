from __future__ import annotations

from fastapi import FastAPI

from src.libs.message_bus import global_message_bus
from src.modules.accounts.api.http import router as accounts_router
from src.modules.budgets.api.http import budgets_router
from src.modules.budgets.application.event_handlers import (
    handle_transaction_created,
    handle_transaction_deleted,
    handle_transaction_updated,
)
from src.modules.categories.api.http import router as categories_router
from src.modules.identity.api.http import router as identity_router
from src.modules.transactions.api.http import router as transactions_router
from src.modules.transactions.domain.events import (
    TransactionCreatedEvent,
    TransactionDeletedEvent,
    TransactionUpdatedEvent,
)

app = FastAPI()

message_bus = global_message_bus

message_bus.register(TransactionCreatedEvent, handle_transaction_created)
message_bus.register(TransactionUpdatedEvent, handle_transaction_updated)
message_bus.register(TransactionDeletedEvent, handle_transaction_deleted)

app.include_router(identity_router, prefix="/identity", tags=["identity"])
app.include_router(categories_router, prefix="/categories", tags=["categories"])
app.include_router(accounts_router, prefix="/accounts", tags=["accounts"])
app.include_router(transactions_router, prefix="/transactions", tags=["transactions"])
app.include_router(budgets_router, prefix="/budgets", tags=["budgets"])
