from datetime import datetime
from typing import List

from pydantic import BaseModel, EmailStr, field_validator, ValidationInfo

from app.orders.schemas import OrderBase
from utils.exceptions import GenericError


class PaymentSchema(BaseModel):
    payment_id: str
    payment_method: str
    order_id: str

    class Config:
        from_attributes = True


class TransactionDetails(BaseModel):
    transaction_code: str
    status: str
    total_amount: float
    transaction_uuid: str
    product_code: str
    signed_field_names: str
    signature: str
    order_details: OrderBase

    @field_validator('order_details')
    def validate_payment_details(cls, order_details: OrderBase, info: ValidationInfo) -> OrderBase:
        total_amount = info.data.get('total_amount')
        if total_amount is None or total_amount == 0:
            raise GenericError(
                status_code=400,
                message='Total amount cannot be zero or null',
                data=None,
                errors={"total_amount": "Total amount cannot be zero or null"}
            )
        total_sum = sum(
            product.quantity * product.price_per_item
            for product in order_details.products
        )

        if abs(total_sum - total_amount) > 0.01:
            raise GenericError(
                status_code=400,
                message='Amount is not valid.',
                data=None,
                errors={"total_amount": "Amount is not valid."}
            )
        return order_details


class PaymentResponseSchema(BaseModel):
    id: int
    payment_id: int
    payment_method: str
    payment_amount: float
    payment_status: str
    order_id: int
    delivery_address: str
    email: EmailStr
    phone_number: str

    class Config:
        from_attributes = True


class OrderProductItem(BaseModel):
    product_id: str
    name: str
    quantity: int
    price: float
    total: float


class OrderConfirmationEmailEvent(BaseModel):
    trace_id: str
    event_name: str
    to: EmailStr
    order_id: str
    full_name: str
    customer_phone: str
    delivery_address: str
    products: List[OrderProductItem]
    total_price: float
    payment_id: str
    payment_amount: float
    payment_method: str
    payment_status: str
    order_date: datetime = datetime.now()
