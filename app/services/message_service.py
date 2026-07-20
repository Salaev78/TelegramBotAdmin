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