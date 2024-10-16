from fastapi import APIRouter
from src.utils.elastic import ElasticClient
from src.constants.brand import brand_ja
from src.utils.geocoder import get_location
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

@router.post("/search/")
def search_gifts(address, distance=0.5):
    es = ElasticClient()
    gift_brand = ['starbucks', 'familymart', 'ministop']
    result = []

    location = get_location(address)
    if not location:
        return result
    
    query = {
        "query": {
            "geo_distance": {
                "distance": f"{distance}km",
                "location": {
                    "lat": location["lat"],
                    "lon": location["lon"]
                }
            }
        }
    }

    for brand in gift_brand:
        res = es.search(brand, query)
        if not res:
            continue
        if res["hits"]["total"]["value"] > 0:
            query_gift = {
                "query": {
                    "match": {
                        "brand_name": brand_ja[brand]
                    }
                }
            }
            res_gift = es.search("gifts", query_gift)
            if res_gift:
                res_gift = res_gift["hits"]["hits"]
                for gifts in res_gift:
                    gift = gifts["_source"]
                    result.append(f"{gift['brand_name']} {gift['gift_name']}")
    
    return result