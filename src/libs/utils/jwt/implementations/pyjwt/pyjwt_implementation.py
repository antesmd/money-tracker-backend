from __future__ import annotations

from typing import TYPE_CHECKING, Any, final, override

import jwt

from src.libs.utils.jwt.exceptions import (
    ExpiredTokenError,
    InvalidTokenSignatureError,
    JWTBackendError,
)
from src.libs.utils.jwt.jwt_interface import IJWT

if TYPE_CHECKING:
    from collections.abc import Mapping
    from datetime import datetime


@final
class PyJWT(IJWT):
    @override
    @staticmethod
    def create_token(
        *,
        secret: str,
        algorithm: str,
        expiration_date: datetime | None = None,
        payload: Mapping[str, Any] | None = None,
    ) -> str:
        to_encode: dict[str, Any] = {}
        if payload is not None:
            to_encode.update(payload)

        if expiration_date is not None:
            to_encode["exp"] = int(expiration_date.timestamp())

        return jwt.encode(
            algorithm=algorithm,
            key=secret,
            payload=to_encode,
        )

    @override
    @staticmethod
    def decode_token(
        *,
        secret: str,
        algorithm: str,
        token: str,
        verify_signature: bool = True,
    ) -> Mapping[str, Any]:
        try:
            payload: Mapping[str, Any] = jwt.decode(
                jwt=token,
                key=secret,
                algorithms=[algorithm],
                options={
                    "verify_signature": verify_signature,
                },
            )
        except jwt.exceptions.ExpiredSignatureError as exc:
            raise ExpiredTokenError from exc
        except jwt.exceptions.InvalidSignatureError as exc:
            raise InvalidTokenSignatureError from exc
        except jwt.exceptions.PyJWTError as exc:
            raise JWTBackendError from exc
        else:
            return payload
