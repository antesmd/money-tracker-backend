from __future__ import annotations

from collections.abc import AsyncIterator

from src.libs.database import async_session_maker
from src.modules.accounts.application.interfaces.read_model_repository import (
    IAccountReadModelRepository,
)
from src.modules.accounts.infrastructure.sqlalchemy.read_model_repository import (
    SqlAlchemyAccountReadModelRepository,
)


async def get_account_read_model_repository() -> AsyncIterator[IAccountReadModelRepository]:
    async with async_session_maker() as session:
        repository = SqlAlchemyAccountReadModelRepository(session)
        yield repository
