from typing import List, Optional

from pydantic import BaseModel


class ProductOrder(BaseModel):
    product_id: str
    quantity: int
    size: Optional[str] = None
    color: Optional[str] = None
    price_per_item: float


class OrderBase(BaseModel):
    products: List[ProductOrder]
    delivery_address: str
    order_notes: str


class OrderItem(BaseModel):
    product_id: str
    quantity: int
    price_per_item: float
    total_amount: float

    class Config:
        from_attributes = True


class UserPayment(BaseModel):
    id: int
    payment_uuid: str
    payment_method: str
    payment_amount: float
    payment_status: str

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    delivery_address: str
    status: str
    order_note: str
    payment: UserPayment
    order_items: List[OrderItem]

    class Config:
        from_attributes = True
