from datetime import datetime

from pydantic import BaseModel, EmailStr, root_validator
from fastapi import HTTPException, status

from app.usecase import get_user_or_404, check_user, check_phone
from app.utils.jwt_token import verify_password
from app import models


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

    @root_validator(pre=True)
    def validate(cls, field_values):
        check_user(field_values['email'])
        check_phone(field_values['phone'])
        if field_values['password'] != field_values['confirm_password']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
        return field_values


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    @root_validator(pre=True)
    def validate(cls, field_values) -> models.User:
        user = get_user_or_404(field_values['email'])
        if not verify_password(password=field_values['password'], hashed_pass=user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Email or Password")
        else:
            return user


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

    @root_validator(pre=True)
    def validate(cls, field_values):
        user = get_user_or_404(field_values['email'])
        return field_values


class ForgetPasswordRequest(BaseModel):
    password: str
    confirm_password: str
    token: str

    @root_validator(pre=True)
    def validate(cls, field_values):
        try:
            if len(field_values['password']) < 8:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Password must be at least 8 characters")
            if field_values['password'] != field_values['confirm_password']:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
            return field_values
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


class UserDetails(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    created_at: datetime
