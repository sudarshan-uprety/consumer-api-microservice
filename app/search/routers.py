from typing import List

from elasticsearch import Elasticsearch, NotFoundError
from fastapi import APIRouter, Depends, HTTPException

from app.search.schemas import SearchRequest, SearchResponse, ProductVariant
from app.search.util import create_es_client, create_index_if_not_exists, index_documents, get_mongo_client, \
    get_all_documents
from utils.variables import ELASTICSEARCH_INDEX

router = APIRouter()


@router.post("/index_data")
async def index_data(es_client: Elasticsearch = Depends(create_es_client)):
    try:
        create_index_if_not_exists(es_client)

        mongo_db = await get_mongo_client()

        # Index products
        products = await get_all_documents(mongo_db.products)
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
            for prod in products
        ]
        index_documents(es_client, product_docs)

        return {"message": "Data indexed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search", response_model=List[SearchResponse])
async def search(
        search_request: SearchRequest,
        es_client: Elasticsearch = Depends(create_es_client)
):
    try:
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": search_request.query,
                                "fields": ["name^3", "description^2", "category", "vendor", "type"],
                                "type": "best_fields",
                                "fuzziness": "AUTO"
                            }
                        }
                    ],
                    "filter": []
                }
            },
            "highlight": {
                "fields": {
                    "name": {},
                    "description": {}
                }
            },
            "from": (search_request.page - 1) * search_request.page_size,
            "size": search_request.page_size
        }

        # Apply filters
        if search_request.category:
            body["query"]["bool"]["filter"].append({"term": {"category": search_request.category}})
        if search_request.min_price is not None or search_request.max_price is not None:
            price_filter = {"range": {"price": {}}}
            if search_request.min_price is not None:
                price_filter["range"]["price"]["gte"] = search_request.min_price
            if search_request.max_price is not None:
                price_filter["range"]["price"]["lte"] = search_request.max_price
            body["query"]["bool"]["filter"].append(price_filter)
        if search_request.size:
            body["query"]["bool"]["filter"].append(
                {"nested": {"path": "variants", "query": {"term": {"variants.size": search_request.size}}}})
        if search_request.color:
            body["query"]["bool"]["filter"].append(
                {"nested": {"path": "variants", "query": {"term": {"variants.color": search_request.color}}}})
        if search_request.vendor:
            body["query"]["bool"]["filter"].append({"term": {"vendor": search_request.vendor}})

        # Apply sorting
        if search_request.sort_by == "price_asc":
            body["sort"] = [{"price": "asc"}]
        elif search_request.sort_by == "price_desc":
            body["sort"] = [{"price": "desc"}]
        else:
            body["sort"] = ["_score"]

        result = es_client.search(index=ELASTICSEARCH_INDEX, body=body)

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
                total_stock=hit["_source"].get("total_stock")
            )
            for hit in result["hits"]["hits"]
        ]

        return search_results
    except NotFoundError:
        print(f"Index '{ELASTICSEARCH_INDEX}' not found. Creating it now.")
        create_index_if_not_exists(es_client)
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
