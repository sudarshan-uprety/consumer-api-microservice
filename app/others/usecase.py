from _datetime import datetime

from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from app.models.models import User
from app.utils.jwt_token import get_hashed_password


async def get_user_or_404(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if user:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


async def timestamp_to_datetime(timestamp: int) -> datetime:
    return datetime.fromtimestamp(timestamp)


# check if the user is already active
async def check_user_active(email: str, db: Session) -> User:
    user = db.query(User).filter(User.email == email).first()
    if user.is_active:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User {email} already active')
    else:
        return user


async def change_password(user: User, password: str, db: Session) -> User:
    user.password = get_hashed_password(password=password)
    db.commit()
    return user
