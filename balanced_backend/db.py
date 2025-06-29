from typing import AsyncGenerator

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine

from balanced_backend.config import settings

SQLALCHEMY_DATABASE_URL_STUB = "://{user}:{password}@{server}:{port}/{db}".format(
    user=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    server=settings.POSTGRES_SERVER,
    port=settings.POSTGRES_PORT,
    db=settings.POSTGRES_DATABASE,
)

ASYNC_SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg" + SQLALCHEMY_DATABASE_URL_STUB
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2" + SQLALCHEMY_DATABASE_URL_STUB

logger.info(
    f"Connecting to server: {settings.POSTGRES_SERVER} and {settings.POSTGRES_DATABASE}"
)

async_engine = create_async_engine(
    ASYNC_SQLALCHEMY_DATABASE_URL,
    echo=True,
    future=True,
    pool_size=20,
    max_overflow=10,
)

async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Run onetime if we want to init with a prebuilt table of attributes
async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


engine = create_engine(SQLALCHEMY_DATABASE_URL)
session_factory = sessionmaker(bind=engine)
