from __future__ import annotations

from datetime import UTC, datetime, timezone


class DateTimeUtils:
    @staticmethod
    def now(*, timezone: timezone = UTC, naive: bool = True) -> datetime:
        dt = datetime.now(timezone)
        if naive:
            dt = dt.replace(tzinfo=None)

        return dt

    @classmethod
    def utc_now(cls, *, naive: bool = True) -> datetime:
        return cls.now(timezone=UTC, naive=naive)

    @staticmethod
    def from_timestamp(
        timestamp: float,
        *,
        timezone: timezone = UTC,
        naive: bool = True,
    ) -> datetime:
        dt = datetime.fromtimestamp(timestamp, timezone)
        if naive:
            dt = dt.replace(tzinfo=None)

        return dt

    @classmethod
    def utc_from_timestamp(cls, timestamp: float, *, naive: bool = True) -> datetime:
        return cls.from_timestamp(timestamp, timezone=UTC, naive=naive)
