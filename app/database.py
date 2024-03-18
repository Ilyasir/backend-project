from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

# Создаём движок, передаём URL в алхимию
engine = create_async_engine(settings.DATABASE_URL)
# Создаём генератор сессий(транзакций)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Используется для миграций с alembic
class Base(DeclarativeBase):
    pass
