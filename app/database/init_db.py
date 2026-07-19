from app.database.base import Base
from app.database.database import engine

# Импортируем модели, чтобы SQLAlchemy "увидела" их
from app.models.group import Group
from pathlib import Path

print(Path("storage/database/database.db").resolve())

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)