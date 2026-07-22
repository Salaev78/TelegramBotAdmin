from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.whitelist import Whitelist


class WhitelistRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_user(
        self,
        user_id: int,
        username: str | None = None,
        reason: str | None = None,
    ) -> None:

        self._session.add(
            Whitelist(
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
            delete(Whitelist).where(
                Whitelist.user_id == user_id
            )
        )

        return result.rowcount > 0

    async def is_whitelisted(
        self,
        user_id: int,
    ) -> bool:

        result = await self._session.execute(
            select(Whitelist.id).where(
                Whitelist.user_id == user_id
            )
        )

        return result.scalar_one_or_none() is not None

    async def get_user(
        self,
        user_id: int,
    ) -> Whitelist | None:

        result = await self._session.execute(
            select(Whitelist).where(
                Whitelist.user_id == user_id
            )
        )

        return result.scalar_one_or_none()