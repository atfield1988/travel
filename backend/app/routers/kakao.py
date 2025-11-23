"""Kakao Maps and Local API integration"""
import httpx
from fastapi import APIRouter, Query, HTTPException
from typing import Optional
import os

router = APIRouter(prefix="/api/kakao", tags=["kakao"])

KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY", "")


@router.get("/search/keyword")
async def search_by_keyword(
    query: str = Query(..., description="Search keyword"),
    x: Optional[float] = Query(None, description="Longitude for sorting by distance"),
    y: Optional[float] = Query(None, description="Latitude for sorting by distance"),
    radius: int = Query(20000, description="Search radius in meters (max 20000)"),
    page: int = Query(1, description="Page number"),
    size: int = Query(15, description="Results per page (max 15)")
):
    """Search places by keyword using Kakao Local API"""
    
    if not KAKAO_REST_API_KEY:
        raise HTTPException(status_code=500, detail="Kakao API key not configured")
    
    params = {
        "query": query,
        "page": page,
        "size": min(size, 15)
    }
    
    if x and y:
        params["x"] = x
        params["y"] = y
        params["radius"] = min(radius, 20000)
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                "https://dapi.kakao.com/v2/local/search/keyword.json",
                params=params,
                headers={"Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"}
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "total": data["meta"]["total_count"],
                "is_end": data["meta"]["is_end"],
                "results": [
                    {
                        "id": place["id"],
                        "name": place["place_name"],
                        "category": place["category_name"],
                        "address": place["address_name"],
                        "road_address": place.get("road_address_name", ""),
                        "phone": place.get("phone", ""),
                        "url": place.get("place_url", ""),
                        "longitude": float(place["x"]),
                        "latitude": float(place["y"]),
                        "distance": place.get("distance", "")
                    }
                    for place in data["documents"]
                ]
            }
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to search: {str(e)}")


@router.get("/search/address")
async def search_by_address(
    query: str = Query(..., description="Address to search"),
    page: int = Query(1, description="Page number"),
    size: int = Query(10, description="Results per page (max 30)")
):
    """Search address using Kakao Local API"""
    
    if not KAKAO_REST_API_KEY:
        raise HTTPException(status_code=500, detail="Kakao API key not configured")
    
    params = {
        "query": query,
        "page": page,
        "size": min(size, 30)
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                "https://dapi.kakao.com/v2/local/search/address.json",
                params=params,
                headers={"Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"}
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "total": data["meta"]["total_count"],
                "results": [
                    {
                        "address": doc["address_name"],
                        "road_address": doc.get("road_address", {}).get("address_name", ""),
                        "longitude": float(doc["x"]) if doc.get("x") else None,
                        "latitude": float(doc["y"]) if doc.get("y") else None
                    }
                    for doc in data["documents"]
                ]
            }
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to search address: {str(e)}")


@router.get("/coord-to-address")
async def coord_to_address(
    x: float = Query(..., description="Longitude"),
    y: float = Query(..., description="Latitude")
):
    """Convert coordinates to address"""
    
    if not KAKAO_REST_API_KEY:
        raise HTTPException(status_code=500, detail="Kakao API key not configured")
    
    params = {"x": x, "y": y}
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                "https://dapi.kakao.com/v2/local/geo/coord2address.json",
                params=params,
                headers={"Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"}
            )
            response.raise_for_status()
            data = response.json()
            
            if not data["documents"]:
                raise HTTPException(status_code=404, detail="Address not found for coordinates")
            
            doc = data["documents"][0]
            
            return {
                "address": doc["address"]["address_name"] if "address" in doc else "",
                "road_address": doc["road_address"]["address_name"] if "road_address" in doc else "",
                "longitude": x,
                "latitude": y
            }
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to convert coordinates: {str(e)}")


@router.get("/category")
async def search_by_category(
    category_code: str = Query(..., description="Category code (MT1:마트, FD6:음식점, CE7:카페, HP8:병원, PM9:약국)"),
    x: float = Query(..., description="Center longitude"),
    y: float = Query(..., description="Center latitude"),
    radius: int = Query(5000, description="Search radius in meters (max 20000)"),
    page: int = Query(1, description="Page number"),
    size: int = Query(15, description="Results per page (max 15)")
):
    """Search places by category"""
    
    if not KAKAO_REST_API_KEY:
        raise HTTPException(status_code=500, detail="Kakao API key not configured")
    
    params = {
        "category_group_code": category_code,
        "x": x,
        "y": y,
        "radius": min(radius, 20000),
        "page": page,
        "size": min(size, 15),
        "sort": "distance"
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                "https://dapi.kakao.com/v2/local/search/category.json",
                params=params,
                headers={"Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"}
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "total": data["meta"]["total_count"],
                "results": [
                    {
                        "id": place["id"],
                        "name": place["place_name"],
                        "category": place["category_name"],
                        "address": place["address_name"],
                        "road_address": place.get("road_address_name", ""),
                        "phone": place.get("phone", ""),
                        "url": place.get("place_url", ""),
                        "longitude": float(place["x"]),
                        "latitude": float(place["y"]),
                        "distance": int(place.get("distance", 0))
                    }
                    for place in data["documents"]
                ]
            }
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to search by category: {str(e)}")
