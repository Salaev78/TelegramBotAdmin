from aiogram.filters.callback_data import CallbackData


class GroupCallback(CallbackData, prefix="group"):
    action: str
    group_id: int