from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Response, status

from src.modules.identity.application.commands import (
    AuthenticateUserCommand,
    CreateUserCommand,
    RefreshTokenCommand,
)
from src.modules.identity.application.exceptions import InvalidCredentialsError
from src.modules.identity.application.interfaces.unit_of_work import IIdentityUnitOfWork
from src.modules.identity.application.use_cases import (
    create_user_use_case,
    refresh_token_use_case,
    user_login_use_case,
)
from src.modules.identity.infrastructure.dependency_injection.uow import get_identity_uow
from src.modules.identity.infrastructure.token_service import TokenService, get_token_service

from .dto import AuthenticateUserRequest, CreateUserRequest

router = APIRouter()


@router.post(path="/users", status_code=status.HTTP_204_NO_CONTENT)
async def create_user(
    body: Annotated[CreateUserRequest, Body()],
    unit_of_work: Annotated[IIdentityUnitOfWork, Depends(get_identity_uow)],
) -> None:
    command = CreateUserCommand(
        email=body.email,
        username=body.username,
        password=body.password,
    )
    await create_user_use_case(command, unit_of_work=unit_of_work)


@router.post(path="/auth", status_code=status.HTTP_204_NO_CONTENT)
async def authenticate_user(
    response: Response,
    body: Annotated[AuthenticateUserRequest, Body()],
    unit_of_work: Annotated[IIdentityUnitOfWork, Depends(get_identity_uow)],
    token_service: Annotated[TokenService, Depends(get_token_service)],
) -> None:
    command = AuthenticateUserCommand(email=body.email, password=body.password)

    try:
        access_token, refresh_token = await user_login_use_case(
            command,
            unit_of_work=unit_of_work,
            token_service=token_service,
        )
    except InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        ) from exc

    response.set_cookie(key="access_token", value=access_token, httponly=True)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)


@router.patch(path="/auth", status_code=status.HTTP_204_NO_CONTENT)
async def refresh_tokens(
    response: Response,
    refresh_token: Annotated[str | None, Depends(TokenService.get_refresh_token_from_cookie)],
    unit_of_work: Annotated[IIdentityUnitOfWork, Depends(get_identity_uow)],
    token_service: Annotated[TokenService, Depends(get_token_service)],
) -> None:
    if refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthenticated",
        )

    command = RefreshTokenCommand(refresh_token=refresh_token)
    try:
        access_token, refresh_token = await refresh_token_use_case(
            command,
            unit_of_work=unit_of_work,
            token_service=token_service,
        )
    except InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        ) from exc

    response.set_cookie(key="access_token", value=access_token, httponly=True)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)


@router.delete(path="/auth", status_code=status.HTTP_204_NO_CONTENT)
async def logout_user(
    response: Response,
) -> None:
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
