import asyncio
from datetime import datetime, timedelta, timezone
from app.database.database import async_session
from app.repositories.message_repository import MessageRepository
from app.services.message_cleanup_service import MessageCleanupService


async def main():
    async with async_session() as session:
        repository = MessageRepository(session)
        service = MessageCleanupService(repository)

        deleted = await service.cleanup(days=0)

        print(f"Удалено сообщений: {deleted}")


if __name__ == "__main__":
    asyncio.run(main())