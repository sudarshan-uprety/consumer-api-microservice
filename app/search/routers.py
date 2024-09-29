from typing import List

from elasticsearch import Elasticsearch, NotFoundError
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from app.search.queries import search_documents, create_index_if_not_exists
from app.search.schemas import SearchRequest, SearchResponse
from app.search.util import create_es_client, create_mongo_client
from utils import constant
from utils.exceptions import GenericError

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

    index_name = request.index + "s"  # "products" or "categories"

    try:
        create_index_if_not_exists(es_client, index_name)
        results = search_documents(es_client, index_name, request.query)

        db = mongo_client["test"]
        collection = db[index_name]

        search_responses = []
        for hit in results:
            doc_id = hit['_id']
            mongo_doc = await collection.find_one({"_id": doc_id})

            if mongo_doc:
                response = SearchResponse(
                    id=str(mongo_doc['_id']),
                    name=mongo_doc.get('name', ''),
                    description=mongo_doc.get('description', ''),
                    score=hit['_score']
                )
                if index_name == "products":
                    response.price = mongo_doc.get('price')
                    response.image = mongo_doc.get('image', [])
                    response.category = str(mongo_doc['category'].id) if mongo_doc.get('category') else None
                    response.status = mongo_doc.get('status', True)
                    response.type = str(mongo_doc['type'].id) if mongo_doc.get('type') else None
                    response.vendor = str(mongo_doc['vendor'].id) if mongo_doc.get('vendor') else None
                    response.variants = [variant.to_dict() for variant in mongo_doc.get('variants', [])]
                    response.total_stock = mongo_doc.get('total_stock', 0)
                search_responses.append(response)

        return search_responses
    except NotFoundError:
        raise HTTPException(status_code=404, detail=f"Index '{index_name}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/populate_index")
async def populate_index(
        es_client: Elasticsearch = Depends(create_es_client),
        mongo_client: AsyncIOMotorClient = Depends(create_mongo_client)
):
    try:
        db = mongo_client["test"]

        for collection_name in ['products', 'categories']:
            create_index_if_not_exists(es_client, collection_name)

            collection = db[collection_name]
            documents = await collection.find().to_list(length=None)

            actions = []
            for doc in documents:
                action = {
                    "_index": collection_name,
                    "_id": str(doc["_id"]),
                    "_source": {
                        "name": doc.get("name", ""),
                        "description": doc.get("description", ""),
                        "status": doc.get("status", True)
                    }
                }
                if collection_name == "products":
                    action["_source"].update({
                        "price": doc.get("price"),
                        "image": doc.get("image", []),
                        "category": str(doc["category"].id) if doc.get("category") else None,
                        "type": str(doc["type"].id) if doc.get("type") else None,
                        "vendor": str(doc["vendor"].id) if doc.get("vendor") else None,
                        "variants": [variant.to_dict() for variant in doc.get("variants", [])],
                        "total_stock": doc.get("total_stock", 0)
                    })
                actions.append(action)

            success, failed = bulk(es_client, actions)
            print(f"Indexed {success} documents in '{collection_name}'. Failed: {len(failed)}")

        return {"message": "Indices populated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while populating indices: {str(e)}")
