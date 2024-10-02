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

class ElasticClient:
    def __init__(self):
        self.es = Elasticsearch(
            ELASTIC_URL,
            http_auth=("elastic", ELASTIC_PASSWORD)
        )

    def __del__(self):
        self.es.close()

    def deleteIndex(self, index):
        if self.es.indices.exists(index=index):
            self.es.indices.delete(index=index)

    def createDocument(self, index, docs, mapping=mapping, rebuild=False):
        if rebuild and self.es.indices.exists(index=index):
            self.deleteIndex(index)
        if not self.es.indices.exists(index=index):
            self.es.indices.create(index=index, body={"mappings": mapping})

        for doc in docs:
            self.es.index(index=index, body=doc)