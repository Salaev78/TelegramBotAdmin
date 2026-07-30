from aiogram import Bot, F, Router
from aiogram.types import Message

from app.database.database import async_session
from app.filters.allowed_user import AllowedUser
from app.keyboards.groups import groups_keyboard
from app.repositories.message_repository import MessageRepository
from app.services.group_access_service import GroupAccessService

router = Router()

REASON_NAMES = {
    "keyword": "🔑 Ключевые слова",
    "link": "🔗 Ссылки",
    "flood": "🌊 Флуд",
}


def format_logs(group_title: str, logs: list) -> str:
    if not logs:
        return (
            f"📋 <b>Последние удаления</b>\n"
            f"<blockquote>{group_title}</blockquote>\n\n"
            f"Удалённых сообщений пока нет."
        )

    text = (
        f"📋 <b>Последние удаления</b>\n"
        f"<blockquote>{group_title}</blockquote>\n\n"
    )

    for log in logs:

        reason = REASON_NAMES.get(
            log.delete_reason,
            log.delete_reason or "Неизвестно",
        )

        message_text = (
            log.text.strip()
            if log.text
            else "<без текста>"
        )

        if len(message_text) > 120:
            message_text = message_text[:120] + "..."

        deleted_at = (
            log.deleted_at.strftime("%d.%m.%Y %H:%M")
            if log.deleted_at
            else "Неизвестно"
        )

        text += (
            f"🕒 <b>{deleted_at}</b>\n"
            f"👤 <code>{log.user_id}</code>\n"
            f"🚫 {reason}\n"
            f"<blockquote>{message_text}</blockquote>\n\n"
        )

    return text


@router.message(F.text == "/logs", AllowedUser())
async def logs(
    message: Message,
    bot: Bot,
):
    async with async_session() as session:

        access_service = GroupAccessService(session)

        groups = await access_service.get_available_groups(
            bot,
            message.from_user.id,
        )

        if not groups:
            await message.answer(
                "❌ У вас нет доступа ни к одной группе."
            )
            return

        if len(groups) == 1:
            repository = MessageRepository(session)

            logs = await repository.get_logs(
                groups[0].id,
            )

            await message.answer(
                format_logs(
                    groups[0].title,
                    logs,
                ),
                parse_mode="HTML",
            )
            return

        await message.answer(
            "📋 Выберите группу:",
            reply_markup=groups_keyboard(
                groups,
                action="logs",
            ),
        )