from elasticsearch import Elasticsearch


async def search_documents(es_client: Elasticsearch, index: str, query: str):
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["name", "description"]
            }
        }
    }
    result = await es_client.search(index=index, body=body)
    return result['hits']['hits']


async def create_index_if_not_exists(es_client: Elasticsearch, index: str):
    if not await es_client.indices.exists(index=index):
        await es_client.indices.create(index=index, body={
            "mappings": {
                "properties": {
                    "name": {"type": "text"},
                    "description": {"type": "text"}
                }
            }
        })
        print(f"Index '{index}' created.")
    else:
        print(f"Index '{index}' already exists.")
