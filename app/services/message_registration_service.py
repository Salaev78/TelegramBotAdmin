from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.group_service import GroupService
from app.services.user_service import UserService
from app.services.group_member_service import GroupMemberService
from app.utils.logger import logger


class MessageRegistrationService:
    def __init__(self, session: AsyncSession):
        self.session = session

        self.group_service = GroupService(session)
        self.user_service = UserService(session)
        self.group_member_service = GroupMemberService(session)

    async def register_message(
        self,
        message: Message,
    ) -> None:
        
        if message.from_user is None:
            return
        
        try:
            await self.group_service.register_group(
                group_id=message.chat.id,
                title=message.chat.title or "Unknown",
            )

            await self.user_service.register_user(
                user_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                is_bot=message.from_user.is_bot,
            )

            await self.group_member_service.register_member(
                group_id=message.chat.id,
                user_id=message.from_user.id,
            )

            await self.session.commit()

        except Exception:
            await self.session.rollback()

            logger.exception(
                "Failed to register message in database."
            )

            raise