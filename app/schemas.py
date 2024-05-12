from datetime import datetime

from pydantic import BaseModel, EmailStr, root_validator, validator, ValidationError
from fastapi import HTTPException, status


class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    confirm_password: str
    phone: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: UserOut


class TokenPayload(BaseModel):
    sub: str
    exp: int


class SystemUser(BaseModel):
    id: int
    full_name: str
    email: str

    class Config:
        orm_mode = True


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class EmailSchema(BaseModel):
    email: EmailStr


class ForgetPasswordRequest(BaseModel):
    password: str
    confirm_password: str
    token: str


class UserDetails(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    created_at: datetime
    phone: str
