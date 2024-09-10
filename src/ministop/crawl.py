import requests
from bs4 import BeautifulSoup

from src.utils.elastic import createDocument
from src.utils.geocoder import Location

stores = []
url_base = "https://map.ministop.co.jp"

# HTMLの取得(GET)
try:
    req = requests.get(f"{url_base}/all?brands=ミニストップ")
except Exception as e:
    print(f"fetch error: {e}")
req.encoding = req.apparent_encoding # 日本語の文字化け防止

# HTMLの解析
bsObj = BeautifulSoup(req.text,"html.parser")

# 要素の抽出
items = bsObj.select("div.result__content > div.store")

print(items)

# 整形
for item in items:
    header = item.select_one("div.store__header a")
    store_name = header.get_text(strip=True)
    link = header.get('href')

    content = item.select_one("div.store__content")
    store_address = content.select_one("div.store__address").get_text(strip=True)

    latlon : Location = {
        "lat": item.get('data-lat'), 
        "lon": item.get('data-lon')
    }

    store = {
        "name": store_name,
        "address": store_address,
        "location": latlon,
        "link": url_base + link
    }

    stores.append(store)
    print(store)

print(f"count: {len(stores)}")

createDocument("ministop", stores, rebuild=True)