import os
from typing import Optional

from pydantic import AnyUrl, BaseSettings


class SqlDsn(AnyUrl):
    allowed_schemes = {"postgres", "postgresql", "sqlite", "mysql"}


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

    SQLALCHEMY_DATABASE_URI: Optional[SqlDsn]

    TESTER_API_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()

if not settings.SQLALCHEMY_DATABASE_URI:
    print(
        "No SQLALCHEMY_DATABASE_URI found. \
        \nUsing in-memory Sqlite database. This is not good for running in production!"
    )
    settings.SQLALCHEMY_DATABASE_URI = "sqlite://"
