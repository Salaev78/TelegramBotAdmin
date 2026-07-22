import unicodedata

from aiogram.types import Message

from app.models.filter_result import FilterResult


def check(message: Message) -> FilterResult:
    text = message.text or ""

    if not text:
        return FilterResult()

    total = len(text)

    emoji_count = 0

    for char in text:
        if unicodedata.category(char) == "So":
            emoji_count += 1

    ratio = emoji_count / total

    if emoji_count >= 5 and ratio >= 0.5:
        return FilterResult(
            is_spam=True,
            reason=f"emoji",
            confidence=100,
        )

    return FilterResult()