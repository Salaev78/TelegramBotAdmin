import re

from app.models.filter_result import FilterResult

LINK_PATTERN = re.compile(
    r"(https?://|www\.|t\.me/|telegram\.me/)",
    re.IGNORECASE
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