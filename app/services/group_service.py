from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.group_repository import GroupRepository


class GroupService:
    def __init__(self, session: AsyncSession):
        self.repository = GroupRepository(session)

    async def register_group(
        self,
        group_id: int,
        title: str,
    ):
        group = await self.repository.get_by_id(group_id)

        if group is not None:
            return group

        group = await self.repository.create(
            group_id=group_id,
            title=title,
        )

        await self.repository.session.commit()

        return group