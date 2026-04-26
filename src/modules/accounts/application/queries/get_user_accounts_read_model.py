from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.accounts.application.interfaces.read_model_repository import (
        IAccountReadModelRepository,
    )
    from src.modules.accounts.domain.entities import AccountReadModel


@dataclass
class GetUserAccountsReadModelQuery:
    user_id: str
    skip: int = 0
    limit: int = 100


async def handle_get_user_accounts_read_model(
    query: GetUserAccountsReadModelQuery,
    repository: IAccountReadModelRepository,
) -> list[AccountReadModel]:
    return await repository.get_by_user_id(
        user_id=query.user_id,
        skip=query.skip,
        limit=query.limit,
    )
