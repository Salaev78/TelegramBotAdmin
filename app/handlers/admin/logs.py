from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.database.database import async_session
from app.repositories.message_repository import MessageRepository
from app.services.message_service import MessageService
from app.filters.admin_only import AdminOnly

router = Router()


@router.message(Command("logs"), AdminOnly())
async def logs(message: Message):

    async with async_session() as session:

        message_service = MessageService(
            MessageRepository(session)
        )
        print(message.chat.id)
        deleted_messages = await message_service.get_recent_deleted(
            group_id=message.chat.id,
            limit=10,
        )

    if not deleted_messages:
        await message.answer("📭 Логи пока пусты.")
        return

    lines = []

    for log in deleted_messages:

        username = (
            f"@{log.username}"
            if log.username
            else log.full_name
        )

        text = log.text or "-"

        reason = log.delete_reason or "Не указана"

        deleted_at = (
            log.deleted_at.strftime("%H:%M:%S %d.%m.%Y")
            if log.deleted_at
            else "-"
        )

        lines.append(
            f"🕒 <b>{deleted_at}</b>\n"
            f"👤 {username} ({log.user_id})\n"
            f"🚫 {reason}\n"
            f"💬 <code>{text}</code>\n"
        )

    await message.answer(
        "📋 <b>Последние удалённые сообщения</b>\n\n"
        + "\n".join(lines),
        parse_mode="HTML",
    )