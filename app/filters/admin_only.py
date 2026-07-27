from aiogram.filters import BaseFilter
from aiogram.types import Message

from app.config import ALLOWED_USERS


class AdminOnly(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return (
            message.from_user is not None
            and message.from_user.id in ALLOWED_USERS
        )