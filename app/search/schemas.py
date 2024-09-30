from typing import List, Optional, Dict, Union

from pydantic import BaseModel, Field


class ProductVariant(BaseModel):
    size: Optional[str]
    color: Optional[str]
    stock: int = 0


class StructuredSearchRequest(BaseModel):
    query: str
    category: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    size: Optional[str] = None
    color: Optional[str] = None
    vendor: Optional[str] = None
    sort_by: str = Field("relevance", pattern="^(relevance|price_asc|price_desc)$")
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


class SearchRequest(BaseModel):
    search: Union[str, StructuredSearchRequest]
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


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
    highlights: Dict[str, List[str]]
