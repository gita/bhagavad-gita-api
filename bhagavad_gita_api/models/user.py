from sqlalchemy import Boolean, Column, Integer, String

from bhagavad_gita_api.db.base_class import Base
from bhagavad_gita_api.utils import AwareDateTime, tzware_datetime


class User(Base):
    __tablename__ = "gita_users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(128))
    email = Column(String, unique=True, index=True)
    app_name = Column(String, index=True)
    app_description = Column(String, index=True)
    app_link = Column(String(128))
    api_key = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

    created_on = Column(AwareDateTime(), default=tzware_datetime)
