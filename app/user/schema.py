from typing import Dict, Any

from pydantic import BaseModel, EmailStr, root_validator, field_validator, ValidationError

from app.user.models import Users
from app.others import exceptions


class UserRegister(BaseModel):
    email: EmailStr
    full_name: str
    phone: str
    address: str
    password: str
    confirm_password: str

    @root_validator(pre=True)
    def validate_all(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        password = values.get('password')
        confirm_password = values.get('confirm_password')
        phone = values.get('phone')
        email = values.get('email')

        if password and len(password) < 8:
            raise exceptions.GenericError(
                message='Password must be at least 8 characters long.',
                status_code=400
            )

        if password != confirm_password:
            raise exceptions.GenericError(
                message='Password and confirm_password must be the same.',
                status_code=400
            )

        if len(phone) != 10:
            raise exceptions.GenericError(
                message='Phone number must be 10 characters long.',
                status_code=400
            )

        phone = Users.query.filter_by(phone=phone).first()
        if phone is not None:
            raise exceptions.GenericError(
                message='Phone number already exists.',
                status_code=400)

        user = Users.query.filter_by(email=email).first()
        if user is not None:
            raise exceptions.GenericError(
                message='Email already registered.',
                status_code=400
            )

        return values

    class Config:
        from_attributes = True


class UserRegisterResponse(BaseModel):
    email: EmailStr
    full_name: str
    phone: str
    address: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: UserRegisterResponse
