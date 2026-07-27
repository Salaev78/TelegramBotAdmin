from dataclasses import dataclass


@dataclass(slots=True)
class UserStats:
    username: str = ""
    full_name: str = ""

    processed: int = 0
    deleted: int = 0

    keyword: int = 0
    link: int = 0
    flood: int = 0
    emoji: int = 0