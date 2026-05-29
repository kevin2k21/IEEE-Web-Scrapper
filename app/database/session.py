"""
Database session management and configuration.

This module initializes the SQLAlchemy async engine and provides
a dependency to get database sessions for FastAPI routes or other async contexts.
"""
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set")

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)

async def get_db():
    """
    Yields an asynchronous database session.

    Intended to be used as a FastAPI dependency. Automatically handles
    session closure when the request is completed.

    Yields:
        AsyncSession: The database session.
    """
    async with AsyncSessionLocal() as session:
        yield session
