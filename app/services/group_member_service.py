from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.group_member import GroupMember
from app.repositories.group_member_repository import GroupMemberRepository


class GroupMemberService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = GroupMemberRepository(session)

    async def register_member(
        self,
        group_id: int,
        user_id: int,
    ) -> GroupMember:
    
        member = await self.repository.get(
            group_id=group_id,
            user_id=user_id,
        )

        if member is None:
            member = GroupMember(
                group_id=group_id,
                user_id=user_id,
            )
            await self.repository.create(member)
            return member

        if not member.is_active:
            member.is_active = True
            member.left_at = None


        return member

    async def leave_member(
        self,
        group_id: int,
        user_id: int,
    ) -> GroupMember | None:

        member = await self.repository.get(
            group_id=group_id,
            user_id=user_id,
        )

        if member is None:
            return None

        member.is_active = False
        member.left_at = datetime.utcnow()


        return member