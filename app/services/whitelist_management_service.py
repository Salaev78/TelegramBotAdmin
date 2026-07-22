from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.whitelist_repository import WhitelistRepository
from app.services.whitelist_service import WhitelistService
from app.utils.logger import logger


class WhitelistManagementService:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

        self.whitelist_service = WhitelistService(
            WhitelistRepository(session)
        )

    async def add_user(
        self,
        user_id: int,
        username: str | None = None,
        reason: str | None = None,
    ) -> bool:

        try:
            result = await self.whitelist_service.add_user(
                user_id=user_id,
                username=username,
                reason=reason,
            )

            await self.session.commit()

            return result

        except Exception:
            await self.session.rollback()

            logger.exception(
                "Failed to add user to whitelist."
            )

            raise

    async def remove_user(
        self,
        user_id: int,
    ) -> bool:

        try:
            result = await self.whitelist_service.remove_user(
                user_id=user_id
            )

            await self.session.commit()

            return result

        except Exception:
            await self.session.rollback()

            logger.exception(
                "Failed to remove user from whitelist."
            )

            raise