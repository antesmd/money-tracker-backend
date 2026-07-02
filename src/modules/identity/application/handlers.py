from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import uuid4

from src.libs.utils.hashing import hash_with_bcrypt, verify_bcrypt_hash
from src.modules.identity.application.commands import (
    AuthenticateUserCommand,
    CreateUserCommand,
    RefreshTokenCommand,
)
from src.modules.identity.application.exceptions import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
)
from src.modules.identity.application.interfaces.unit_of_work import IIdentityUnitOfWork
from src.modules.identity.domain.entities import User

if TYPE_CHECKING:
    from src.modules.identity.application.interfaces.unit_of_work import IIdentityUnitOfWork
    from src.modules.identity.infrastructure.token_service import TokenService

    from .commands import AuthenticateUserCommand, CreateUserCommand, RefreshTokenCommand



async def handle_create_user(
    command: CreateUserCommand,
    unit_of_work: IIdentityUnitOfWork,
) -> User:
    if await unit_of_work.users.get_by_email(command.email):
        raise EmailAlreadyExistsError

    user = User(
        user_id=str(uuid4()),
        username=command.username,
        email=command.email,
        hashed_password=hash_with_bcrypt(command.password),
    )
    unit_of_work.users.add(user)
    await unit_of_work.commit()

    return user


async def handle_authenticate_user(
    command: AuthenticateUserCommand,
    unit_of_work: IIdentityUnitOfWork,
    token_service: TokenService,
) -> tuple[str, str]:
    user = await unit_of_work.users.get_by_email(command.email)
    if not user or not verify_bcrypt_hash(command.password, user.hashed_password):
        raise InvalidCredentialsError

    access_token = token_service.create_access_token(
        payload={"user_id": user.user_id, "role": user.role.value},
    )
    refresh_token = token_service.create_refresh_token(
        payload={"user_id": user.user_id, "role": user.role.value},
    )

    return access_token, refresh_token


async def handle_list_users(unit_of_work: IIdentityUnitOfWork) -> list[User]:
    return await unit_of_work.users.list_all()


async def handle_refresh_token(
    command: RefreshTokenCommand,
    unit_of_work: IIdentityUnitOfWork,
    token_service: TokenService,
) -> tuple[str, str]:
    payload = token_service.decode_token(command.refresh_token)
    if payload is None:
        raise InvalidCredentialsError

    user_id = payload["user_id"]
    user = await unit_of_work.users.get_by_id(user_id)
    if not user:
        raise InvalidCredentialsError

    new_access_token = token_service.create_access_token(
        payload={"user_id": user.user_id, "role": user.role.value},
    )
    new_refresh_token = token_service.create_refresh_token(
        payload={"user_id": user.user_id, "role": user.role.value},
    )

    return new_access_token, new_refresh_token
