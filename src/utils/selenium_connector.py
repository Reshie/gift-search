from selenium import webdriver
from selenium.webdriver.common.by import By

class SeleniumConnector:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        self.driver = webdriver.Remote(
            command_executor = 'http://selenium:4444/wd/hub',
            options = options
            )
        self.driver.implicitly_wait(10)

    def get(self, url):
        try:
            self.driver.get(url)
        except Exception as e:
            print(f"Network error: {e}")

    def get_response_body(self, request_id):
        try:
            response = self.driver.execute(
                driver_command='executeCdpCommand',
                params={
                    'cmd': 'Network.getResponseBody',
                    'params': {'requestId': request_id}
                }
            )
        except Exception as e:
            print(f"Failed to get response: {e}")
        return response
    
    def find_elements(self, class_name: str):
        return self.driver.find_elements(By.CLASS_NAME, class_name)

    def quit(self):
        self.driver.quit()