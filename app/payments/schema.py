from pydantic import BaseModel

from app.user.schema import UserDetails


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
    order_details: dict


class PaymentResponseSchema(BaseModel):
    id: int
    payment_id: str
    payment_method: str
    order_id: str
    user: UserDetails

    class Config:
        from_attributes = True
