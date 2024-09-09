import time
import jageocoder
import requests
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch

jageocoder.init(url='https://jageocoder.info-proto.com/jsonrpc')

stores = []
target = "北海道"
url_base = "https://as.chizumaru.com"
page = 1
page_size = 100

while True:
    # HTMLの取得(GET)
    try:
        req = requests.get(f"{url_base}/famima/articleList?account=famima&kkw001={target}&pg={page}&pageSize={page_size}")
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
            "location": None,
            "link": url_base + link
        }

        try:
            loc = jageocoder.search(store["address"])
            if not loc['matched']:
                raise Exception("Address not found")
            store["location"] = {
                "lat": loc['candidates'][0]['y'],
                "lon": loc['candidates'][0]['x']
            }
        except Exception as e:
            print(f"geocoding error: {e}")

        stores.append(store)
        print(store)

    page += 1
    time.sleep(1)

print(stores)
print(f"count: {len(stores)}")

es = Elasticsearch("http://elasticsearch:9200")

for store in stores:
    es.index(index="familymart", body=store)

es.close()
