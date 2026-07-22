import asyncio

from app.database.database import async_session
from app.repositories.message_repository import MessageRepository
from app.services.message_cleanup_service import MessageCleanupService
from app.models.group import Group
from app.models.user import User
from app.models.group_member import GroupMember
from app.models.message import Message


async def main():
    async with async_session() as session:
        repository = MessageRepository(session)
        service = MessageCleanupService(repository)

        deleted = await service.cleanup(days=0)

        print(f"Удалено сообщений: {deleted}")


if __name__ == "__main__":
    asyncio.run(main())