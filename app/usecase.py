
from fastapi import HTTPException, status
from _datetime import datetime
from jose import jwt

from app import models
from app.database.database import SessionLocal
from app.utils.settings import JWT_REFRESH_SECRET_KEY, ALGORITHM


def get_user_or_404(email: str) -> models.User:
    with SessionLocal() as db:
        user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


def check_user(email: str) -> bool:
    with SessionLocal() as db:
        user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    else:
        return True


def check_phone(phone: str) -> bool:
    with SessionLocal() as db:
        user = db.query(models.User).filter(models.User.phone == phone).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Phone already exists")
    else:
        return True


def timestamp_to_datetime(timestamp: int) -> datetime:
    return datetime.fromtimestamp(timestamp)


def verify_refresh_token(refresh_token: str) -> str:
    try:
        payload = jwt.decode(refresh_token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get('sub')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")