print("keyword_filter loaded")
from app.models.filter_result import FilterResult

SPAM_WORDS = [
    "crypto",
    "bitcoin",
    "usdt",
    "onlyfans",
    "porn",
    "casino",
]


def check(message: Message) -> FilterResult:
    text = (message.text or "").lower()

    for word in SPAM_WORDS:
        if word in text:
            return FilterResult(
                is_spam=True,
                reason=f"keyword: {word}",
                confidence=100,
            )

    return FilterResult()