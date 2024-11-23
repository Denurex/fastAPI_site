import sys
from logging.config import fileConfig
from os.path import abspath, dirname

from alembic import context
from sqlalchemy import engine_from_config, pool

# Убедитесь, что путь к вашему приложению корректен
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from app.bookings.models import Bookings
from app.config import DATABASE_URL, TEST_DATABASE_URL
from app.database import Base
from app.hotels.models import Hotels, Rooms
from app.users.users_models import Users

# Получаем объект конфигурации Alembic
config = context.config

# Устанавливаем URL для подключения к базе данных
config.set_main_option('sqlalchemy.url', f'{DATABASE_URL}?async_fallback=True')

# Настройка логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Добавляем метаданные для поддержки автогенерации миграций
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Запуск миграций в офлайн-режиме."""
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
    """Запуск миграций в онлайн-режиме."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
