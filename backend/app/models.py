# backend/app/models.py
from sqlalchemy import (
    Column, Integer, String, Date, DateTime, Float, Text,
    ForeignKey, Enum, UniqueConstraint
)
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .db import Base


class SocialProvider(str, enum.Enum):
    google = "google"
    facebook = "facebook"
    apple = "apple"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    social_provider = Column(Enum(SocialProvider), nullable=False)
    social_id = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True, unique=True, index=True)
    display_name = Column(String(100), nullable=True)
    language_code = Column(String(10), default="en")
    currency_code = Column(String(3), default="USD")
    avatar_url = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        UniqueConstraint("social_provider", "social_id", name="uq_user_social"),
    )
    
    itineraries = relationship("Itinerary", back_populates="owner", cascade="all,delete")


class Itinerary(Base):
    __tablename__ = "itineraries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    owner = relationship("User", back_populates="itineraries")
    items = relationship("ItineraryItem", back_populates="itinerary", cascade="all,delete")
    budgets = relationship("Budget", back_populates="itinerary", cascade="all,delete")


class ItineraryItem(Base):
    __tablename__ = "itinerary_items"
    
    id = Column(Integer, primary_key=True, index=True)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id", ondelete="CASCADE"), nullable=False)
    place_name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    visit_date = Column(Date, nullable=True)
    visit_order = Column(Integer, nullable=True)
    memo = Column(Text, nullable=True)
    place_type = Column(String(50), nullable=True)
    kakao_place_id = Column(String(255), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    itinerary = relationship("Itinerary", back_populates="items")


class Budget(Base):
    __tablename__ = "budgets"
    
    id = Column(Integer, primary_key=True, index=True)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id", ondelete="CASCADE"), nullable=False)
    category = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False, default="USD")
    spent_at = Column(DateTime, nullable=False)
    description = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    itinerary = relationship("Itinerary", back_populates="budgets")
