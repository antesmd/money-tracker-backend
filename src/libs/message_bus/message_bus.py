from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable

logger = logging.getLogger(__name__)


class MessageBus[T]:
    def __init__(self) -> None:
        self._handlers: dict[type[Any], list[Callable[[Any], None]]] = {}

    def register(self, message_type: type[T], handler: Callable[[T], None]) -> None:
        if message_type not in self._handlers:
            self._handlers[message_type] = []

        self._handlers[message_type].append(handler)

    def dispatch(self, message: object) -> None:
        message_type = type(message)
        if message_type in self._handlers:
            for handler in self._handlers[message_type]:
                handler(message)
