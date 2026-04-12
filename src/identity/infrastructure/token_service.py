from __future__ import annotations

from datetime import timedelta
from pathlib import Path
from typing import TypedDict

from fastapi import Cookie

from src.libs.constants.environment.authentication import (
    AUTHENTICATION_JWT_ACCESS_EXPIRATION_SECONDS,
    AUTHENTICATION_JWT_PRIVATE_KEY,
    AUTHENTICATION_JWT_PUBLIC_KEY,
    AUTHENTICATION_JWT_REFRESH_EXPIRATION_SECONDS,
)
from src.libs.utils import DateTimeUtils
from src.libs.utils.jwt import IJWT, BaseJWTError
from src.libs.utils.jwt.implementations.pyjwt.pyjwt_implementation import PyJWT


class TokenPayload(TypedDict):
    user_id: str


class TokenService:
    __private_key: str
    __public_key: str
    __algorithm: str
    __access_token_expire_seconds: int
    __refresh_token_expire_seconds: int
    __jwt: IJWT

    def __init__(
        self,
        private_key: str,
        public_key: str,
        algorithm: str,
        access_token_expire_seconds: int,
        refresh_token_expire_seconds: int,
        jwt: IJWT,
    ) -> None:
        self.__private_key = private_key
        self.__public_key = public_key
        self.__algorithm = algorithm
        self.__access_token_expire_seconds = access_token_expire_seconds
        self.__refresh_token_expire_seconds = refresh_token_expire_seconds
        self.__jwt = jwt

    def create_access_token(
        self,
        payload: TokenPayload,
    ) -> str:
        expire = DateTimeUtils.utc_now() + timedelta(seconds=self.__access_token_expire_seconds)
        return self.__jwt.create_token(
            secret=self.__private_key,
            algorithm=self.__algorithm,
            payload=payload,
            expiration_date=expire,
        )

    def create_refresh_token(
        self,
        payload: TokenPayload,
    ) -> str:
        expire = DateTimeUtils.utc_now() + timedelta(seconds=self.__refresh_token_expire_seconds)
        return self.__jwt.create_token(
            secret=self.__private_key,
            algorithm=self.__algorithm,
            payload=payload,
            expiration_date=expire,
        )

    def decode_token(self, token: str) -> TokenPayload | None:
        try:
            return self.__jwt.decode_token(
                secret=self.__public_key,
                algorithm=self.__algorithm,
                token=token,
            )  # type: ignore[return-value]
        except BaseJWTError:
            return None

    @staticmethod
    def get_refresh_token_from_cookie(
        refresh_token: str | None = Cookie(default=None, alias="refresh_token"),
    ) -> str | None:
        return refresh_token


def get_token_service() -> TokenService:
    return TokenService(
        private_key=Path(AUTHENTICATION_JWT_PRIVATE_KEY).read_text(),
        public_key=Path(AUTHENTICATION_JWT_PUBLIC_KEY).read_text(),
        algorithm="RS256",
        access_token_expire_seconds=AUTHENTICATION_JWT_ACCESS_EXPIRATION_SECONDS,
        refresh_token_expire_seconds=AUTHENTICATION_JWT_REFRESH_EXPIRATION_SECONDS,
        jwt=PyJWT(),
    )
