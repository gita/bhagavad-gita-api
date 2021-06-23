from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///foo.db"

# SQLALCHEMY_DATABASE_URL = "postgresql://pi:12345@192.168.18.15:5432/gita"


engine = create_engine(
    # SQLALCHEMY_DATABASE_URL
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
