from typing import List

from pydantic import BaseModel


class ProductOrder(BaseModel):
    product_id: str
    quantity: int
    price_per_item: float


class OrderBase(BaseModel):
    products: List[ProductOrder]
    delivery_address: str
    order_notes: str
