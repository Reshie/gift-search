from src.utils.pyppeteer_connector import PyppeteerConnector
from src.utils.elastic import ElasticClient
import asyncio
import json

def format_store_data(data):
    fields = data['fields']

    latlon = {
        "lat": fields['location'].split(',')[0], 
        "lon": fields['location'].split(',')[1]
    }

    store = {
        "name": fields['name'],
        "address": fields['address_5'],
        "location": latlon,
        "link": f"https://store.starbucks.co.jp/detail-{fields['store_id']}/"
    }

    return store

async def click_button(conn: PyppeteerConnector):
    while True:
        button = await conn.find_elements('.searching-result__show-more__button') #もっと見るボタン
        if button == []:
            break
        await conn.page.click('.searching-result__show-more__button')
        await asyncio.sleep(0.5)

async def main():
    try: 
        connector = PyppeteerConnector() # モバイルのレイアウトにする
        await connector.init()
        connector.filter = '/storesearch?'

        await connector.get(f"https://store.starbucks.co.jp/?keyword=")

        await click_button(connector)

        stores = []

        es = ElasticClient()

        stores_data_list = connector.log
        for stores_data in stores_data_list:
            items = json.loads(stores_data)['hits']['hit']
            for item in items:
                store = format_store_data(item)
                stores.append(store)
                print(store)
                print('-' * 50)

        print(f"count: {len(stores)}")
        es.createDocument("starbucks", stores, rebuild=True)

        await asyncio.sleep(3)

    except Exception as e:
        print(e)
    finally:
        await connector.quit()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())