import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import AnyUrl, BaseSettings

load_dotenv()


def get_database_uri():
    DB_USER = os.getenv("POSTGRES_USER")
    DB_PASS = os.getenv("POSTGRES_PASSWORD")
    DB_NAME = os.getenv("POSTGRES_DB")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    if None in [DB_USER, DB_PASS, DB_NAME, DB_HOST, DB_PORT]:
        return None
    return "postgresql://{user}:{password}@{host}:{port}/{database}".format(
        user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT, database=DB_NAME
    )


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

    SQLALCHEMY_DATABASE_URI: Optional[SqlDsn] = get_database_uri()

    TESTER_API_KEY: str
    # celery cronjobs
    CELERY_BROKER: str = os.getenv("CELERY_BROKER")
    CELERY_BACKEND: str = os.getenv("CELERY_BACKEND")
    CRONJOB_BASE_URL: str = os.getenv("CRONJOB_BASE_URL", "http://api:8081")

    TWITTER = {
        "CONSUMER_KEY": os.getenv("CONSUMER_KEY"),
        "CONSUMER_SECRET": os.getenv("CONSUMER_SECRET"),
        "CLIENT_ID": os.getenv("CLIENT_ID"),
        "CLIENT_SECRET": os.getenv("CLIENT_SECRET"),
        "ACCESS_TOKEN": os.getenv("ACCESS_TOKEN"),
        "ACCESS_TOKEN_SECRET": os.getenv("ACCESS_TOKEN_SECRET"),
    }

    INSTAGRAM = {
        "USERNAME": os.getenv("INSTAGRAM_USERNAME"),
        "PASSWORD": os.getenv("INSTAGRAM_PASSWORD"),
    }

    class Config:
        env_file = ".env"


settings = Settings()

if not settings.SQLALCHEMY_DATABASE_URI:
    print(
        "No SQLALCHEMY_DATABASE_URI found. \
        \nUsing default set Sqlite database gita.db. This is not good for running in production!"
    )
    settings.SQLALCHEMY_DATABASE_URI = "sqlite:///{}?{}".format(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "gita.db"),
        "check_same_thread=False",
    )
