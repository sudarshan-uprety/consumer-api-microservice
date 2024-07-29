from datetime import datetime

from pydantic import BaseModel, EmailStr
from typing import List


class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr

    class Config:
        from_attributes = True


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
        from_attributes = True


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


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str


class UserOrder(BaseModel):
    id: int
    product: str
    quantity: int
    price: float
    is_delivered: bool

    class Config:
        from_attributes = True


class UserOrderList(BaseModel):
    orders: List[UserOrder]

# class UserOrderList(BaseModel):
#     id: str
#     product: str
#     quantity: int
#     price: float
#     is_delivered: bool
#
#     class Config:
#         from_attributes = True
