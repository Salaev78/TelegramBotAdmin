from aiogram import Bot, Router
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION
from aiogram.types import ChatMemberUpdated

from app.database.database import async_session
from app.services.group_service import GroupService

router = Router()


@router.my_chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def bot_added(event: ChatMemberUpdated, bot: Bot):

    if event.new_chat_member.user.id != bot.id:
        return

    async with async_session() as session:
        service = GroupService(session)

        await service.register_group(
            group_id=event.chat.id,
            title=event.chat.title,
        )

        print(f"Группа сохранена: {event.chat.title}")