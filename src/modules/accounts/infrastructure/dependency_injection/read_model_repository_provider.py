from __future__ import annotations

from src.libs.database import async_session_maker
from src.modules.accounts.application.interfaces.read_model_repository import (
    IAccountReadModelRepository,
)
from src.modules.accounts.infrastructure.sqlalchemy.read_model_repository import (
    SqlAlchemyAccountReadModelRepository,
)


async def get_account_read_model_repository() -> IAccountReadModelRepository:
    async with async_session_maker() as session:
        return SqlAlchemyAccountReadModelRepository(session)
