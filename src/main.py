from elasticsearch import Elasticsearch
import os

ELASTIC_URL = os.environ.get("ELASTIC_URL")
ELASTIC_PASSWORD = os.environ.get("ELASTIC_PASSWORD")

def main():
    es = Elasticsearch(
        ELASTIC_URL,
        basic_auth=("elastic", ELASTIC_PASSWORD)
    )

    print(es.info())

    es.close()

if __name__ == '__main__':
    main()