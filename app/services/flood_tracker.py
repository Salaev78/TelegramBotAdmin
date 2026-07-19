from collections import defaultdict
from typing import DefaultDict
import time


class FloodTracker:
    MAX_MESSAGES = 5
    TIME_WINDOW = 10

    def __init__(self):
        self.history: DefaultDict[int, list[float]] = defaultdict(list)

    def register_message(self, user_id: int) -> bool:
        current_time = time.time()

        # Добавляем текущее сообщение
        self.history[user_id].append(current_time)

        # Оставляем только сообщения за последние TIME_WINDOW секунд
        self.history[user_id] = [
            timestamp
            for timestamp in self.history[user_id]
            if current_time - timestamp <= self.TIME_WINDOW
        ]

        # Проверяем лимит
        return len(self.history[user_id]) >= self.MAX_MESSAGES


flood_tracker = FloodTracker()