from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


# SQLALCHEMY_DATABASE_URL = "sqlite:///foo.db"

SQLALCHEMY_DATABASE_URL = "postgresql://krishna:t5sOw9aMmBENpmNFIT9roi7IWCykWj2v@oregon-postgres.render.com:5432/bhagavadgita_kp4u"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
    # SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()