from pydantic import BaseModel


class ProductItem(BaseModel):
    product_id: str
    quantity: int


class ReduceQuantityEvent(BaseModel):
    operation: str
    product: list[ProductItem]
