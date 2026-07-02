from __future__ import annotations

from src.libs.constants.environment.identity import ADMIN_EMAIL
from src.libs.database import async_session_maker
from src.modules.identity.domain.roles import Role
from src.modules.identity.infrastructure.sqlalchemy.unit_of_work import SqlAlchemyIdentityUnitOfWork


async def seed_admin_user() -> None:
    if not ADMIN_EMAIL:
        return

    async with async_session_maker() as session:
        uow = SqlAlchemyIdentityUnitOfWork(session)
        user = await uow.users.get_by_email(ADMIN_EMAIL)
        if user is None or user.role == Role.ADMIN:
            return

        await uow.users.set_role(user.user_id, Role.ADMIN)
        await uow.commit()
