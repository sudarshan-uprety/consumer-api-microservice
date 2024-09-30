from typing import List, Dict, Any

from bson import ObjectId
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from motor.motor_asyncio import AsyncIOMotorClient

from utils.exceptions import GenericError
from utils.variables import ELASTICSEARCH_URL, MONGODB_DB_NAME, MONGODB_URL, ENV, ELASTIC_USERNAME, ELASTIC_PASSWORD


def create_es_client():
    data = Elasticsearch([ELASTICSEARCH_URL], http_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD), timeout=60)
    return data


def get_index_name() -> str:
    return f"{ENV.lower()}"


def create_index_if_not_exists(es_client: Elasticsearch) -> None:
    index_name = get_index_name()
    if not es_client.indices.exists(index=index_name):
        mapping = {
            "settings": {
                "analysis": {
                    "analyzer": {
                        "custom_analyzer": {
                            "type": "custom",
                            "tokenizer": "standard",
                            "filter": ["lowercase", "snowball", "edge_ngram"]
                        }
                    },
                    "filter": {
                        "edge_ngram": {
                            "type": "edge_ngram",
                            "min_gram": 1,
                            "max_gram": 20
                        }
                    }
                }
            },
            "mappings": {
                "properties": {
                    "name": {"type": "text", "analyzer": "custom_analyzer", "search_analyzer": "standard"},
                    "description": {"type": "text", "analyzer": "custom_analyzer", "search_analyzer": "standard"},
                    "price": {"type": "float"},
                    "image": {"type": "keyword"},
                    "category": {"type": "keyword"},
                    "status": {"type": "boolean"},
                    "type": {"type": "keyword"},
                    "vendor": {"type": "keyword"},
                    "total_stock": {"type": "integer"},
                    "variants": {
                        "type": "nested",
                        "properties": {
                            "size": {"type": "keyword"},
                            "color": {"type": "keyword"},
                            "stock": {"type": "integer"}
                        }
                    }
                }
            }
        }
        es_client.indices.create(index=index_name, body=mapping)
    else:
        pass
        # raise GenericError(message=f"Index {index_name} already exists", status_code=constant.RESOURCE_EXISTS)


def index_documents(es_client: Elasticsearch, documents: List[Dict[str, Any]]) -> None:
    index_name = get_index_name()
    actions = [
        {
            "_index": index_name,
            "_id": str(doc["id"]),
            "_source": serialize_document({
                "name": doc.get("name", ""),
                "description": doc.get("description", ""),
                "price": doc.get("price", 0),
                "image": doc.get("image", []),
                "category": doc.get("category", ""),  # Ensure ObjectId fields are converted
                "status": doc.get("status", True),
                "type": doc.get("type", ""),
                "vendor": doc.get("vendor", ""),
                "total_stock": doc.get("total_stock", 0),
                "variants": doc.get("variants", [])
            })
        }
        for doc in documents
    ]

    success, failed = bulk(es_client, actions, raise_on_error=False)

    if failed:
        error_messages = [f"{item['index']['_id']}: {item['index']['error']['reason']}" for item in failed]
        raise GenericError(message=f"Failed to index some documents: {', '.join(error_messages)}")


async def get_mongo_client():
    client = AsyncIOMotorClient(MONGODB_URL)
    return client[MONGODB_DB_NAME]


async def get_all_documents(collection):
    cursor = collection.find({})
    documents = await cursor.to_list(length=None)
    return documents


def serialize_document(doc):
    """Convert ObjectId to string and handle other non-serializable types."""
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            doc[key] = str(value)
        elif isinstance(value, list):
            doc[key] = [serialize_document(item) if isinstance(item, dict) else str(item) if isinstance(item,
                                                                                                        ObjectId) else item
                        for item in value]
        elif isinstance(value, dict):
            doc[key] = serialize_document(value)
    return doc
