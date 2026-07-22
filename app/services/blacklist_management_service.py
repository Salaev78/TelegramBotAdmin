from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.blacklist_repository import BlacklistRepository
from app.services.blacklist_service import BlacklistService
from app.utils.logger import logger


class BlacklistManagementService:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

        self.blacklist_service = BlacklistService(
            BlacklistRepository(session)
        )

    async def add_user(
        self,
        user_id: int,
        username: str | None = None,
        reason: str | None = None,
    ) -> bool:

        try:
            result = await self.blacklist_service.add_user(
                user_id=user_id,
                username=username,
                reason=reason,
            )

            await self.session.commit()

            return result

        except Exception:
            await self.session.rollback()

            logger.exception(
                "Failed to add user to blacklist."
            )

            raise

    async def remove_user(
        self,
        user_id: int,
    ) -> bool:

        try:
            result = await self.blacklist_service.remove_user(
                user_id=user_id
            )

            await self.session.commit()

            return result

        except Exception:
            await self.session.rollback()

            logger.exception(
                "Failed to remove user from blacklist."
            )

            raise