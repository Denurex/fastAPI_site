from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (AsyncSession, async_session,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.util.preloaded import engine_url

from app.config import DATABASE_URL, TEST_DATABASE_URL, settings

if settings.MODE == 'TEST':
    DB_URL = TEST_DATABASE_URL
    DATABASE_PARAMS = {'poolclass' : NullPool}
else:
    DB_URL = DATABASE_URL
    DATABASE_PARAMS = {}


engine = create_async_engine(DB_URL, **DATABASE_PARAMS)

async_session_maker = sessionmaker(engine, class_= AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass
