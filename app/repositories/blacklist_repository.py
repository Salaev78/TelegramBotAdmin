from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.blacklist import Blacklist


class BlacklistRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_user(
        self,
        user_id: int,
        username: str | None = None,
        reason: str | None = None,
    ) -> None:

        self._session.add(
            Blacklist(
                user_id=user_id,
                username=username,
                reason=reason,
            )
        )

    async def remove_user(
        self,
        user_id: int,
    ) -> bool:

        result = await self._session.execute(
            delete(Blacklist).where(
                Blacklist.user_id == user_id
            )
        )

        return result.rowcount > 0

    async def is_blacklisted(
        self,
        user_id: int,
    ) -> bool:

        result = await self._session.execute(
            select(Blacklist.id).where(
                Blacklist.user_id == user_id
            )
        )

        return result.scalar_one_or_none() is not None

    async def get_user(
        self,
        user_id: int,
    ) -> Blacklist | None:

        result = await self._session.execute(
            select(Blacklist).where(
                Blacklist.user_id == user_id
            )
        )

        return result.scalar_one_or_none()