from typing import List, Optional

from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    index: str


class ProductVariant(BaseModel):
    size: Optional[str]
    color: Optional[str]
    stock: int = 0


class SearchResponse(BaseModel):
    id: str
    name: str
    description: str
    score: float
    price: Optional[float]
    image: Optional[List[str]]
    category: Optional[str]
    status: Optional[bool]
    type: Optional[str]
    vendor: Optional[str]
    variants: Optional[List[ProductVariant]]
    total_stock: Optional[int]
