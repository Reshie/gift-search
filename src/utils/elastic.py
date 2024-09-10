from elasticsearch import Elasticsearch

mapping = {
	"properties": {
		"name": {"type": "text"},
		"address": {"type": "text"},
		"location": {"type": "geo_point"},
		"link": {"type": "keyword"}
	}
}

def createDocument(index, docs, rebuild=False):
    es = Elasticsearch("http://elasticsearch:9200")

    if rebuild and es.indices.exists(index=index):
        es.indices.delete(index=index)
    if not es.indices.exists(index=index):
        es.indices.create(index=index, body={"mappings": mapping})

    for doc in docs:
        es.index(index=index, body=doc)

    es.close()