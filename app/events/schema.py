from pydantic import BaseModel, EmailStr


class ProductItem(BaseModel):
    product_id: str
    quantity: int


class ReduceQuantityEvent(BaseModel):
    trace_id: str
    operation: str
    product: list[ProductItem]


class RegisterEmailEvent(BaseModel):
    trace_id: str
    event_name: str
    to: EmailStr
    otp: str
    full_name: str


class ForgotPasswordEvent(BaseModel):
    trace_id: str
    event_name: str
    to: EmailStr
    otp: str
    full_name: str
