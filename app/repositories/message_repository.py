from datetime import datetime

from sqlalchemy import delete, select, update, case, func
#from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message


class MessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        telegram_id: int,
        group_id: int,
        user_id: int,
        text: str | None,
        message_type: str,
    ) -> Message:
        message = Message(
            telegram_id=telegram_id,
            group_id=group_id,
            user_id=user_id,
            text=text,
            message_type=message_type,
        )

        self.session.add(message)
        await self.session.flush()

        return message

    async def get_by_telegram_id(
        self,
        telegram_id: int,
        group_id: int,
    ) -> Message | None:
        result = await self.session.execute(
            select(Message).where(
                Message.telegram_id == telegram_id,
                Message.group_id == group_id,
            )
        )

        return result.scalar_one_or_none()

    async def delete_before(self, before: datetime) -> int:
        result = await self.session.execute(
            delete(Message).where(Message.created_at < before)
        )
        await self.session.commit()
        return result.rowcount or 0

    async def mark_deleted(
        self,
        telegram_id: int,
        group_id: int,
        reason: str,
    ) -> None:
        await self.session.execute(
            update(Message)
            .where(
                Message.telegram_id == telegram_id,
                Message.group_id == group_id,
            )
            .values(
                is_deleted=True,
                delete_reason=reason,
                deleted_at=func.now(),
            )
        )

    async def get_recent_deleted(
        self,
        group_id: int,
        limit: int = 10,
    ) -> list[Message]:

        result = await self.session.execute(
            select(Message)
            .where(
                Message.group_id == group_id,
                Message.is_deleted.is_(True),
            )
            .order_by(Message.deleted_at.desc())
            .limit(limit)
        )

        return list(result.scalars())

    async def get_stats(self, group_id: int) -> dict:
        total = await self.session.scalar(
            select(func.count(Message.id))
            .where(Message.group_id == group_id)
        )

        deleted = await self.session.scalar(
            select(func.count(Message.id))
            .where(
                Message.group_id == group_id,
                Message.is_deleted.is_(True),
            )
        )

        reasons = await self.session.execute(
            select(
                Message.delete_reason,
                func.count(Message.id),
            )
            .where(
                Message.group_id == group_id,
                Message.is_deleted.is_(True),
            )
            .group_by(Message.delete_reason)
        )

        return {
            "total": total or 0,
            "deleted": deleted or 0,
            "alive": (total or 0) - (deleted or 0),
            "reasons": dict(reasons.all()),
            }
    async def get_logs(
        self,
        group_id: int,
        limit: int = 10,
    ):
        result = await self.session.execute(
            select(Message)
            .where(
                Message.group_id == group_id,
                Message.is_deleted.is_(True),
            )
            .order_by(Message.deleted_at.desc())
            .limit(limit)
        )

        return result.scalars().all()