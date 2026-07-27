import asyncio

from aiogram import Router
from aiogram.types import Message

from app.database.database import async_session
from app.repositories.blacklist_repository import BlacklistRepository
from app.repositories.whitelist_repository import WhitelistRepository
from app.services.blacklist_service import BlacklistService
from app.services.message_registration_service import MessageRegistrationService
from app.services.spam_engine import spam_engine
from app.services.whitelist_service import WhitelistService
from app.utils.logger import logger

router = Router()

REASONS = {
    "keyword": "Подозрение на спам",
    "link": "Подозрение на спам",
    "flood": "Слишком много сообщений",
    "emoji": "Подозрение на спам",
}


@router.message()
async def handle_message(message: Message):

    if message.from_user is None:
        return

    member = await message.bot.get_chat_member(
    message.chat.id,
    message.from_user.id,
)

    if member.status in ("administrator", "creator"):
        return

    async with async_session() as session:

        # ---------- BlackList ----------

        blacklist = BlacklistService(
            BlacklistRepository(session)
        )

        if await blacklist.is_blacklisted(message.from_user.id):

            logger.warning(
                f"BLACKLIST | "
                f"{message.from_user.full_name} | "
                f"{message.text}"
            )

            await message.delete()

            status = await message.answer(
                f"🛡 Сообщение пользователя "
                f"{message.from_user.full_name} удалено.\n\n"
                f"Причина: Пользователь находится в BlackList"
            )

            await asyncio.sleep(60)

            try:
                await status.delete()
            except Exception:
                pass

            return

        # ---------- WhiteList ----------

        whitelist = WhitelistService(
            WhitelistRepository(session)
        )

        if await whitelist.is_whitelisted(message.from_user.id):
            return

        # ---------- Регистрация ----------

        registration = MessageRegistrationService(session)

        await registration.register_message(message)

        logger.info(
            f"{message.from_user.full_name} | "
            f"{message.chat.title} | "
            f"{message.text}"
        )

        # ---------- Проверка на спам ----------

        result = await spam_engine.check(message)

        if result.is_spam:

            logger.warning(
                f"SPAM ({result.reason}) | "
                f"{message.from_user.full_name} | "
                f"{message.text}"
            )

            await message.delete()

            reason = REASONS.get(
                result.reason,
                result.reason,
            )

            status = await message.answer(
                f"🛡 Сообщение пользователя "
                f"{message.from_user.full_name} удалено.\n\n"
                f"Причина: {reason}"
            )

            await asyncio.sleep(60)

            try:
                await status.delete()
            except Exception:
                pass