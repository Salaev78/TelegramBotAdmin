import asyncio

from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message

from app.database.database import async_session
from app.services.whitelist_management_service import WhitelistManagementService
from app.utils.admin import is_admin

router = Router()


async def send_temporary_message(
    message: Message,
    text: str,
    seconds: int = 30,
):
    response = await message.reply(text)

    await asyncio.sleep(seconds)

    try:
        await response.delete()
    except Exception:
        pass

    try:
        await message.delete()
    except Exception:
        pass


@router.message(Command("whitelist"))
async def whitelist(
    message: Message,
    bot: Bot,
):
    if message.from_user is None:
        return

    if not await is_admin(
        bot=bot,
        chat_id=message.chat.id,
        user_id=message.from_user.id,
    ):
        return

    if message.reply_to_message is None:
        await send_temporary_message(
            message,
            "❌ Ответьте на сообщение пользователя.",
            seconds=8,
        )
        return

    user = message.reply_to_message.from_user

    if user is None:
        return

    reason = message.text.removeprefix("/whitelist").strip()

    if reason == "":
        reason = None

    async with async_session() as session:

        whitelist = WhitelistManagementService(session)

        added = await whitelist.add_user(
            user_id=user.id,
            username=user.username,
            reason=reason,
        )

    if not added:
        await send_temporary_message(
            message,
            "⚠️ Пользователь уже находится в WhiteList.",
            seconds=8,
        )
        return

    await send_temporary_message(
        message,
        f"✅ {user.full_name} добавлен в WhiteList.",
    )


@router.message(Command("unwhitelist"))
async def unwhitelist(
    message: Message,
    bot: Bot,
):
    if message.from_user is None:
        return

    if not await is_admin(
        bot=bot,
        chat_id=message.chat.id,
        user_id=message.from_user.id,
    ):
        return

    if message.reply_to_message is None:
        await send_temporary_message(
            message,
            "❌ Ответьте на сообщение пользователя.",
            seconds=8,
        )
        return

    user = message.reply_to_message.from_user

    if user is None:
        return

    async with async_session() as session:

        whitelist = WhitelistManagementService(session)

        removed = await whitelist.remove_user(
            user_id=user.id,
        )

    if not removed:
        await send_temporary_message(
            message,
            "⚠️ Пользователь отсутствует в WhiteList.",
            seconds=8,
        )
        return

    await send_temporary_message(
        message,
        f"✅ {user.full_name} удалён из WhiteList.",
    )