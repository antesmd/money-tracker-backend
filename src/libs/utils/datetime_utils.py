from __future__ import annotations

from datetime import UTC, datetime, timezone


class DateTimeUtils:
    @staticmethod
    def now(timezone: timezone = UTC) -> datetime:
        return datetime.now(timezone)

    @classmethod
    def utc_now(cls) -> datetime:
        return cls.now(UTC)

    @staticmethod
    def from_timestamp(timestamp: float, timezone: timezone = UTC) -> datetime:
        return datetime.fromtimestamp(timestamp, timezone)

    @classmethod
    def utc_from_timestamp(cls, timestamp: float) -> datetime:
        return cls.from_timestamp(timestamp, UTC)
