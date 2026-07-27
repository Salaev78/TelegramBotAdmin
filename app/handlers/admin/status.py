from datetime import datetime
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import text

from app.core import runtime
from app.database.database import async_session

from app.filters.admin_only import AdminOnly

from aiogram import F

router = Router()


@router.message(F.text == "/status", AdminOnly())
async def status(message: Message):

    # Проверка БД
    try:
        async with async_session() as session:
            await session.execute(text("SELECT 1"))
        db_status = "🟢 Connected"
    except Exception:
        db_status = "🔴 Disconnected"

    uptime = datetime.now() - runtime.BOT_START_TIME

    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    started = runtime.BOT_START_TIME.strftime("%d.%m.%Y %H:%M:%S")

    await message.answer(
        "🤖 <b>Bot Status</b>\n\n"
        "🟢 <b>Status:</b> Online\n"
        f"💾 <b>Database:</b> {db_status}\n\n"
        f"🚀 <b>Started:</b> {started}\n"
        f"⏱ <b>Uptime:</b> {days}d {hours}h {minutes}m\n\n"
        f"📨 <b>Messages processed:</b> {runtime.PROCESSED_MESSAGES}\n"
        f"🚫 <b>Spam deleted:</b> {runtime.DELETED_MESSAGES}",
        parse_mode="HTML",
    )