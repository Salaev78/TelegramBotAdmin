from dataclasses import dataclass


@dataclass(slots=True)
class DeletionLog:
    time: str
    chat_title: str
    user_id: int
    username: str
    reason: str
    text: str