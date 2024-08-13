from pydantic import BaseModel


class ProductItem(BaseModel):
    product_id: str
    quantity: int


class ReduceQuantityEvent(BaseModel):
    trace_id: str
    operation: str
    product: list[ProductItem]
