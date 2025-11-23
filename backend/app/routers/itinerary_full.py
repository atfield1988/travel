"""Complete Itinerary Management with Places"""
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, date
from pydantic import BaseModel

router = APIRouter(prefix="/api/itineraries", tags=["itineraries"])

# For now, use in-memory storage (replace with DB later)
itineraries_db = {}
itinerary_counter = 1


class PlaceInItinerary(BaseModel):
    id: str
    title: str
    title_kr: str
    category: str
    address: str
    mapX: float
    mapY: float
    date: str  # YYYY-MM-DD
    time: Optional[str] = None  # HH:MM
    notes: Optional[str] = None
    order: int = 0


class ItineraryBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: str  # YYYY-MM-DD
    end_date: str  # YYYY-MM-DD
    destination: str = "Seoul, Korea"


class ItineraryCreate(ItineraryBase):
    pass


class ItineraryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    destination: Optional[str] = None


class ItineraryResponse(ItineraryBase):
    id: int
    user_id: str
    places: List[PlaceInItinerary]
    created_at: str
    updated_at: str


@router.get("/")
async def list_itineraries(
    user_id: str = Query(..., description="User ID from auth token"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Get all itineraries for user"""
    
    user_itineraries = [
        itinerary for itinerary in itineraries_db.values()
        if itinerary["user_id"] == user_id
    ]
    
    # Pagination
    paginated = user_itineraries[offset:offset + limit]
    
    return {
        "total": len(user_itineraries),
        "itineraries": paginated
    }


@router.post("/", status_code=201)
async def create_itinerary(
    data: ItineraryCreate,
    user_id: str = Query(..., description="User ID from auth token")
):
    """Create new itinerary"""
    
    global itinerary_counter
    
    now = datetime.now().isoformat()
    
    new_itinerary = {
        "id": itinerary_counter,
        "user_id": user_id,
        "title": data.title,
        "description": data.description,
        "start_date": data.start_date,
        "end_date": data.end_date,
        "destination": data.destination,
        "places": [],
        "created_at": now,
        "updated_at": now
    }
    
    itineraries_db[itinerary_counter] = new_itinerary
    itinerary_counter += 1
    
    return new_itinerary


@router.get("/{itinerary_id}")
async def get_itinerary(
    itinerary_id: int,
    user_id: str = Query(..., description="User ID from auth token")
):
    """Get specific itinerary"""
    
    if itinerary_id not in itineraries_db:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    
    itinerary = itineraries_db[itinerary_id]
    
    if itinerary["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return itinerary


@router.put("/{itinerary_id}")
async def update_itinerary(
    itinerary_id: int,
    data: ItineraryUpdate,
    user_id: str = Query(..., description="User ID from auth token")
):
    """Update itinerary"""
    
    if itinerary_id not in itineraries_db:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    
    itinerary = itineraries_db[itinerary_id]
    
    if itinerary["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Update fields
    if data.title is not None:
        itinerary["title"] = data.title
    if data.description is not None:
        itinerary["description"] = data.description
    if data.start_date is not None:
        itinerary["start_date"] = data.start_date
    if data.end_date is not None:
        itinerary["end_date"] = data.end_date
    if data.destination is not None:
        itinerary["destination"] = data.destination
    
    itinerary["updated_at"] = datetime.now().isoformat()
    
    return itinerary


@router.delete("/{itinerary_id}")
async def delete_itinerary(
    itinerary_id: int,
    user_id: str = Query(..., description="User ID from auth token")
):
    """Delete itinerary"""
    
    if itinerary_id not in itineraries_db:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    
    itinerary = itineraries_db[itinerary_id]
    
    if itinerary["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    del itineraries_db[itinerary_id]
    
    return {"message": "Itinerary deleted successfully"}


# Places management within itinerary

@router.post("/{itinerary_id}/places")
async def add_place_to_itinerary(
    itinerary_id: int,
    place: PlaceInItinerary,
    user_id: str = Query(..., description="User ID from auth token")
):
    """Add place to itinerary"""
    
    if itinerary_id not in itineraries_db:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    
    itinerary = itineraries_db[itinerary_id]
    
    if itinerary["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Add place with auto-increment order
    place_dict = place.dict()
    if place_dict["order"] == 0:
        place_dict["order"] = len(itinerary["places"]) + 1
    
    itinerary["places"].append(place_dict)
    itinerary["updated_at"] = datetime.now().isoformat()
    
    return {"message": "Place added", "place": place_dict}


@router.get("/{itinerary_id}/places")
async def get_itinerary_places(
    itinerary_id: int,
    user_id: str = Query(..., description="User ID from auth token"),
    date_filter: Optional[str] = Query(None, description="Filter by date YYYY-MM-DD")
):
    """Get all places in itinerary"""
    
    if itinerary_id not in itineraries_db:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    
    itinerary = itineraries_db[itinerary_id]
    
    if itinerary["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    places = itinerary["places"]
    
    # Filter by date if provided
    if date_filter:
        places = [p for p in places if p["date"] == date_filter]
    
    # Sort by order
    places.sort(key=lambda x: x["order"])
    
    return {"places": places}


@router.delete("/{itinerary_id}/places/{place_id}")
async def remove_place_from_itinerary(
    itinerary_id: int,
    place_id: str,
    user_id: str = Query(..., description="User ID from auth token")
):
    """Remove place from itinerary"""
    
    if itinerary_id not in itineraries_db:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    
    itinerary = itineraries_db[itinerary_id]
    
    if itinerary["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Find and remove place
    original_length = len(itinerary["places"])
    itinerary["places"] = [p for p in itinerary["places"] if p["id"] != place_id]
    
    if len(itinerary["places"]) == original_length:
        raise HTTPException(status_code=404, detail="Place not found in itinerary")
    
    itinerary["updated_at"] = datetime.now().isoformat()
    
    return {"message": "Place removed successfully"}


@router.put("/{itinerary_id}/places/{place_id}/reorder")
async def reorder_place(
    itinerary_id: int,
    place_id: str,
    new_order: int = Body(..., embed=True),
    user_id: str = Query(..., description="User ID from auth token")
):
    """Reorder place in itinerary"""
    
    if itinerary_id not in itineraries_db:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    
    itinerary = itineraries_db[itinerary_id]
    
    if itinerary["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Find place and update order
    place_found = False
    for place in itinerary["places"]:
        if place["id"] == place_id:
            place["order"] = new_order
            place_found = True
            break
    
    if not place_found:
        raise HTTPException(status_code=404, detail="Place not found")
    
    # Re-sort
    itinerary["places"].sort(key=lambda x: x["order"])
    itinerary["updated_at"] = datetime.now().isoformat()
    
    return {"message": "Place reordered", "places": itinerary["places"]}
