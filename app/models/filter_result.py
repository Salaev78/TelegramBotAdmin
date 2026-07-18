from dataclasses import dataclass


@dataclass
class FilterResult:
    is_spam: bool = False
    reason: str | None = None
    confidence: int = 0