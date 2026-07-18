
from aiogram.types import Message

from app.models.filter_result import FilterResult

from app.filters.keyword_filter import check as keyword_check

from app.filters.link_filter import check as link_check

from app.filters.flood_filter import check as flood_check

FILTERS = [
    keyword_check,
    link_check,
    flood_check,
]        
        
class SpamEngine:

    async def check(self, message) -> FilterResult:

        text = message.text or ""
        
        for filter_check in FILTERS:
            result = filter_check(message) 

            if result.is_spam:
                return result

        return FilterResult()


spam_engine = SpamEngine()