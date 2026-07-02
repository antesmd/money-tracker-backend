from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from fastapi import HTTPException, Request, status

from src.libs.constants.environment.authentication import AUTHENTICATION_JWT_PUBLIC_KEY_PATH
from src.libs.utils.jwt.exceptions import BaseJWTError
from src.libs.utils.jwt.implementations.pyjwt import PyJWT

if TYPE_CHECKING:
    from collections.abc import Callable

    from src.libs.utils.jwt import IJWT
    from src.modules.identity.domain.roles import Role
    from src.modules.identity.infrastructure.token_service import TokenPayload

public_key_path = Path(AUTHENTICATION_JWT_PUBLIC_KEY_PATH)
public_key = public_key_path.read_text()


def _decode_payload(request: Request) -> TokenPayload:
    jwt: IJWT = PyJWT()

    token = request.cookies.get("access_token")
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is missing",
        )

    try:
        return jwt.decode_token(  # type: ignore[return-value]
            secret=public_key,
            token=token,
            algorithm="RS256",
        )
    except BaseJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        ) from exc


def authenticate(request: Request) -> str:
    payload = _decode_payload(request)
    return payload["user_id"]


def require_role(*allowed_roles: Role) -> Callable[[Request], str]:
    allowed_role_values = {role.value for role in allowed_roles}

    def dependency(request: Request) -> str:
        payload = _decode_payload(request)
        if payload.get("role") not in allowed_role_values:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return payload["user_id"]

    return dependency
