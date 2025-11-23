"""Tour API integration for Korea tourism data"""
import httpx
from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
import os

router = APIRouter(prefix="/api/tour", tags=["tour"])

TOUR_API_KEY = os.getenv("TOUR_API_KEY", "")
BASE_URL = "http://apis.data.go.kr/B551011/KorService1"


@router.get("/search")
async def search_tourist_spots(
    keyword: str = Query(..., description="Search keyword"),
    mapX: float = Query(..., description="Longitude"),
    mapY: float = Query(..., description="Latitude"),
    radius: int = Query(10000, description="Search radius in meters"),
    numOfRows: int = Query(10, description="Number of results"),
    contentTypeId: Optional[str] = Query(None, description="Content type: 12(관광지), 14(문화시설), 15(축제), 32(숙박), 39(음식점)")
):
    """Search tourist spots using TourAPI 4.0"""
    
    if not TOUR_API_KEY:
        raise HTTPException(status_code=500, detail="Tour API key not configured")
    
    params = {
        "serviceKey": TOUR_API_KEY,
        "_type": "json",
        "MobileOS": "ETC",
        "MobileApp": "TravelKorea",
        "mapX": mapX,
        "mapY": mapY,
        "radius": radius,
        "numOfRows": numOfRows,
        "keyword": keyword,
        "arrange": "P"  # Popular order
    }
    
    if contentTypeId:
        params["contentTypeId"] = contentTypeId
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{BASE_URL}/locationBasedList1",
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
            
            # Normalize single item to list
            if isinstance(items, dict):
                items = [items]
            
            return {
                "total": len(items),
                "results": [
                    {
                        "id": item.get("contentid"),
                        "title": item.get("title", ""),
                        "address": item.get("addr1", ""),
                        "category": item.get("cat3", ""),
                        "image": item.get("firstimage", ""),
                        "thumbnail": item.get("firstimage2", ""),
                        "mapX": float(item.get("mapx", 0)),
                        "mapY": float(item.get("mapy", 0)),
                        "tel": item.get("tel", "")
                    }
                    for item in items
                ]
            }
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch tour data: {str(e)}")


@router.get("/detail/{content_id}")
async def get_tour_detail(content_id: str):
    """Get detailed information about a tourist spot"""
    
    if not TOUR_API_KEY:
        raise HTTPException(status_code=500, detail="Tour API key not configured")
    
    params = {
        "serviceKey": TOUR_API_KEY,
        "_type": "json",
        "MobileOS": "ETC",
        "MobileApp": "TravelKorea",
        "contentId": content_id,
        "defaultYN": "Y",
        "firstImageYN": "Y",
        "addrinfoYN": "Y",
        "mapinfoYN": "Y",
        "overviewYN": "Y"
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{BASE_URL}/detailCommon1",
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
            
            if isinstance(items, list) and len(items) > 0:
                item = items[0]
            elif isinstance(items, dict):
                item = items
            else:
                raise HTTPException(status_code=404, detail="Tourist spot not found")
            
            return {
                "id": item.get("contentid"),
                "title": item.get("title", ""),
                "address": item.get("addr1", ""),
                "detailAddress": item.get("addr2", ""),
                "category": item.get("cat3", ""),
                "image": item.get("firstimage", ""),
                "thumbnail": item.get("firstimage2", ""),
                "mapX": float(item.get("mapx", 0)),
                "mapY": float(item.get("mapy", 0)),
                "tel": item.get("tel", ""),
                "homepage": item.get("homepage", ""),
                "overview": item.get("overview", ""),
                "zipcode": item.get("zipcode", "")
            }
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch detail: {str(e)}")


@router.get("/popular")
async def get_popular_spots(
    areaCode: Optional[str] = Query(None, description="Area code (1:서울, 6:부산, 32:강원 등)"),
    contentTypeId: str = Query("12", description="Content type: 12(관광지), 32(숙박), 39(음식점)"),
    numOfRows: int = Query(20, description="Number of results")
):
    """Get popular tourist spots"""
    
    if not TOUR_API_KEY:
        raise HTTPException(status_code=500, detail="Tour API key not configured")
    
    params = {
        "serviceKey": TOUR_API_KEY,
        "_type": "json",
        "MobileOS": "ETC",
        "MobileApp": "TravelKorea",
        "contentTypeId": contentTypeId,
        "numOfRows": numOfRows,
        "arrange": "P"  # Popular order
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
            
            return {
                "total": len(items),
                "results": [
                    {
                        "id": item.get("contentid"),
                        "title": item.get("title", ""),
                        "address": item.get("addr1", ""),
                        "category": item.get("cat3", ""),
                        "image": item.get("firstimage", ""),
                        "thumbnail": item.get("firstimage2", ""),
                        "mapX": float(item.get("mapx", 0)),
                        "mapY": float(item.get("mapy", 0))
                    }
                    for item in items
                ]
            }
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch popular spots: {str(e)}")
