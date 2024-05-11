from datetime import datetime

from pydantic import BaseModel, EmailStr, root_validator, validator, ValidationError
from fastapi import HTTPException, status

from app.validation import login_user_verification


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

    @validator('confirm_password')
    def validate(cls, confirm_password, values):
        if confirm_password != values["password"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')
        return values


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

    @root_validator(pre=True)
    def validate(cls, field_values):
        user = login_user_verification(field_values['email'])
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
    phone: str
