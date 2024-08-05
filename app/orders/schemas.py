from typing import List

from pydantic import BaseModel


class ProductOrder(BaseModel):
    product_id: str
    quantity: int


class OrderBase(BaseModel):
    products: List[ProductOrder]
    delivery_address: str
    order_notes: str
