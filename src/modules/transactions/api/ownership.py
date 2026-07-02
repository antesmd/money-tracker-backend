from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import HTTPException, status

if TYPE_CHECKING:
    from src.modules.accounts.application.interfaces.unit_of_work import IAccountsUnitOfWork
    from src.modules.categories.application.interfaces.unit_of_work import ICategoriesUnitOfWork


async def ensure_account_and_category_ownership(
    user_id: str,
    account_id: str,
    category_id: str | None,
    accounts_uow: IAccountsUnitOfWork,
    categories_uow: ICategoriesUnitOfWork,
) -> None:
    account = await accounts_uow.accounts.get_by_id(account_id)
    if account is None or account.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    if category_id is not None:
        category = await categories_uow.categories.get_by_id(category_id)
        if category is None or category.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
