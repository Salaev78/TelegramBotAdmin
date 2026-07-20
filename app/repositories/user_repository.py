from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )

        return result.scalar_one_or_none()

    async def create(
        self,
        user_id: int,
        username: str | None,
        first_name: str,
        is_bot: bool,
    ) -> User:

        user = User(
            id=user_id,
            username=username,
            first_name=first_name,
            is_bot=is_bot,
        )

        self.session.add(user)

        return user