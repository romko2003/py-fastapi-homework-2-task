from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import get_settings
from .models import Base  # важливо: відносний імпорт, щоб не створювати цикл

settings = get_settings()

SQLITE_DATABASE_URL = f"sqlite+aiosqlite:///{settings.PATH_TO_DB}"
sqlite_engine = create_async_engine(SQLITE_DATABASE_URL, echo=False)
AsyncSQLiteSessionLocal = sessionmaker(  # type: ignore
    bind=sqlite_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSQLiteSessionLocal() as session:
        yield session
# ================================================================


async def get_sqlite_db() -> AsyncGenerator[AsyncSession, None]:
    """Alias: те саме, що й get_db, залишено для сумісності."""
    async with AsyncSQLiteSessionLocal() as session:
        yield session


@asynccontextmanager
async def get_sqlite_db_contextmanager() -> AsyncGenerator[AsyncSession, None]:
    """Контекст-менеджер для тестів: async with get_sqlite_db_contextmanager() as db: ..."""
    async with AsyncSQLiteSessionLocal() as session:
        yield session


async def reset_sqlite_database() -> None:
    """Скидає БД: drop_all + create_all (зручно для тестів)."""
    async with sqlite_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def reset_database() -> None:
    """Alias для тестів: очікують reset_database з пакета `database`."""
    await reset_sqlite_database()
