from datetime import datetime, timedelta, timezone

class MessageCleanupService:
    def __init__(self, repository: MessageRepository):
        self.repository = repository

    async def cleanup(self, days: int = 30):
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)

        deleted = await self.repository.delete_before(cutoff)

        return deleted