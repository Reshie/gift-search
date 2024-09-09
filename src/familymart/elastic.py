from elasticsearch import Elasticsearch

es = Elasticsearch("http://elasticsearch:9200")

mapping = {
	"properties": {
		"name": {"type": "text"},
		"address": {"type": "text"},
		"location": {"type": "geo_point"},
		"link": {"type": "keyword"}
	}
}

es.indices.create(index="familymart", body={"mappings": mapping})

es.close()