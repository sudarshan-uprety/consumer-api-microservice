from elasticsearch import Elasticsearch
from motor.motor_asyncio import AsyncIOMotorClient

from utils.variables import ELASTICSEARCH_URL, MONGODB_URL


def create_es_client():
    return Elasticsearch([ELASTICSEARCH_URL])


def create_mongo_client():
    return AsyncIOMotorClient(MONGODB_URL)
