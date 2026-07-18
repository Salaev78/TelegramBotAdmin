from aiogram.types import Message

from app.models.filter_result import FilterResult
from app.services.flood_tracker import flood_tracker


def check(message: Message) -> FilterResult:
    if flood_tracker.register_message(message.from_user.id):
        return FilterResult(
            is_spam=True,
            reason="flood",
            confidence=95,
        )

    return FilterResult()