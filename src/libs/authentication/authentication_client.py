from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from fastapi import HTTPException, Request, status

from src.libs.constants.environment.authentication import AUTHENTICATION_JWT_PUBLIC_KEY
from src.libs.utils.jwt.exceptions import BaseJWTError
from src.libs.utils.jwt.implementations.pyjwt import PyJWT

if TYPE_CHECKING:
    from src.identity.infrastructure.token_service import TokenPayload
    from src.libs.utils.jwt import IJWT

public_key_path = Path(AUTHENTICATION_JWT_PUBLIC_KEY)
public_key = public_key_path.read_text()


def authenticate(request: Request) -> str:
    jwt: IJWT = PyJWT()

    token = request.cookies.get("access_token")
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is missing",
        )

    try:
        payload: TokenPayload = jwt.decode_token(
            secret=public_key,
            token=token,
            algorithm="RS256",
        )  # type: ignore[assignment]
    except BaseJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        ) from exc
    else:
        return payload["user_id"]
