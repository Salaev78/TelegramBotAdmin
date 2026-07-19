from pathlib import Path

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

DATABASE_URL = "sqlite+aiosqlite:///storage/database/database.db"

print("Рабочая директория:", Path.cwd())
print("Путь к БД:", Path(DATABASE_URL.replace("sqlite+aiosqlite:///", "")).resolve())

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)