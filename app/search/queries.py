from elasticsearch import Elasticsearch, NotFoundError


def create_index_if_not_exists(es_client: Elasticsearch, index: str):
    if not es_client.indices.exists(index=index):
        mapping = {
            "mappings": {
                "properties": {
                    "name": {"type": "text"},
                    "description": {"type": "text"},
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
        es_client.indices.create(index=index, body=mapping)
    else:
        pass


def search_documents(es_client: Elasticsearch, index: str, query: str):
    try:
        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["name", "description"]
                }
            }
        }
        result = es_client.search(index=index, body=body)
        return result['hits']['hits']
    except NotFoundError:
        create_index_if_not_exists(es_client, index)
        return []
