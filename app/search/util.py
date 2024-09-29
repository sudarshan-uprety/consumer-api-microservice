from bson import ObjectId
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from motor.motor_asyncio import AsyncIOMotorClient

from utils.variables import ELASTICSEARCH_URL, ELASTICSEARCH_INDEX, MONGODB_DB_NAME, MONGODB_URL


def create_es_client():
    return Elasticsearch([ELASTICSEARCH_URL])


def create_index_if_not_exists(es_client: Elasticsearch):
    try:
        if not es_client.indices.exists(index=ELASTICSEARCH_INDEX):
            mapping = {
                "settings": {
                    "analysis": {
                        "analyzer": {
                            "custom_analyzer": {
                                "type": "custom",
                                "tokenizer": "standard",
                                "filter": ["lowercase", "snowball"]
                            }
                        }
                    }
                },
                "mappings": {
                    "properties": {
                        "name": {"type": "text", "analyzer": "custom_analyzer"},
                        "description": {"type": "text", "analyzer": "custom_analyzer"},
                        "status": {"type": "boolean"},
                        "price": {"type": "float"},
                        "image": {"type": "keyword", "index": False},
                        "category": {"type": "keyword"},
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
            es_client.indices.create(index=ELASTICSEARCH_INDEX, body=mapping)
            print(f"Index '{ELASTICSEARCH_INDEX}' created.")
        else:
            print(f"Index '{ELASTICSEARCH_INDEX}' already exists.")
    except Exception as e:
        print(f"Error creating index '{ELASTICSEARCH_INDEX}': {str(e)}")
        raise


def index_documents(es_client: Elasticsearch, documents):
    serialized_docs = [serialize_document(doc) for doc in documents]
    actions = [
        {
            "_index": ELASTICSEARCH_INDEX,
            "_id": doc["id"],
            "_source": doc
        }
        for doc in serialized_docs
    ]
    success, failed = bulk(es_client, actions)
    print(f"Indexed {success} documents. Failed: {len(failed)}")


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
