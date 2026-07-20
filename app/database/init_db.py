from app.database.base import Base
from app.database.database import engine
from app.models.group import Group
from app.models.user import User
from app.models.group_member import GroupMember

# Импортируем модели, чтобы SQLAlchemy "увидела" их
from app.models.group import Group
from pathlib import Path

print(Path("storage/database/database.db").resolve())

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)