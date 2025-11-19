# backend/app/routers/budgets.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas, crud, deps, models

router = APIRouter(prefix="/itineraries/{itinerary_id}/budgets", tags=["budgets"])


async def _verify_owner(
    itinerary_id: int,
    db: AsyncSession,
    user: models.User
):
    it = await crud.get_itinerary(db, itinerary_id, user.id)
    if not it:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return it


@router.get("/", response_model=List[schemas.BudgetRead])
async def list_budgets(
    itinerary_id: int,
    db: AsyncSession = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_user),
):
    await _verify_owner(itinerary_id, db, user)
    return await crud.get_budgets(db, itinerary_id)


@router.post("/", response_model=schemas.BudgetRead, status_code=201)
async def create_budget(
    itinerary_id: int,
    data: schemas.BudgetCreate,
    db: AsyncSession = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_user),
):
    await _verify_owner(itinerary_id, db, user)
    return await crud.add_budget(db, itinerary_id, data)
