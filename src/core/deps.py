from contextlib import asynccontextmanager
from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import Session


@asynccontextmanager
async def get_session() -> Generator:
    session: AsyncSession = Session()

    try:
        yield session
    except Exception:
        await session.rollback()
    finally:
        await session.close()
