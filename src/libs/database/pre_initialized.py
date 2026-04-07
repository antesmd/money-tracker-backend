from __future__ import annotations

from typing import Final

from src.libs.constants.database import DATABASE_URL

from .engine import create_database_engine
from .sessions import create_async_session_maker

engine: Final = create_database_engine(DATABASE_URL)
async_session_maker: Final = create_async_session_maker(engine)
