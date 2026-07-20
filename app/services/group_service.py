from app.models.group import Group
from app.repositories.group_repository import GroupRepository


class GroupService:
    def __init__(self, repository: GroupRepository):
        self.repository = repository

    async def register_group(
        self,
        group_id: int,
        title: str,
    ) -> Group:
        group = await self.repository.get_by_id(group_id)

        if group is None:
            return await self.repository.create(
                group_id=group_id,
                title=title,
            )

        if group.title != title:
            group.title = title

        if not group.is_active:
            group.is_active = True

        return group