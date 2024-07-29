
from fastapi import HTTPException, status
from jose import jwt

from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models import models
from app.others import usecase
from app.utils.jwt_token import verify_password
from app.utils.settings import JWT_REFRESH_SECRET_KEY, ALGORITHM


async def signup_user_verification(email: str, phone: str, db: Session) -> None:
    user = db.query(models.User).filter(or_(models.User.email == email, models.User.phone == phone)).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email or Phone already registered")
    else:
        pass


async def login_user_verification(email: str, password: str, db: Session) -> models.User:
    user = await usecase.get_user_or_404(email=email, db=db)

    if not user.is_active or user.is_deleted:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Inactive or deleted account')

    await verify_password(password=password, hashed_pass=user.password)

    return user


async def password_validation(password: str, confirm_password: str) -> None:
    if len(password) < 8 or len(confirm_password) < 8:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Password must be at least 8 characters long')
    if confirm_password != password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')
    pass


async def verify_refresh_token(refresh_token: str) -> str:
    payload = jwt.decode(refresh_token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
    return payload.get('sub')


async def check_used_token(token: str, db: Session) -> bool:
    token = db.query(models.UsedToken).filter(models.UsedToken.token == token).first()
    if token:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Token already used.")
    else:
        return False


async def current_password_validation(old_hashed_password: str, new_hashed_password: str) -> None:
    if old_hashed_password == new_hashed_password:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="New password can not be current password.")