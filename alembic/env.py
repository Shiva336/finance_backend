from logging.config import fileConfig
import asyncio

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

from app.core.config import settings
from app.models.user import Base
from app.models import user, category, financial_record, refresh_token

# Alembic Config object
config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 👇 Set DB URL from your app config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# 👇 Metadata for autogenerate
target_metadata = Base.metadata


# ----------------------------
# OFFLINE MODE
# ----------------------------
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ----------------------------
# CORE MIGRATION FUNCTION
# ----------------------------
def do_run_migrations(connection: Connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


# ----------------------------
# ONLINE MODE (ASYNC)
# ----------------------------
async def run_migrations_online():
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


# ----------------------------
# ENTRYPOINT
# ----------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())