from app.models.message import Message
from app.repositories.message_repository import MessageRepository


class MessageService:
    def __init__(self, repository: MessageRepository):
        self.repository = repository

    async def register_message(
        self,
        telegram_id: int,
        group_id: int,
        user_id: int,
        text: str | None,
        message_type: str,
    ) -> Message:
        return await self.repository.create(
            telegram_id=telegram_id,
            group_id=group_id,
            user_id=user_id,
            text=text,
            message_type=message_type,
        )
    async def mark_deleted(
        self,
        telegram_id: int,
        group_id: int,
        reason: str,
    ) -> None:
        await self.repository.mark_deleted(
            telegram_id=telegram_id,
            group_id=group_id,
            reason=reason,
        )

    async def get_recent_deleted(
        self,
        group_id: int,
        limit: int = 10,
    ):
        return await self.repository.get_recent_deleted(
            group_id,
            limit,
        )