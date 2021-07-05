from sqlalchemy.orm import Session

from bhagavad_gita_api import crud
from bhagavad_gita_api.config import settings
from bhagavad_gita_api.data import insert_all
from bhagavad_gita_api.db.base_class import Base
from bhagavad_gita_api.db.session import engine
from bhagavad_gita_api.models import user


def init_db(db: Session) -> None:
    # add test user
    user_in = crud.get_user(db, user_id=1)
    new_db = False
    if not user_in:
        new_db = True
        user_in = user.User(
            id=1,
            full_name="Radha Krishna",
            email="admin@bhagavadgita.io",
            app_name="BhagavadGita.io",
            app_description="BhagavadGita.io is a modern Bhagavad Gita app with a simple, beautiful and easy to use interface, helping you focus on reading. It is an app built for Bhagavad Gita readers, by Bhagavad Gita readers.",
            app_link="https://bhagavadgita.io",
            api_key=settings.TESTER_API_KEY,
            is_active=True,
        )

        db.add(user_in)
        db.commit()

    Base.metadata.create_all(engine)
    if new_db:
        # pass
        insert_all()
        # reference_all()
        # the reference scripts are very slow
