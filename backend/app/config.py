# backend/app/config.py
import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Core
    PROJECT_NAME: str = "Travel Planner API"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    
    # JWT
    JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # OAuth
    GOOGLE_CLIENT_ID: str = Field(..., env="GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = Field(..., env="GOOGLE_CLIENT_SECRET")
    
    # External APIs
    KAKAO_REST_API_KEY: str = Field(..., env="KAKAO_REST_API_KEY")
    EXCHANGE_RATE_API_KEY: str = Field(..., env="EXCHANGE_RATE_API_KEY")
    EXCHANGE_RATE_API_URL: str = "https://v6.exchangerate-api.com/v6"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
