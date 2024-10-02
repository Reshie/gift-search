from typing import TypedDict
import requests
import time

url = 'https://msearch.gsi.go.jp/address-search/AddressSearch?q='

class Location(TypedDict):
    lat: float
    lon: float

def getLocation(add) -> Location:
    for _ in range(3): # 3回までリトライ
        try:
            res = requests.get(url + add)
            res.encoding = res.apparent_encoding # 日本語の文字化け防止
            if not res:
                raise Exception("Address not found")
            loc = res.json()[0]["geometry"]["coordinates"]
            latlon : Location = {
                "lat": loc[1],
                "lon": loc[0]
            }
        except Exception as e:
            print(f"geocoding error: {e}")
            time.sleep(1)
        else:
            return latlon
    else:
        return None