print("keyword_filter loaded")
from app.models.filter_result import FilterResult

SPAM_WORDS = [
        "crypto", "bitcoin", "btc", "eth", "ethereum",
    "usdt", "usdc", "ton", "toncoin", "wallet",
    "airdrop", "blockchain", "web3", "binance", "крипта", "биток",

    # Казино / ставки
    "casino", "aviator", "1win", "melbet", "parimatch",
    "bet", "букмекер", "ставки", "казино",

    # 18+
    "onlyfans", "of", "nsfw", "porn", "sex", "escort", "cp",

    # Работа / развод
    "заработок", "доход", "без вложений", "работа онлайн",
    "инвестиции", "пассивный доход",

    # Telegram
    "t.me/", "@",

    # Спам
    "пиши в лс", "в лс", "личные сообщения",
    "пишите в личку", "пиши мне"
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