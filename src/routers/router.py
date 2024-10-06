import asyncio
from fastapi import APIRouter
from src.starbucks.crawl import main as starbucks_crawler
from src.familymart.crawl import main as familymart_crawler
from src.ministop.crawl import main as ministop_crawler

router = APIRouter()

@router.get("/starbucks/")
async def crawl_starbucks():
    try:
        await starbucks_crawler()
        return {"message": "Success"}
    except Exception as e:
        return {"message": f"Error: {e}"}

@router.get("/familymart/")
def crawl_familymart():
    try:
        familymart_crawler()
        return {"message": "Success"}
    except Exception as e:
        return {"message": f"Error: {e}"}

@router.get("/ministop/")
def crawl_ministop():
    try:
        ministop_crawler()
        return {"message": "Success"}
    except Exception as e:
        return {"message": f"Error: {e}"}