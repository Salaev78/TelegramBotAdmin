import asyncio


from app.handlers.start import router as start_router

from app.handlers.message_handler import router as message_router

from app.database.init_db import init_db

from app.handlers.chat_member import router as chat_member_router

from app.database.database import async_session

from app.models.group import Group

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from aiogram import Bot, Dispatcher

from config.config import BOT_TOKEN

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


async def main():
    await init_db()
    dp.include_router(start_router)
    dp.include_router(message_router) 
    dp.include_router(chat_member_router)
    
    print("Бот запущен...")
    async with async_session() as session:
        result = await session.execute(
         select(Group).options(
            selectinload(Group.members)
        )   
    )

    groups = result.scalars().all()

    for group in groups:
        print(group.title)
        print(group.members)
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped.")