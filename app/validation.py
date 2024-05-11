
from fastapi import HTTPException, status
from jose import jwt

from app import models, schemas
from app.utils.settings import JWT_REFRESH_SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session
from app.utils.jwt_token import verify_password


async def signup_user_verification(email: str, phone: str, db: Session) -> None:
    user = db.query(models.User).filter(models.User.email == email or models.User.phone == phone).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email or Phone already registered")


async def login_user_verification(email: str, password: str, db: Session) -> models.User:
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        if await verify_password(password=password, hashed_pass=user.password):
            return user
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect email or password')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


def verify_refresh_token(refresh_token: str) -> str:
    try:
        payload = jwt.decode(refresh_token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get('sub')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")


async def check_used_token(token: str, db: Session) -> bool:
    try:
        token = db.query(models.UsedToken).filter(models.UsedToken.token == token).first()
        if token:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Token already used.")
        else:
            return False
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
