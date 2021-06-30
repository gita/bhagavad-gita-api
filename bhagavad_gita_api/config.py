import os
from typing import Optional

from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    project_name: str = "Bhagavad Gita API"
    admin_email: str = "admin@bhagavadgita.io"
    debug: bool = False

    # Server
    server_name: Optional[str]
    server_host: Optional[str]
    sentry_dsn: Optional[str]
    secret_key: bytes = os.urandom(32)

    API_V2_STR: str = "/v2"

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn]

    TESTER_API_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()

if not settings.SQLALCHEMY_DATABASE_URI:
    # use in-memory sqlite db
    settings.SQLALCHEMY_DATABASE_URI = "sqlite://"
