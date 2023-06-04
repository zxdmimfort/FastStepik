from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Используем pydantic для конфиденциальных данных в файле config
from app.config import settings

# Создаем ссылку к нашей локальной базе данных для алхимии
# Используем postgresql и драйвер asyncpg
engine = create_async_engine(settings.DATABASE_URL)

# Генератор сессий(транзакций)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass
