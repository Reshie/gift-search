from elasticsearch import Elasticsearch
import os

mapping = {
	"properties": {
		"name": {"type": "text"},
		"address": {"type": "text"},
		"location": {"type": "geo_point"},
		"link": {"type": "keyword"}
	}
}

ELASTIC_URL = os.environ.get("ELASTIC_URL")
ELASTIC_PASSWORD = os.environ.get("ELASTIC_PASSWORD")

def createDocument(index, docs, rebuild=False):
    es = Elasticsearch(
        ELASTIC_URL,
        http_auth=("elastic", ELASTIC_PASSWORD)
    )

    if rebuild and es.indices.exists(index=index):
        es.indices.delete(index=index)
    if not es.indices.exists(index=index):
        es.indices.create(index=index, body={"mappings": mapping})

    for doc in docs:
        es.index(index=index, body=doc)

    es.close()