from typing import Dict, Any

from pydantic import BaseModel, EmailStr, root_validator

from app.user.models import Users
from app.user.queries import get_user_or_404


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
            raise ValueError('Password must be at least 8 characters long')
        if password != confirm_password:
            raise ValueError('Password and confirm password do not match')
        if len(str(phone)) != 10:
            raise ValueError('Phone must be 10 digits long')

        user = Users.query.filter_by(email=email).first()
        if user:
            raise ValueError("Email already registered")

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
