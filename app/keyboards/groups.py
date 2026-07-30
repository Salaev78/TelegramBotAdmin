from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.callbacks.groups import GroupCallback
from app.models.group import Group


def groups_keyboard(
    groups: list[Group],
    action: str,
) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    for group in groups:
        builder.button(
            text=group.title,
            callback_data=GroupCallback(
                action=action,
                group_id=group.id,
            ),
        )

    builder.adjust(1)

    return builder.as_markup()