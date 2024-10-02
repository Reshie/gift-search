import time
import requests
from bs4 import BeautifulSoup

from src.utils.elastic import ElasticClient
from src.utils.geocoder import getLocation

from src.constants.prefecture import pref_kanji

def main():
    url_base = "https://as.chizumaru.com"
    page_size = 100

    es = ElasticClient()
    es.deleteIndex("familymart")

    for pref in pref_kanji:
        stores = []
        page = 1

        while True:
            # HTMLの取得(GET)
            try:
                req = requests.get(f"{url_base}/famima/articleList?account=famima&kkw001={pref}&pg={page}&pageSize={page_size}")
            except Exception as e:
                print(f"fetch error: {e}")
            req.encoding = req.apparent_encoding # 日本語の文字化け防止

            # HTMLの解析
            bsObj = BeautifulSoup(req.text,"html.parser")

            # 要素の抽出
            items = bsObj.select("dl.cz_terms table.cz_result_table tbody")

            if not items:
                break

            # 整形
            for item in items:
                # data := [name, address, tel_number, opening_hours, ...]
                data = item.select("tr > td:nth-of-type(1)")
                elem = [i.get_text(strip=True).strip().replace(" ", "") for i in data]
                link = data[0].a.get('href')

                store = {
                    "name": elem[0],
                    "address": elem[1],
                    "location": getLocation(elem[1]),
                    "link": url_base + link
                }

                stores.append(store)
                print(store)
                print('-' * 50)
                time.sleep(1) # geocoding APIの制限対策

            page += 1

        print(f"count({pref}): {len(stores)}")

        es.createDocument("familymart", stores)

if __name__ == "__main__":
    main()