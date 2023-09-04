import os
from typing import List
from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = os.environ.get("APP_SECRET", "testing")
    HASH_ALGORITHM: str = os.environ.get("HASH_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
    ALGORITHM: str = os.environ.get("APP_SECRET", "testing")
    MONGODB_URL: str = os.environ.get("MONGODB_URL")
    ALLOWED_ORIGINS: str = os.environ.get("ALLOWED_ORIGINS", "*")
    MONGODB_DB_NAME: str = os.environ.get("MONGODB_DB_NAME", "Testing_db_name")
    TEST_MODE: bool = os.environ.get("TEST_MODE", False)
    MONGODB_INIT_COLLECTION: str = os.environ.get("MONGODB_INIT_COLLECTION", "User")
    AUTH_TOKEN_TTL: int = os.environ.get("AUTH_TOKEN_TTL", 30)
    MONGODB_TEST_DB: str = os.environ.get("MONGODB_TEST_DB", "User")


settings = Settings()
