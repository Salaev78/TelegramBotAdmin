from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.group_repository import GroupRepository
from app.utils.admin import is_admin


class GroupAccessService:
    def __init__(self, session: AsyncSession):
        self.group_repository = GroupRepository(session)

    async def get_available_groups(
        self,
        bot: Bot,
        user_id: int,
    ):
        groups = await self.group_repository.get_all()

        available = []

        for group in groups:
            if await is_admin(bot, group.id, user_id):
                available.append(group)

        return available

    async def has_access(
        self,
        bot: Bot,
        user_id: int,
        group_id: int,
    ) -> bool:
        return await is_admin(bot, group_id, user_id)