import time
import requests
from bs4 import BeautifulSoup

from src.utils.elastic import createDocument
from src.utils.geocoder import getLocation

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
            "location": getLocation(elem[1]),
            "link": url_base + link
        }

        stores.append(store)
        print(store)

    page += 1
    time.sleep(1)

print(f"count: {len(stores)}")

createDocument("familymart", stores)