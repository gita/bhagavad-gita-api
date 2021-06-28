from typing import Generator

import crud
from db.session import SessionLocal
from fastapi import Depends, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from models.user import User
from sqlalchemy.orm import Session

API_KEY_NAME = "X-API-KEY"
api_key_header_auth = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), api_key_header: str = Security(api_key_header_auth)
) -> User:
    if api_key_header not in crud.get_valid_api_keys(db):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    user = crud.get_user_by_api_key(db, api_key=api_key_header)
    if not user:
        raise HTTPException(status_code=404, detail="Account not found.")
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive account.")
    return current_user
