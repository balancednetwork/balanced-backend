import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import SQLModel

from balanced_backend.db import ASYNC_SQLALCHEMY_DATABASE_URL, SQLALCHEMY_DATABASE_URL

from balanced_backend.tables.historical import DailyHistorical
from balanced_backend.tables.volumes import (
    ContractMethodVolume,
    VolumeSeries5Min,
    VolumeSeries15Min,
    VolumeSeries1Hour,
    VolumeSeries4Hour,
    VolumeSeries1Day,
    VolumeSeries1Month,
)
from balanced_backend.tables.tokens import Token, TokenPool, TokenPrice
from balanced_backend.tables.pools import Pool
from balanced_backend.tables.dex import DexSwap
from balanced_backend.tables.dividends import Dividend

# Other versions imported each object
config = context.config

config.set_main_option("sqlalchemy.url", ASYNC_SQLALCHEMY_DATABASE_URL)

fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = SQLModel.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    url = SQLALCHEMY_DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """
    Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

asyncio.run(run_migrations_online())
