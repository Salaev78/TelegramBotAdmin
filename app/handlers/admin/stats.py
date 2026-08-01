from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery, Message

from app.callbacks.groups import GroupCallback
from app.database.database import async_session
from app.filters.allowed_user import AllowedUser
from app.keyboards.groups import groups_keyboard
from app.repositories.group_repository import GroupRepository
from app.repositories.message_repository import MessageRepository
from app.services.group_access_service import GroupAccessService

router = Router()

REASON_NAMES = {
    "keyword": "🔑 Ключевые слова",
    "link": "🔗 Ссылки",
    "flood": "🌊 Флуд",
    "emoji": "😊 Эмодзи",
}


def format_stats(group_title: str, stats: dict) -> str:
    total = stats["total"]
    deleted = stats["deleted"]
    alive = stats["alive"]

    percent = (deleted / total * 100) if total else 0

    reasons = []

    for reason, count in stats["reasons"].items():
        title = REASON_NAMES.get(reason, reason)
        reasons.append(f"{title}: {count}")

    if not reasons:
        reasons.append("Удалённых сообщений нет.")

    return (
        f"📊 <b>Статистика группы</b>\n"
        f"<blockquote>{group_title}</blockquote>\n\n"
        f"💬 <b>Всего сообщений:</b> {total}\n"
        f"🟢 <b>Не удалено:</b> {alive}\n"
        f"🔴 <b>Удалено:</b> {deleted} ({percent:.1f}%)\n\n"
        f"━━━━━━━━━━━━━━\n\n"
        f"🛡 <b>Причины удаления</b>\n"
        + "\n".join(reasons)
    )


@router.message(F.text == "/stats", AllowedUser())
async def stats(
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
            await send_stats(
                message,
                groups[0].id,
            )
            return

        await message.answer(
            "📊 Выберите группу:",
            reply_markup=groups_keyboard(
                groups,
                action="stats",
            ),
        )


@router.callback_query(GroupCallback.filter(F.action == "stats"))
async def stats_callback(
    callback: CallbackQuery,
    callback_data: GroupCallback,
):
    await callback.answer()

    await send_stats(
        callback.message,
        callback_data.group_id,
    )


async def send_stats(
    message: Message,
    group_id: int,
):
    async with async_session() as session:

        repository = MessageRepository(session)
        group_repository = GroupRepository(session)

        stats = await repository.get_stats(group_id)
        group = await group_repository.get_by_id(group_id)

        if group is None:
            await message.answer(
                "❌ Группа не найдена."
            )
            return

        await message.answer(
            format_stats(
                group.title,
                stats,
            ),
            parse_mode="HTML",
        )