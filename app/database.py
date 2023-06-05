from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

# Используем pydantic для конфиденциальных данных в файле config
from app.config import settings

# Создаем ссылку к нашей локальной базе данных для алхимии
# Используем postgresql и драйвер asyncpg
engine = create_async_engine(settings.DATABASE_URL)

# Генератор сессий(транзакций) # async_sessionmaker из 2.0 Алхимии
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass
