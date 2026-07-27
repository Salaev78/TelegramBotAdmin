from aiogram import Router
from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message

import app.core.runtime as runtime
from app.filters.admin_only import AdminOnly

router = Router()


@router.message(F.text == "/stats", AdminOnly())
async def stats(message: Message):
    processed = runtime.PROCESSED_MESSAGES
    deleted = runtime.DELETED_MESSAGES

    spam_rate = (
        deleted / processed * 100
        if processed
        else 0
    )

    await message.answer(
        "📊 <b>Statistics</b>\n\n"
        f"📨 <b>Processed:</b> {processed}\n"
        f"🚫 <b>Deleted:</b> {deleted}\n\n"
        f"🔤 <b>Keyword:</b> {runtime.KEYWORD_DETECTIONS}\n"
        f"🔗 <b>Links:</b> {runtime.LINK_DETECTIONS}\n"
        f"🌊 <b>Flood:</b> {runtime.FLOOD_DETECTIONS}\n"
        f"😊 <b>Emoji:</b> {runtime.EMOJI_DETECTIONS}\n\n"
        f"📈 <b>Spam rate:</b> {spam_rate:.2f}%",
        parse_mode="HTML",
    )