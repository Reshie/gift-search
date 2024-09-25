from pyppeteer import launch
from pyppeteer.browser import Browser
from pyppeteer.page import Page

class PyppeteerConnector:
    async def init(self):
        self.browser: Browser = await launch(executablePath='/usr/bin/google-chrome-stable', headless=True, args=['--no-sandbox'])
        self.log = []

    async def get(self, url):
        try:
            self.page: Page = await self.browser.newPage()
            await self.page.goto(url, {'waitUntil': 'networkidle0'})
        except Exception as e:
            print(f"Network error: {e}")

    async def get_response_body(self, request_id):
        try:
            session = await self.page.target.createCDPSession()
            response = await session.send(
                'Network.getResponseBody',
                {'requestId': request_id}
            )
            await session.detach()
            return response
        except Exception as e:
            print(f"Failed to get response: {e}")
    
    async def find_elements(self, query: str):
        return await self.page.querySelectorAll(query)
        
    async def quit(self):
        await self.browser.close()