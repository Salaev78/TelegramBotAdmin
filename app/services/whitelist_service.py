from app.repositories.whitelist_repository import WhitelistRepository


class WhitelistService:
    def __init__(
        self,
        repository: WhitelistRepository,
    ):
        self._repository = repository

    async def add_user(
        self,
        user_id: int,
        username: str | None = None,
        reason: str | None = None,
    ) -> bool:

        if await self._repository.is_whitelisted(user_id):
            return False

        await self._repository.add_user(
            user_id=user_id,
            username=username,
            reason=reason,
        )

        return True

    async def remove_user(
        self,
        user_id: int,
    ) -> bool:

        return await self._repository.remove_user(user_id)

    async def is_whitelisted(
        self,
        user_id: int,
    ) -> bool:

        return await self._repository.is_whitelisted(user_id)

    async def get_user(
        self,
        user_id: int,
    ):

        return await self._repository.get_user(user_id)