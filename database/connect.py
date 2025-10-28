from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from core import config


async_engine = create_async_engine(
    url=config.DATABASE_URL,
    pool_size=30,
    max_overflow=60,
    pool_recycle=1800,
    pool_timeout=5
)

async_session_local = async_sessionmaker(bind=async_engine)
Base = declarative_base()