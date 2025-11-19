# backend/app/schemas.py
from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[int] = None
    exp: Optional[int] = None


# Users
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    display_name: Optional[str] = None
    language_code: Optional[str] = "en"
    currency_code: Optional[str] = "USD"
    avatar_url: Optional[str] = None


class UserCreate(UserBase):
    social_provider: str
    social_id: str


class UserRead(UserBase):
    id: int
    
    class Config:
        from_attributes = True


# Itinerary
class ItineraryBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: date
    end_date: date
    
    @field_validator("end_date")
    @classmethod
    def end_after_start(cls, v, info):
        if "start_date" in info.data and v < info.data["start_date"]:
            raise ValueError("end_date must be after start_date")
        return v


class ItineraryCreate(ItineraryBase):
    pass


class ItineraryRead(ItineraryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ItineraryItem
class ItineraryItemBase(BaseModel):
    place_name: str
    latitude: float
    longitude: float
    visit_date: Optional[date] = None
    visit_order: Optional[int] = None
    memo: Optional[str] = None
    place_type: Optional[str] = None
    kakao_place_id: Optional[str] = None


class ItineraryItemCreate(ItineraryItemBase):
    pass


class ItineraryItemRead(ItineraryItemBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Budget
class BudgetBase(BaseModel):
    category: str
    amount: float
    currency: str = "USD"
    spent_at: datetime
    description: Optional[str] = None


class BudgetCreate(BudgetBase):
    pass


class BudgetRead(BudgetBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Search & Exchange
class PlaceResult(BaseModel):
    id: str
    name: str
    latitude: float
    longitude: float
    address: str
    phone: Optional[str] = None
    kakao_place_id: str


class ExchangeRateResponse(BaseModel):
    base: str
    rates: dict[str, float]
    timestamp: datetime
