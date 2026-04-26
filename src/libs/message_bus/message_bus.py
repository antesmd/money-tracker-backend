from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable


class MessageBus:
    _handlers: dict[
        type[Any],
        list[Callable[[Any], Awaitable[None]] | Callable[[Any], None]],
    ]

    def __init__(self) -> None:
        self._handlers: dict[
            type[Any],
            list[Callable[[Any], Awaitable[None]] | Callable[[Any], None]],
        ] = {}

    def register(
        self,
        message_type: type[Any],
        handler: Callable[[Any], Awaitable[None]] | Callable[[Any], None],
    ) -> None:
        if message_type not in self._handlers:
            self._handlers[message_type] = []

        self._handlers[message_type].append(handler)

    def dispatch(self, message: object) -> None:
        message_type = type(message)
        if message_type in self._handlers:
            for handler in self._handlers[message_type]:
                if asyncio.iscoroutinefunction(handler):
                    asyncio.create_task(handler(message))
                else:
                    handler(message)
