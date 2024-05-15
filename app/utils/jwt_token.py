from fastapi import HTTPException, status

from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt

from app.utils.settings import (ACCESS_TOKEN_EXPIRE_MINUTES, JWT_REFRESH_SECRET_KEY, ALGORITHM, JWT_SECRET_KEY,
                                REFRESH_TOKEN_EXPIRE_MINUTES)

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


async def verify_password(password: str, hashed_pass: str):
    if not password_context.verify(password, hashed_pass):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")


async def compare_passwords(new_password: str, old_hashed_password: str) -> bool:
    if password_context.verify(new_password, old_hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="New password cannot be current password.")


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=int(REFRESH_TOKEN_EXPIRE_MINUTES))

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt