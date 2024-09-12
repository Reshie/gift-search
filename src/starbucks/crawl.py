from src.utils.selenium_connector import SeleniumConnector
from src.utils.geocoder import Location
from src.utils.elastic import createDocument
from src.constants.prefecture import pref_romaji
import time
import json

def get_stores_data(conn: SeleniumConnector):
    response_body = []
    logs = conn.driver.get_log('performance')

    for entry in logs:
        message_data = json.loads(entry['message'])['message']
        method = message_data['method']
        if 'Network.responseReceived' == method and '/storesearch?' in str(message_data):
            request_id = message_data['params']['requestId']
            response_body.append(conn.get_response_body(request_id))

    return response_body

def format_store_data(data):
    fields = data['fields']

    latlon : Location = {
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

def click_button(conn: SeleniumConnector):
    while True:
        button = conn.find_elements('searching-result__show-more__button') #もっと見るボタン
        if button == []:
            break
        conn.driver.execute_script("arguments[0].click();", button[0])
        time.sleep(0.5)

def main():
    try: 
        connector = SeleniumConnector()
        connector.driver.set_window_size(800,1080) # モバイルのレイアウトにする

        for pref in pref_romaji:
            connector.get(f"https://store.starbucks.co.jp/pref/{pref}/")

            click_button(connector)

            stores = []

            stores_data_list = get_stores_data(connector)
            for stores_data in stores_data_list:
                items = json.loads(stores_data['value']['body'])['hits']['hit']
                for item in items:
                    store = format_store_data(item)
                    stores.append(store)
                    print(store)
                    print('-' * 50)

            print(f"count({pref}): {len(stores)}")
            createDocument("starbucks", stores)

            time.sleep(3)

    except Exception as e:
        print(e)
    finally:
        connector.quit()

if __name__ == '__main__':
    main()