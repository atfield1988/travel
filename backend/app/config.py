# backend/app/config.py
import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Core
    PROJECT_NAME: str = "UltimateKorea API"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = Field(
        default="postgresql://ultimatekorea:ultimatekorea@localhost:5432/ultimatekorea_db",
        env="DATABASE_URL"
    )
    
    # JWT & Authentication (for testing - optional)
    SECRET_KEY: str = Field(
        default="test-secret-key-change-in-production-min-32-chars",
        env="SECRET_KEY"
    )
    JWT_SECRET_KEY: Optional[str] = Field(
        default=None,
        env="JWT_SECRET_KEY"
    )
    ALGORITHM: str = Field(
        default="HS256",
        env="ALGORITHM"
    )
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        env="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # OAuth (Optional for testing - commented out for now)
    GOOGLE_CLIENT_ID: Optional[str] = Field(
        default=None,
        env="GOOGLE_CLIENT_ID"
    )
    GOOGLE_CLIENT_SECRET: Optional[str] = Field(
        default=None,
        env="GOOGLE_CLIENT_SECRET"
    )
    
    # External APIs
    TOUR_API_KEY: str = Field(
        default="c745faba8eea6de1385f50ed9370cdf9eb0decd5df2f09c22a338bdb6e02b32a",
        env="TOUR_API_KEY"
    )
    KAKAO_REST_API_KEY: str = Field(
        default="fa7c31d05cde8de2056e916709884cfc",
        env="KAKAO_REST_API_KEY"
    )
    EXCHANGE_RATE_API_KEY: Optional[str] = Field(
        default=None,
        env="EXCHANGE_RATE_API_KEY"
    )
    EXCHANGE_RATE_API_URL: str = "https://v6.exchangerate-api.com/v6"
    
    # Redis (Optional for caching)
    REDIS_HOST: str = Field(
        default="localhost",
        env="REDIS_HOST"
    )
    REDIS_PORT: int = Field(
        default=6379,
        env="REDIS_PORT"
    )
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000"
    ]
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"  # Allow extra fields from .env


settings = Settings()
