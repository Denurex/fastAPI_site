from typing import Literal

from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"] # Значение по умолчанию

    class Config:
        env_file = ".env-base"  # Файл для загрузки режима приложения

base_config = BaseConfig()

class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"] = base_config.MODE
    LOG_LEVEL: Literal['INFO', 'DEBUG']

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    SECRET_KEY: str
    ALGORITHM: str
    # DATABASE_URL:str

    REDIS_HOST: str
    REDIS_PORT: int

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    class Config:
        env_file = ".env-non-dev" if base_config.MODE == "PROD" else ".env"


# if __name__ == '__main__':
#     settings = Settings()
#     DATABASE_URL = f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'
#     print(DATABASE_URL)

settings = Settings()

DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

TEST_DATABASE_URL = f"postgresql+asyncpg://{settings.TEST_DB_USER}:{settings.TEST_DB_PASS}@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}"
