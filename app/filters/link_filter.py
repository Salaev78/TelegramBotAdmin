import re

from aiogram.types import Message

from app.models.filter_result import FilterResult


LINK_PATTERN = re.compile(
    r"\b(?:https?://)?"
    r"(?:"
    r"(?:www\.)?"
    r"(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}"
    r"|t\.me"
    r"|telegram\.me"
    r"|discord\.gg"
    r")"
    r"(?:/\S*)?\b",
    re.IGNORECASE,
)


def check(message: Message) -> FilterResult:
    text = message.text or ""

    if LINK_PATTERN.search(text):
        return FilterResult(
            is_spam=True,
            reason="link",
            confidence=90,
        )

    return FilterResult()