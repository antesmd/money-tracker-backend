from __future__ import annotations

from typing import TYPE_CHECKING

from src.modules.identity.application.handlers import (
    handle_authenticate_user,
    handle_create_user,
    handle_list_users,
    handle_refresh_token,
)

if TYPE_CHECKING:
    from src.modules.identity.application.commands import (
        AuthenticateUserCommand,
        CreateUserCommand,
        RefreshTokenCommand,
    )
    from src.modules.identity.application.interfaces.unit_of_work import IIdentityUnitOfWork
    from src.modules.identity.domain.entities import User
    from src.modules.identity.infrastructure.token_service import TokenService


async def create_user_use_case(
    command: CreateUserCommand,
    unit_of_work: IIdentityUnitOfWork,
) -> User:
    return await handle_create_user(command, unit_of_work=unit_of_work)


async def user_login_use_case(
    command: AuthenticateUserCommand,
    unit_of_work: IIdentityUnitOfWork,
    token_service: TokenService,
) -> tuple[str, str]:
    return await handle_authenticate_user(
        command,
        unit_of_work=unit_of_work,
        token_service=token_service,
    )


async def list_users_use_case(unit_of_work: IIdentityUnitOfWork) -> list[User]:
    return await handle_list_users(unit_of_work)


async def refresh_token_use_case(
    command: RefreshTokenCommand,
    unit_of_work: IIdentityUnitOfWork,
    token_service: TokenService,
) -> tuple[str, str]:
    return await handle_refresh_token(
        command,
        unit_of_work=unit_of_work,
        token_service=token_service,
    )
