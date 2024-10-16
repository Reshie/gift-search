from src.utils.elastic import ElasticClient
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
    es = ElasticClient()
    docs = []
    table = str.maketrans({'\u3000': ' '}) # 全角スペースを削除

    with open('src/data/gift.csv', encoding = "utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['ブランド名'] in brand:
                doc = {
                    "id": row['ID'],
                    "brand_name": row['ブランド名'],
                    "gift_name": row['ギフト名'].translate(table),
                }
                print(doc)
                docs.append(doc)

        es.create_document("gifts", docs, mapping=mapping, rebuild=True)

if __name__ == '__main__':
    main()