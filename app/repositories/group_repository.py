from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.group import Group


class GroupRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, group_id: int) -> Group | None:
        result = await self.session.execute(
            select(Group).where(Group.id == group_id)
        )

        return result.scalar_one_or_none()

    async def get_all(self) -> list[Group]:
        result = await self.session.execute(
              select(Group)
        )
        return result.scalars().all()

    async def create(
        self,
        group_id: int,
        title: str,
    ) -> Group:
        group = Group(
            id=group_id,
            title=title,
        )

        self.session.add(group)

        return group