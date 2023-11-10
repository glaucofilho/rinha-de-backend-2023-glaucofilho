from contextlib import asynccontextmanager
from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import Session


@asynccontextmanager
async def get_session() -> Generator:
    session: AsyncSession = Session()

    try:
        yield session
        await session.commit()
    except:
        await session.rollback()
        raise
    finally:
        await session.close()
