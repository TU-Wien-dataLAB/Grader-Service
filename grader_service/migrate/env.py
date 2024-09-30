# Copyright (c) 2022, TU Wien
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config, pool
from alembic import context
import grader_service.orm

# Alembic configuration
config = context.config

# Set up logging from the config file
fileConfig(config.config_file_name)

def configure_db_url():
    """Set the database URL from environment variables if not set in config."""
    if not config.get_main_option('sqlalchemy.url'):
        db_url = os.getenv("GRADER_DB_URL", "sqlite:///grader.db")
        config.set_main_option('sqlalchemy.url', db_url)

configure_db_url()

# Metadata for autogenerate support
target_metadata = grader_service.orm.Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = config.attributes.get('connection', None)
    if connectable is None:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix='sqlalchemy.',
            poolclass=pool.NullPool
        )

    try:
        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                render_as_batch=True
            )

            with context.begin_transaction():
                context.run_migrations()
    except Exception as e:
        raise

# Run migrations according to the mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()