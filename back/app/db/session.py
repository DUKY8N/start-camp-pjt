"""
SQLAlchemy async 엔진 및 세션팩토리.
사용법(의존성 주입 예시):
    async def route(db: AsyncSession = Depends(get_session)): ...
"""
import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./dev.db")

engine = create_async_engine(
    DATABASE_URL,
    future=True,
    echo=False,
)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI 의존성으로 사용하세요:
    async def handler(db: AsyncSession = Depends(get_session)):
        async with db.begin():
            ...
    """
    async with AsyncSessionLocal() as session:
        yield session