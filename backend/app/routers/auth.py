# backend/app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
from datetime import datetime, timedelta
from jose import jwt

from .. import schemas, crud, deps
from ..config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


def _create_jwt(user_id: int, expires_delta: timedelta):
    to_encode = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + expires_delta
    }
    return jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )


@router.post("/google", response_model=schemas.Token)
async def google_login(
    request: Request,
    db: AsyncSession = Depends(deps.get_db),
    code: str = None,
):
    """
    Exchange Google authorization code for JWT tokens
    """
    if not code:
        raise HTTPException(status_code=400, detail="code is required")
    
    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": str(request.base_url) + "auth/google/callback",
        "grant_type": "authorization_code",
    }
    
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(token_url, data=payload, timeout=10)
        if token_resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Invalid authorization code")
        token_data = token_resp.json()
        
        # Decode ID token
        id_token = token_data["id_token"]
        id_info = jwt.decode(
            id_token,
            options={"verify_signature": False},
        )
    
    # Get or create user
    social_id = id_info["sub"]
    email = id_info.get("email")
    display_name = id_info.get("name")
    avatar_url = id_info.get("picture")
    
    user = await crud.get_user_by_social(db, "google", social_id)
    if not user:
        user_in = schemas.UserCreate(
            social_provider="google",
            social_id=social_id,
            email=email,
            display_name=display_name,
            avatar_url=avatar_url,
        )
        user = await crud.create_user(db, user_in)
    
    # Issue JWTs
    access_token = _create_jwt(
        user.id,
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = _create_jwt(
        user.id,
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    
    return schemas.Token(
        access_token=access_token,
        refresh_token=refresh_token
    )
