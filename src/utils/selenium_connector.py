from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

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
        self.driver.get(url)

    def save_screenshot(self, filename):
        self.driver.save_screenshot(filename)

    def quit(self):
        self.driver.quit()