from sqlalchemy.orm import Session

from bhagavad_gita_api.models.user import User


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_api_key(db: Session, api_key: str):
    return db.query(User).filter(User.api_key == api_key).first()


def get_valid_api_keys(db: Session):
    valid_api_keys = [
        u.api_key for u in db.query(User.api_key).filter(User.is_active == True).all()
    ]
    return valid_api_keys
