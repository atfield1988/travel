# backend/app/routers/search.py
from fastapi import APIRouter, Query, HTTPException
from typing import List
import httpx

from .. import schemas
from ..config import settings

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/places", response_model=List[schemas.PlaceResult])
async def search_places(
    q: str = Query(..., description="Search term (English)"),
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    language: str = Query("en"),
    limit: int = Query(15, ge=1, le=30),
):
    """
    Search places using Kakao Local Keyword API
    Official docs: https://developers.kakao.com/docs/latest/en/local/dev-guide#place-search-by-keyword
    """
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {settings.KAKAO_REST_API_KEY}"}
    params = {
        "query": q,
        "x": longitude,
        "y": latitude,
        "radius": 20000,  # 20 km
        "size": limit,
        "sort": "distance",
    }
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers, params=params, timeout=10)
        if resp.status_code != 200:
            raise HTTPException(status_code=502, detail="Kakao API error")
        data = resp.json()
    
    results = []
    for doc in data.get("documents", []):
        results.append(
            schemas.PlaceResult(
                id=doc["id"],
                name=doc["place_name"],
                latitude=float(doc["y"]),
                longitude=float(doc["x"]),
                address=doc["address_name"],
                phone=doc.get("phone"),
                kakao_place_id=doc["id"],
            )
        )
    return results
