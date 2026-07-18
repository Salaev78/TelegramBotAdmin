from aiogram import Router
from aiogram.types import Message

from app.utils.logger import logger
from app.services.spam_engine import spam_engine

router = Router()


@router.message()
async def handle_message(message: Message):
    logger.info(
        f"{message.from_user.full_name} | "
        f"{message.chat.title} | "
        f"{message.text}"
    )

    result = await spam_engine.check(message)

    if result.is_spam:
        logger.warning(
            f"SPAM ({result.reason}) | "
            f"{message.from_user.full_name} | "
            f"{message.text}"
        )
        await message.delete()
        return
