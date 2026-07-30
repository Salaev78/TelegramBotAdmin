from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.command import CommandObject
from aiogram.types import Message

from app.core import runtime
from app.filters.allowed_user import AllowedUser

router = Router()


@router.message(Command("user"), AllowedUser())
async def user_info(
    message: Message,
    command: CommandObject,
):

    if not command.args:
        await message.answer(
            "❌ Использование:\n<code>/user &lt;user_id&gt;</code>",
            parse_mode="HTML",
        )
        return

    try:
        user_id = int(command.args)
    except ValueError:
        await message.answer(
            "❌ User ID должен быть числом."
        )
        return

    stats = runtime.USER_STATS.get(user_id)

    if stats is None:
        await message.answer(
            "❌ Пользователь не найден."
        )
        return

    username = (
        f"@{stats.username}"
        if stats.username
        else "—"
    )

    text = (
        "👤 <b>Информация о пользователе</b>\n\n"
        f"🪪 <b>Имя:</b> {stats.full_name}\n"
        f"📛 <b>Username:</b> {username}\n"
        f"🆔 <b>ID:</b> <code>{user_id}</code>\n\n"
        f"📨 <b>Обработано:</b> {stats.processed}\n"
        f"🗑 <b>Удалено:</b> {stats.deleted}\n\n"
        f"🔤 <b>Keyword:</b> {stats.keyword}\n"
        f"🔗 <b>Link:</b> {stats.link}\n"
        f"📨 <b>Flood:</b> {stats.flood}\n"
        f"😀 <b>Emoji:</b> {stats.emoji}"
    )

    await message.answer(
        text,
        parse_mode="HTML",
    )