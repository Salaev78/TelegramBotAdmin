import asyncio


from app.handlers.start import router as start_router

from app.handlers.message_handler import router as message_router

from app.database.init_db import init_db

from aiogram import Bot, Dispatcher

from config.config import BOT_TOKEN

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(start_router)
    dp.include_router(message_router) 
    
    print("Бот запущен...")
    
    await init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped.")