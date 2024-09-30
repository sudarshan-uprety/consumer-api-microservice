from typing import List

from elasticsearch import Elasticsearch, NotFoundError
from fastapi import APIRouter, Depends

from app.search.schemas import SearchRequest, SearchResponse, ProductVariant, StructuredSearchRequest
from app.search.util import create_es_client, create_index_if_not_exists, index_documents, get_mongo_client, \
    get_all_documents
from utils.variables import ELASTICSEARCH_INDEX

router = APIRouter()


@router.post("/index_data")
async def index_data(es_client: Elasticsearch = Depends(create_es_client)):
    create_index_if_not_exists(es_client)
    mongo_db = await get_mongo_client()
    products = await get_all_documents(mongo_db.products)
    print(products)
    product_docs = [
        {
            "id": str(prod["_id"]),
            "name": prod["name"],
            "description": prod["description"],
            "price": prod.get("price", 0),
            "image": prod.get("image", []),
            "category": prod.get("category", ""),
            "status": prod.get("status", True),
            "type": prod.get("type", ""),
            "vendor": prod.get("vendor", ""),
            "total_stock": prod.get("total_stock", 0),
            "variants": prod.get("variants", [])
        }
        for prod in products if prod.get("status", True)  # Only index products with status=True
    ]
    index_documents(es_client, product_docs)
    return {"message": "Data indexed successfully"}


@router.post("/search", response_model=List[SearchResponse])
async def search(
        search_request: SearchRequest,
        es_client: Elasticsearch = Depends(create_es_client)
):
    try:
        if isinstance(search_request.search, str):
            # Simple search
            body = {
                "query": {
                    "multi_match": {
                        "query": search_request.search,
                        "fields": ["name^3", "description^2", "category", "vendor", "type"],
                        "type": "best_fields",
                        "fuzziness": "AUTO"
                    }
                }
            }
        else:
            # Structured search
            structured_request: StructuredSearchRequest = search_request.search
            body = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "multi_match": {
                                    "query": structured_request.query,
                                    "fields": ["name^3", "description^2", "category", "vendor", "type"],
                                    "type": "best_fields",
                                    "fuzziness": "AUTO"
                                }
                            }
                        ],
                        "filter": []
                    }
                }
            }

            # Apply filters (similar to your original code)
            if structured_request.category:
                body["query"]["bool"]["filter"].append({"term": {"category": structured_request.category}})
            # ... (add other filters)

            # Apply sorting
            if structured_request.sort_by == "price_asc":
                body["sort"] = [{"price": "asc"}]
            elif structured_request.sort_by == "price_desc":
                body["sort"] = [{"price": "desc"}]
            else:
                body["sort"] = ["_score"]

        # Add pagination
        body["from"] = (search_request.page - 1) * search_request.page_size
        body["size"] = search_request.page_size

        # Add highlighting
        body["highlight"] = {
            "fields": {
                "name": {},
                "description": {}
            }
        }
        result = es_client.search(index=ELASTICSEARCH_INDEX, body=body)
        # Process results (similar to your original code)
        search_results = [
            SearchResponse(
                id=hit["_id"],
                name=hit["_source"]["name"],
                description=hit["_source"]["description"],
                score=hit["_score"],
                price=hit["_source"].get("price"),
                image=hit["_source"].get("image"),
                category=hit["_source"].get("category"),
                status=hit["_source"].get("status"),
                type=hit["_source"].get("type"),
                vendor=hit["_source"].get("vendor"),
                variants=[ProductVariant(**variant) for variant in hit["_source"].get("variants", [])],
                total_stock=hit["_source"].get("total_stock"),
                highlights={
                    "name": hit.get("highlight", {}).get("name", []),
                    "description": hit.get("highlight", {}).get("description", [])
                }
            )
            for hit in result["hits"]["hits"]
        ]
        return search_results

    except NotFoundError:
        create_index_if_not_exists(es_client)
        return []
