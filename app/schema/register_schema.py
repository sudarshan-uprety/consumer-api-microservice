from pydantic import BaseModel, EmailStr, field_validator, ValidationError, validator


class UserRegister(BaseModel):
    email: EmailStr
    name: str
    phone: str
    address: str
    password: str
    confirm_password: str
    city: str
    state: str
    address: str
    username: str

    @field_validator('password')
    def password_validator(cls, value, values):
        print('herere')
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return value

    @field_validator('confirm_password')
    def passwords_match(cls, value, values):
        if value != values.data.get('password'):
            raise ValueError('Password and confirm password do not match')
        return value


class UserRegisterResponse(BaseModel):
    email: EmailStr
    name: str
    phone: str
    address: str
    city: str
    state: str
    address: str
    username: str
