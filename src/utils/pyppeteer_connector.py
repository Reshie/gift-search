from pyppeteer import launch
from pyppeteer.browser import Browser
from pyppeteer.page import Page

from typing import TypedDict
import asyncio

class Log(TypedDict):
    url: str
    body: str

class PyppeteerConnector:
    async def init(self):
        self.browser: Browser = await launch(executablePath='/usr/bin/google-chrome-stable', headless=True, args=['--no-sandbox'])
        self.log = []
        self.filter = ''

    async def get(self, url):
        try:
            self.page: Page = await self.browser.newPage()
            self.page.on('response', lambda res: asyncio.ensure_future(self.store_response(res))) # ログを取得
            await self.page.goto(url, {'waitUntil': 'networkidle0'}) # ページが読み込まれるまで待つ
        except Exception as e:
            print(f"Network error: {e}")

    async def store_response(self, response):
        if self.filter in response.url:
            print(f"response was detected: {response.url}")
            body = await response.text()
            self.log.append(body)
    
    async def find_elements(self, query: str):
        return await self.page.querySelectorAll(query)
        
    async def quit(self):
        # print(self.log)
        await self.browser.close()