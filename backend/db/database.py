"""
Database configuration for SmartHire AI.
Uses SQLite for local development (via aiosqlite).
Switch DATABASE_URL in .env to PostgreSQL for production.
"""
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

# Default to SQLite for local development (no Postgres needed)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./smarthire.db")

# If postgres URL provided, convert to asyncpg driver
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class Base(DeclarativeBase):
    pass


async def get_db():
    """Dependency: yields an async DB session."""
    async with AsyncSessionLocal() as session:
        yield session
