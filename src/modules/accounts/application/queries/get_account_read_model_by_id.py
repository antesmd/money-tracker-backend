from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.accounts.application.interfaces import (
        IAccountReadModelRepository,
    )
    from src.modules.accounts.domain.entities import AccountReadModel


@dataclass
class GetAccountReadModelByIdQuery:
    account_id: str


async def handle_get_account_read_model_by_id(
    query: GetAccountReadModelByIdQuery,
    repository: IAccountReadModelRepository,
) -> AccountReadModel | None:
    return await repository.get_by_id(query.account_id)
