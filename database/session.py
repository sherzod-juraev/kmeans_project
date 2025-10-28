from .connect import async_session_local
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db() -> AsyncSession:
    async with async_session_local() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
