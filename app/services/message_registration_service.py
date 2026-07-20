from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.message_repository import MessageRepository
from app.services.group_member_service import GroupMemberService
from app.services.group_service import GroupService
from app.services.message_service import MessageService
from app.services.user_service import UserService
from app.repositories.group_repository import GroupRepository
from app.repositories.user_repository import UserRepository
from app.repositories.group_member_repository import GroupMemberRepository
from app.utils.logger import logger


class MessageRegistrationService:
    def __init__(self, session: AsyncSession):
        self.session = session

        self.group_service = GroupService(GroupRepository(session))
        self.user_service = UserService(UserRepository(session))
        self.group_member_service = GroupMemberService(GroupMemberRepository(session))

        self.message_service = MessageService(
            MessageRepository(session)
        )

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

            await self.message_service.register_message(
                telegram_id=message.message_id,
                group_id=message.chat.id,
                user_id=message.from_user.id,
                text=message.text,
                message_type=message.content_type,
            )

            await self.session.commit()

        except Exception:
            await self.session.rollback()

            logger.exception(
                "Failed to register message in database."
            )

            raise