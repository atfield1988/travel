# backend/app/crud.py
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from . import models, schemas


# Users
async def get_user_by_social(
    db: AsyncSession, provider: str, social_id: str
) -> Optional[models.User]:
    result = await db.execute(
        select(models.User).where(
            and_(
                models.User.social_provider == provider,
                models.User.social_id == social_id
            )
        )
    )
    return result.scalars().first()


async def create_user(db: AsyncSession, user_in: schemas.UserCreate) -> models.User:
    user = models.User(
        social_provider=user_in.social_provider,
        social_id=user_in.social_id,
        email=user_in.email,
        display_name=user_in.display_name,
        language_code=user_in.language_code or "en",
        currency_code=user_in.currency_code or "USD",
        avatar_url=user_in.avatar_url,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


# Itineraries
async def get_itineraries(
    db: AsyncSession, user_id: int, limit: int = 10, offset: int = 0
) -> List[models.Itinerary]:
    result = await db.execute(
        select(models.Itinerary)
        .where(models.Itinerary.user_id == user_id)
        .order_by(models.Itinerary.start_date.desc())
        .limit(limit)
        .offset(offset)
    )
    return list(result.scalars().all())


async def create_itinerary(
    db: AsyncSession, user_id: int, data: schemas.ItineraryCreate
) -> models.Itinerary:
    itinerary = models.Itinerary(user_id=user_id, **data.model_dump())
    db.add(itinerary)
    await db.commit()
    await db.refresh(itinerary)
    return itinerary


async def get_itinerary(
    db: AsyncSession, itinerary_id: int, user_id: int
) -> Optional[models.Itinerary]:
    result = await db.execute(
        select(models.Itinerary).where(
            models.Itinerary.id == itinerary_id,
            models.Itinerary.user_id == user_id
        )
    )
    return result.scalars().first()


# Items
async def add_item(
    db: AsyncSession, itinerary_id: int, data: schemas.ItineraryItemCreate
) -> models.ItineraryItem:
    item = models.ItineraryItem(itinerary_id=itinerary_id, **data.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


async def get_items(
    db: AsyncSession, itinerary_id: int
) -> List[models.ItineraryItem]:
    result = await db.execute(
        select(models.ItineraryItem).where(
            models.ItineraryItem.itinerary_id == itinerary_id
        )
    )
    return list(result.scalars().all())


# Budgets
async def add_budget(
    db: AsyncSession, itinerary_id: int, data: schemas.BudgetCreate
) -> models.Budget:
    budget = models.Budget(itinerary_id=itinerary_id, **data.model_dump())
    db.add(budget)
    await db.commit()
    await db.refresh(budget)
    return budget


async def get_budgets(
    db: AsyncSession, itinerary_id: int
) -> List[models.Budget]:
    result = await db.execute(
        select(models.Budget).where(models.Budget.itinerary_id == itinerary_id)
    )
    return list(result.scalars().all())
