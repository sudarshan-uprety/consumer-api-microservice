from typing import Optional

from pydantic import BaseModel, EmailStr


class ProductItem(BaseModel):
    product_id: str
    quantity: int
    size: Optional[str] = None
    color: Optional[str] = None


class ReduceQuantityEvent(BaseModel):
    trace_id: str
    event_name: str
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


class OrderEventEmail(BaseModel):
    trace_id: str
    event_name: str
    to: EmailStr
    product: list[ProductItem]
    total_price: float
    vendor_name: str
