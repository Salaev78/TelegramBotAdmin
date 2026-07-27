from datetime import datetime
from collections import deque
from collections import defaultdict

from app.models.user_stats import UserStats

# Время запуска бота
BOT_START_TIME = datetime.now()

# Статистика
PROCESSED_MESSAGES = 0
DELETED_MESSAGES = 0

KEYWORD_DETECTIONS = 0
LINK_DETECTIONS = 0
FLOOD_DETECTIONS = 0
EMOJI_DETECTIONS = 0
DELETION_LOGS = deque(maxlen=50)
USER_STATS = defaultdict(UserStats)