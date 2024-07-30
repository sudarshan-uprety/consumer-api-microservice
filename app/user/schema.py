from typing import Dict, Any

from pydantic import BaseModel, EmailStr, root_validator, field_validator, ValidationError

from app.user.models import Users
from app.user.queries import get_user_by_email_or_404
from app.others import exceptions


class UserRegister(BaseModel):
    email: EmailStr
    full_name: str
    phone: int
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
            raise exceptions.ValidationError('Password must be at least 8 characters long')
        if password != confirm_password:
            raise exceptions.ValidationError('Password and confirm password do not match')
        if len(str(phone)) != 10:
            raise exceptions.ValidationError('Phone must be 10 digits long')

        user = Users.query.filter_by(email=email).first()
        if user:
            raise exceptions.ValidationError("Email already registered")

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
