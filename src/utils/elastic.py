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

    def delete_index(self, index):
        if self.es.indices.exists(index=index):
            self.es.indices.delete(index=index)

    def create_document(self, index, docs, mapping=mapping, rebuild=False):
        if rebuild and self.es.indices.exists(index=index):
            self.delete_index(index)
        if not self.es.indices.exists(index=index):
            self.es.indices.create(index=index, body={"mappings": mapping})

        for doc in docs:
            self.es.index(index=index, body=doc)

    def search(self, index, query):
        if not self.es.indices.exists(index=index): # インデックスが存在しない場合
            return None
        res = self.es.search(index=index, body=query)
        return res