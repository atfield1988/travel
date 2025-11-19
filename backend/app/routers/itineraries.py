# backend/app/routers/itineraries.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas, crud, deps, models

router = APIRouter(prefix="/itineraries", tags=["itineraries"])


@router.get("/", response_model=List[schemas.ItineraryRead])
async def list_itineraries(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_user),
):
    return await crud.get_itineraries(db, user.id, limit=limit, offset=offset)


@router.post("/", response_model=schemas.ItineraryRead, status_code=201)
async def create_itinerary(
    data: schemas.ItineraryCreate,
    db: AsyncSession = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_user),
):
    return await crud.create_itinerary(db, user.id, data)


@router.get("/{itinerary_id}", response_model=schemas.ItineraryRead)
async def read_itinerary(
    itinerary_id: int,
    db: AsyncSession = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_user),
):
    it = await crud.get_itinerary(db, itinerary_id, user.id)
    if not it:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return it
