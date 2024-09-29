from typing import List

from elasticsearch import Elasticsearch
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.search.queries import search_documents, create_index_if_not_exists
from app.search.schemas import SearchRequest, SearchResponse
from app.search.util import create_es_client, create_mongo_client
from utils import constant
from utils.exceptions import GenericError
from utils.variables import ENV

router = APIRouter(
    prefix="/search",
    tags=["search endpoints"],
)


@router.post("/", response_model=List[SearchResponse])
async def search(
        request: SearchRequest,
        es_client: Elasticsearch = Depends(create_es_client),
        mongo_client: AsyncIOMotorClient = Depends(create_mongo_client)
):
    if request.index not in ['product', 'category']:
        raise GenericError(status_code=constant.ERROR_BAD_REQUEST,
                           message="Index must be one of 'product' or 'category'")

    index_name = "products" if request.index == 'product' else "category"

    await create_index_if_not_exists(es_client, index_name)
    results = await search_documents(es_client, index_name, request.query)

    # Fetch additional data from MongoDB if needed
    db = mongo_client[ENV]
    collection = db[request.index + 's']

    search_responses = []
    for hit in results:
        doc_id = hit['_id']
        mongo_doc = await collection.find_one({"_id": doc_id})

        if mongo_doc:
            search_responses.append(
                SearchResponse(
                    id=str(mongo_doc['_id']),
                    name=mongo_doc.get('name', ''),
                    description=mongo_doc.get('description', ''),
                    score=hit['_score']
                )
            )

    return search_responses
