from elasticsearch import Elasticsearch
import csv

mapping = {
    "properties": {
        "id": {"type": "long"},
        "brand_name": {"type": "keyword"},
        "gift_name": {"type": "text"},
    }
}

brand = ['スターバックス', 'ファミリーマート', 'ミニストップ']

def main():
    es = Elasticsearch("http://elasticsearch:9200")

    if es.indices.exists(index='gifts'):
        es.indices.delete(index='gifts')
    if not es.indices.exists(index='gifts'):
        es.indices.create(index='gifts', body={"mappings": mapping})

    with open('src/data/gift.csv', encoding = "utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['ブランド名'] in brand:
                doc = {
                    "id": row['ID'],
                    "brand_name": row['ブランド名'],
                    "gift_name": row['ギフト名'],
                }
                print(doc)
                es.index(index='gifts', body=doc)

    es.close()

if __name__ == '__main__':
    main()