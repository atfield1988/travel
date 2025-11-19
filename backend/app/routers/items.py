# backend/app/routers/items.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .. import schemas, crud, deps, models

router = APIRouter(prefix="/itineraries/{itinerary_id}/items", tags=["items"])


async def _verify_owner(
    itinerary_id: int,
    db: AsyncSession,
    user: models.User,
):
    it = await crud.get_itinerary(db, itinerary_id, user.id)
    if not it:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return it


@router.get("/", response_model=List[schemas.ItineraryItemRead])
async def list_items(
    itinerary_id: int,
    db: AsyncSession = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_user),
):
    await _verify_owner(itinerary_id, db, user)
    return await crud.get_items(db, itinerary_id)


@router.post("/", response_model=schemas.ItineraryItemRead, status_code=201)
async def create_item(
    itinerary_id: int,
    data: schemas.ItineraryItemCreate,
    db: AsyncSession = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_user),
):
    await _verify_owner(itinerary_id, db, user)
    return await crud.add_item(db, itinerary_id, data)


@router.put("/{item_id}", response_model=schemas.ItineraryItemRead)
async def update_item(
    itinerary_id: int,
    item_id: int,
    data: schemas.ItineraryItemCreate,
    db: AsyncSession = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_user),
):
    await _verify_owner(itinerary_id, db, user)
    result = await db.execute(
        select(models.ItineraryItem).where(
            models.ItineraryItem.id == item_id,
            models.ItineraryItem.itinerary_id == itinerary_id,
        )
    )
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    for attr, val in data.model_dump().items():
        setattr(item, attr, val)
    await db.commit()
    await db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=204)
async def delete_item(
    itinerary_id: int,
    item_id: int,
    db: AsyncSession = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_user),
):
    await _verify_owner(itinerary_id, db, user)
    result = await db.execute(
        select(models.ItineraryItem).where(
            models.ItineraryItem.id == item_id,
            models.ItineraryItem.itinerary_id == itinerary_id,
        )
    )
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    await db.delete(item)
    await db.commit()
