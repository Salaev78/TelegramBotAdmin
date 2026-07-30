from aiogram import F, Bot, Router
from aiogram.types import CallbackQuery

from app.callbacks.groups import GroupCallback

router = Router()


@router.callback_query(
    GroupCallback.filter(F.action == "stats")
)
async def stats_callback(
    callback: CallbackQuery,
    callback_data: GroupCallback,
    bot: Bot,
):
    await callback.answer()

    await callback.message.answer(
        f"Выбрана группа:\n{callback_data.group_id}"
    )