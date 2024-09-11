from src.utils.selenium_connector import SeleniumConnector
import time
import json

class StarbucksConnector(SeleniumConnector):
    def __init__(self):
        super().__init__()

    def get_log(self):
        try:
            self.get("https://store.starbucks.co.jp/pref/tokyo/")
            logs = self.driver.get_log('performance')
            for entry in logs:
                message_data = json.loads(entry['message'])['message']
                if '/storesearch?' in str(message_data):
                    # print(entry)
                    # print("-" * 50)
                    if 'Network.responseReceived' == message_data['method']:
                        print(f"requestId: {message_data["params"]["requestId"]}")
                        res = self.driver('Network.getResponseBody', {'requestId': message_data["params"]["requestId"]})
                        print("-" * 50)
                # リクエスト情報が存在する場合のみ処理
                # if 'request' in message_data:
                #     request_data = message_data['request']
                #     request_url = request_data['url']
                #     request_headers = request_data['headers']

                #     if '/storesearch?' not in request_url:
                #         continue

                #     # ボディを取得
                #     if 'postData' in request_data:
                #         post_data = request_data['postData']
                #     else:
                #         post_data = None

                #     print(f"URL: {request_url}")
                #     print(f"Headers: {request_headers}")
                #     print(f"Body: {post_data}")
                #     print("-" * 50)
                #     print(f"Raw: {entry}")
        except Exception as e:
            print(e)


connector = StarbucksConnector()
connector.get_log()
time.sleep(1)
connector.quit()