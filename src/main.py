from src.utils.pyppeteer_connector import PyppeteerConnector
import time
import asyncio

async def main():
    conn = PyppeteerConnector()
    try:
        await conn.init()
    except Exception as e:
        print(e)
        
    try:
        await conn.get('https://store.starbucks.co.jp/pref/hokkaido/')
        time.sleep(3)
    finally:
        await conn.quit()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())