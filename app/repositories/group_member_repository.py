from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.group_member import GroupMember


class GroupMemberRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(
        self,
        group_id: int,
        user_id: int,
    ) -> GroupMember | None:

        result = await self.session.execute(
            select(GroupMember).where(
                GroupMember.group_id == group_id,
                GroupMember.user_id == user_id,
            )
        )

        return result.scalar_one_or_none()

    async def create(
        self,
        group_member: GroupMember,
    ) -> None:

        self.session.add(group_member)