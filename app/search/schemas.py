from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    index: str


class SearchResponse(BaseModel):
    id: str
    name: str
    description: str
    score: float
