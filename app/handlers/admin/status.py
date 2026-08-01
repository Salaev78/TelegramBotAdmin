from datetime import datetime

from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery, Message
from sqlalchemy import text

from app.callbacks.groups import GroupCallback
from app.core import runtime
from app.database.database import async_session
from app.filters.allowed_user import AllowedUser
from app.keyboards.groups import groups_keyboard
from app.repositories.group_repository import GroupRepository
from app.repositories.message_repository import MessageRepository
from app.services.group_access_service import GroupAccessService

router = Router()


@router.message(F.text == "/status", AllowedUser())
async def status(
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
            await send_status(
                message,
                groups[0].id,
            )
            return

        await message.answer(
            "🤖 Выберите группу:",
            reply_markup=groups_keyboard(
                groups,
                action="status",
            ),
        )


@router.callback_query(GroupCallback.filter(F.action == "status"))
async def status_callback(
    callback: CallbackQuery,
    callback_data: GroupCallback,
):
    await callback.answer()

    await send_status(
        callback.message,
        callback_data.group_id,
    )


async def send_status(
    message: Message,
    group_id: int,
):
    async with async_session() as session:

        # Проверка подключения к БД
        try:
            await session.execute(text("SELECT 1"))
            db_status = "🟢 Connected"
        except Exception:
            db_status = "🔴 Disconnected"

        repository = MessageRepository(session)
        group_repository = GroupRepository(session)

        stats = await repository.get_stats(group_id)
        group = await group_repository.get_by_id(group_id)

    uptime = datetime.now() - runtime.BOT_START_TIME

    days = uptime.days
    hours, remainder = divmod(
        uptime.seconds,
        3600,
    )
    minutes, _ = divmod(
        remainder,
        60,
    )

    total = stats["total"]
    deleted = stats["deleted"]

    spam_rate = (
        deleted / total * 100
        if total
        else 0
    )

    started = runtime.BOT_START_TIME.strftime(
        "%d.%m.%Y %H:%M:%S"
    )

    title = (
        group.title
        if group
        else f"ID {group_id}"
    )

    await message.answer(
        "🤖 <b>Bot Status</b>\n"
        f"<blockquote>{title}</blockquote>\n\n"
        "🟢 <b>Status:</b> Online\n"
        f"💾 <b>Database:</b> {db_status}\n\n"
        f"🚀 <b>Started:</b> {started}\n"
        f"⏱ <b>Uptime:</b> {days}d {hours}h {minutes}m\n\n"
        f"📨 <b>Messages:</b> {total}\n"
        f"🚫 <b>Deleted:</b> {deleted}\n"
        f"📈 <b>Spam rate:</b> {spam_rate:.2f}%",
        parse_mode="HTML",
    )