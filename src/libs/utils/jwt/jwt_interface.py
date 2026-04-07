from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Mapping
    from datetime import datetime


class IJWT(ABC):
    @staticmethod
    @abstractmethod
    def create_token(
        *,
        secret: str,
        algorithm: str,
        payload: Mapping[str, Any] | None = None,
        expiration_date: datetime | None = None,
    ) -> str:
        """
        Create token.

        Parameters:
            secret (str):
                Secret key for encoding.
            algorithm (str):
                Algorithm for encoding.
            expiration_date (datetime):
                Expiration date of token.
            payload (dict[str, Any] | None):
                Payload of token.

        Returns:
            str: JWT token.
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def decode_token(
        *,
        secret: str,
        algorithm: str,
        token: str,
        verify_signature: bool = True,
    ) -> Mapping[str, Any]:
        """
        Decode token and return content of payload.

        Parameters:
            secret (str):
                Secret key for decoding.
            algorithm (str):
                Algorithm for decoding.
            token (str):
                JWT token.
            verify_signature (bool):
                Should the signature be verified.

        Raises:
            BaseJWTError:
                If any error occurs during decoding.

        Returns:
            Any: Content of token's payload.
        """
        raise NotImplementedError
