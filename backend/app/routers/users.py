# backend/app/routers/users.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas, deps, models

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=schemas.UserRead)
async def read_current_user(
    current_user: models.User = Depends(deps.get_current_user),
):
    return current_user


@router.put("/me", response_model=schemas.UserRead)
async def update_current_user(
    user_update: schemas.UserBase,
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    for attr, value in user_update.model_dump(exclude_unset=True).items():
        setattr(current_user, attr, value)
    await db.commit()
    await db.refresh(current_user)
    return current_user
