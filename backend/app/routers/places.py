"""Places and tourist spots API with TourAPI integration"""
import httpx
from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
import os

router = APIRouter(prefix="/api/places", tags=["places"])

TOUR_API_KEY = os.getenv("TOUR_API_KEY", "")
BASE_URL = "http://apis.data.go.kr/B551011/KorService1"


@router.get("/popular")
async def get_popular_places(
    language: str = Query("ENG", description="KOR, ENG, JPN, CHS, CHT"),
    areaCode: Optional[str] = Query(None, description="Area code (1:Seoul, 6:Busan, etc)"),
    contentTypeId: str = Query("12", description="12(Tourist), 14(Culture), 15(Festival), 32(Hotel), 39(Food)"),
    numOfRows: int = Query(20, ge=1, le=100)
):
    """Get popular tourist spots"""
    
    if not TOUR_API_KEY:
        # Return mock data if API key not configured
        return {
            "total": 6,
            "results": [
                {
                    "id": "mock_1",
                    "title": "Gyeongbokgung Palace",
                    "title_kr": "경복궁",
                    "category": "Historical Site",
                    "address": "161 Sajik-ro, Jongno-gu, Seoul",
                    "address_kr": "서울특별시 종로구 사직로 161",
                    "mapX": 126.9770,
                    "mapY": 37.5788,
                    "image": "https://via.placeholder.com/400x300?text=Gyeongbokgung",
                    "rating": 4.8,
                    "tel": "+82-2-3700-3900"
                },
                {
                    "id": "mock_2",
                    "title": "N Seoul Tower",
                    "title_kr": "N서울타워",
                    "category": "Landmark",
                    "address": "105 Namsangongwon-gil, Yongsan-gu, Seoul",
                    "address_kr": "서울특별시 용산구 남산공원길 105",
                    "mapX": 126.9882,
                    "mapY": 37.5512,
                    "image": "https://via.placeholder.com/400x300?text=N+Seoul+Tower",
                    "rating": 4.7,
                    "tel": "+82-2-3455-9277"
                },
                {
                    "id": "mock_3",
                    "title": "Bukchon Hanok Village",
                    "title_kr": "북촌한옥마을",
                    "category": "Cultural",
                    "address": "37 Gyedong-gil, Jongno-gu, Seoul",
                    "address_kr": "서울특별시 종로구 계동길 37",
                    "mapX": 126.9850,
                    "mapY": 37.5825,
                    "image": "https://via.placeholder.com/400x300?text=Bukchon",
                    "rating": 4.6,
                    "tel": "+82-2-2148-4161"
                },
                {
                    "id": "mock_4",
                    "title": "Myeongdong Shopping Street",
                    "title_kr": "명동 쇼핑거리",
                    "category": "Shopping",
                    "address": "Myeongdong-gil, Jung-gu, Seoul",
                    "address_kr": "서울특별시 중구 명동길",
                    "mapX": 126.9850,
                    "mapY": 37.5637,
                    "image": "https://via.placeholder.com/400x300?text=Myeongdong",
                    "rating": 4.5,
                    "tel": ""
                },
                {
                    "id": "mock_5",
                    "title": "Gangnam District",
                    "title_kr": "강남",
                    "category": "Entertainment",
                    "address": "Gangnam-gu, Seoul",
                    "address_kr": "서울특별시 강남구",
                    "mapX": 127.0276,
                    "mapY": 37.4979,
                    "image": "https://via.placeholder.com/400x300?text=Gangnam",
                    "rating": 4.6,
                    "tel": ""
                },
                {
                    "id": "mock_6",
                    "title": "Insadong Street",
                    "title_kr": "인사동",
                    "category": "Cultural",
                    "address": "Insadong-gil, Jongno-gu, Seoul",
                    "address_kr": "서울특별시 종로구 인사동길",
                    "mapX": 126.9853,
                    "mapY": 37.5742,
                    "image": "https://via.placeholder.com/400x300?text=Insadong",
                    "rating": 4.5,
                    "tel": ""
                }
            ]
        }
    
    params = {
        "serviceKey": TOUR_API_KEY,
        "_type": "json",
        "MobileOS": "ETC",
        "MobileApp": "UltimateKorea",
        "contentTypeId": contentTypeId,
        "numOfRows": numOfRows,
        "arrange": "P",  # Popular order
        "langCode": language
    }
    
    if areaCode:
        params["areaCode"] = areaCode
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{BASE_URL}/areaBasedList1",
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
            
            if isinstance(items, dict):
                items = [items]
            
            results = []
            for item in items:
                results.append({
                    "id": item.get("contentid"),
                    "title": item.get("title", ""),
                    "title_kr": item.get("title", ""),
                    "category": get_category_name(item.get("cat3", "")),
                    "address": item.get("addr1", ""),
                    "address_kr": item.get("addr1", ""),
                    "mapX": float(item.get("mapx", 0)),
                    "mapY": float(item.get("mapy", 0)),
                    "image": item.get("firstimage", "") or item.get("firstimage2", ""),
                    "rating": 4.5,  # Default rating
                    "tel": item.get("tel", "")
                })
            
            return {
                "total": len(results),
                "results": results
            }
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch places: {str(e)}")


@router.get("/search")
async def search_places(
    keyword: str = Query(..., description="Search keyword"),
    language: str = Query("ENG", description="KOR, ENG, JPN, CHS, CHT"),
    areaCode: Optional[str] = Query(None, description="Area code filter"),
    contentTypeId: Optional[str] = Query(None, description="Content type filter"),
    numOfRows: int = Query(20, ge=1, le=100)
):
    """Search places by keyword"""
    
    if not TOUR_API_KEY:
        return {
            "total": 0,
            "results": [],
            "message": "API key not configured. Using mock data."
        }
    
    params = {
        "serviceKey": TOUR_API_KEY,
        "_type": "json",
        "MobileOS": "ETC",
        "MobileApp": "UltimateKorea",
        "keyword": keyword,
        "numOfRows": numOfRows,
        "langCode": language
    }
    
    if areaCode:
        params["areaCode"] = areaCode
    
    if contentTypeId:
        params["contentTypeId"] = contentTypeId
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{BASE_URL}/searchKeyword1",
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
            
            if isinstance(items, dict):
                items = [items]
            
            results = []
            for item in items:
                results.append({
                    "id": item.get("contentid"),
                    "title": item.get("title", ""),
                    "title_kr": item.get("title", ""),
                    "category": get_category_name(item.get("cat3", "")),
                    "address": item.get("addr1", ""),
                    "address_kr": item.get("addr1", ""),
                    "mapX": float(item.get("mapx", 0)),
                    "mapY": float(item.get("mapy", 0)),
                    "image": item.get("firstimage", "") or item.get("firstimage2", ""),
                    "tel": item.get("tel", "")
                })
            
            return {
                "total": len(results),
                "results": results
            }
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to search places: {str(e)}")


def get_category_name(cat3: str) -> str:
    """Convert category code to readable name"""
    categories = {
        "관광지": "Tourist Attraction",
        "문화시설": "Cultural Facility",
        "축제": "Festival",
        "숙박": "Accommodation",
        "음식점": "Restaurant",
        "쇼핑": "Shopping",
        "역사": "Historical Site"
    }
    return categories.get(cat3, "Tourist Spot")
