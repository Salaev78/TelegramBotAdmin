from aiogram.types import Message

from app.models.filter_result import FilterResult
from app.filters.keyword_filter import SPAM_WORDS


def check(message: Message) -> FilterResult:
    text = (message.text or "").lower()

    contains_link = (
        "http://" in text
        or "https://" in text
        or "t.me/" in text
        or "telegram.me/" in text
        or "www." in text
    )

    contains_spam_word = any(word in text for word in SPAM_WORDS)

    if contains_link and contains_spam_word:
        return FilterResult(
            is_spam=True,
            reason="link + spam words",
            confidence=100,
        )

    return FilterResult()