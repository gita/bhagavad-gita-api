from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session

from bhagavad_gita_api.config import settings
from bhagavad_gita_api.db.base_class import Base

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(engine)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))  
Base.query = db_session.query_property()