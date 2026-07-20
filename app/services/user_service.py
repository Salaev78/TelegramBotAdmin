from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)

    async def register_user(
        self,
        user_id: int,
        username: str | None,
        first_name: str,
        is_bot: bool,
    ) -> User:

        user = await self.repository.get_by_id(user_id)

        if user is None:
            return await self.repository.create(
                user_id=user_id,
                username=username,
                first_name=first_name,
                is_bot=is_bot,
            )

        if user.username != username:
            user.username = username

        if user.first_name != first_name:
            user.first_name = first_name

        if user.is_bot != is_bot:
            user.is_bot = is_bot

        return user