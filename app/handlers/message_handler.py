import asyncio
from datetime import datetime

from aiogram import F, Router
from aiogram.types import Message

from app.core import runtime
from app.database.database import async_session
from app.models.deletion_log import DeletionLog
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


@router.message(~F.text.startswith("/"), F.text)
async def handle_message(message: Message):

    if message.from_user is None:
        return

    # Если понадобится игнорировать админов
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

        runtime.PROCESSED_MESSAGES += 1

        stats = runtime.USER_STATS[message.from_user.id]
        stats.username = message.from_user.username or ""
        stats.full_name = message.from_user.full_name
        stats.processed += 1

        logger.info(
            f"{message.from_user.full_name} | "
            f"{message.chat.title} | "
            f"{message.text}"
        )

        # ---------- Проверка на спам ----------

        result = await spam_engine.check(message)

        if result.is_spam:

            reason_key = result.reason.split(":", 1)[0].strip()

            if reason_key == "keyword":
                runtime.KEYWORD_DETECTIONS += 1
                stats.keyword += 1

            elif reason_key == "link":
                runtime.LINK_DETECTIONS += 1
                stats.link += 1

            elif reason_key == "flood":
                runtime.FLOOD_DETECTIONS += 1
                stats.flood += 1

            elif reason_key == "emoji":
                runtime.EMOJI_DETECTIONS += 1
                stats.emoji += 1

            logger.warning(
                f"SPAM ({result.reason}) | "
                f"{message.from_user.full_name} | "
                f"{message.text}"
            )

            await message.delete()

            await registration.mark_message_deleted(
                telegram_id=message.message_id,
                group_id=message.chat.id,
                reason=reason_key,
            )

            runtime.DELETED_MESSAGES += 1
            stats.deleted += 1

            runtime.DELETION_LOGS.append(
                DeletionLog(
                    time=datetime.now().strftime("%H:%M:%S"),
                    chat_title=message.chat.title or "Private",
                    user_id=message.from_user.id,
                    username=message.from_user.username
                    or message.from_user.full_name,
                    reason=reason_key.upper(),
                    text=(message.text or "<без текста>")[:200],
                )
            )

            reason = REASONS.get(
                reason_key,
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
