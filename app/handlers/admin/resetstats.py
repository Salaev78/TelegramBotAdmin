from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.core import runtime
from app.filters.admin_only import AdminOnly

router = Router()


@router.message(Command("resetstats"), AdminOnly())
async def reset_stats(message: Message):
    runtime.PROCESSED_MESSAGES = 0
    runtime.DELETED_MESSAGES = 0

    runtime.KEYWORD_DETECTIONS = 0
    runtime.LINK_DETECTIONS = 0
    runtime.FLOOD_DETECTIONS = 0
    runtime.EMOJI_DETECTIONS = 0

    await message.answer(
        "✅ <b>Statistics have been reset.</b>",
        parse_mode="HTML",
    )