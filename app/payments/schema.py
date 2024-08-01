from pydantic import BaseModel

from app.user.schema import UserDetails


class PaymentSchema(BaseModel):
    payment_id: str
    payment_method: str
    order_id: str

    class Config:
        from_attributes = True


class PaymentResponseSchema(BaseModel):
    id: int
    payment_id: str
    payment_method: str
    order_id: str
    user: UserDetails

    class Config:
        from_attributes = True
