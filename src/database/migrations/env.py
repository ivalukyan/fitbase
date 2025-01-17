from logging.config import fileConfig
from models import Base
from os import getenv
from dotenv import load_dotenv

import sqlalchemy
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Загрузка переменных окружения из файла .env
load_dotenv()

# Alembic Config объект, обеспечивающий доступ к значению из .ini файла
config = context.config

# Настройка логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Добавляем метаданные моделей для автогенерации
target_metadata = Base.metadata

# Указываем URL базы данных из переменной окружения или по умолчанию
config.set_main_option("sqlalchemy.url", getenv("DATABASE_URL"))

def run_migrations_offline() -> None:
    """Запуск миграций в режиме 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Запуск миграций в режиме 'online'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()