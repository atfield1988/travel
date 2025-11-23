"""Currency exchange rate API integration"""
import httpx
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import os
from datetime import datetime, timedelta
import json

router = APIRouter(prefix="/api/currency", tags=["currency"])

EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY", "")
BASE_URL = "https://v6.exchangerate-api.com/v6"

# Simple in-memory cache (for production, use Redis)
cache = {}
CACHE_DURATION = 3600  # 1 hour


@router.get("/rates")
async def get_exchange_rates(base: str = Query("KRW", description="Base currency code")):
    """Get current exchange rates for base currency"""
    
    cache_key = f"exchange_rates:{base}"
    current_time = datetime.now()
    
    # Check cache
    if cache_key in cache:
        cached_data, cached_time = cache[cache_key]
        if (current_time - cached_time).total_seconds() < CACHE_DURATION:
            return cached_data
    
    if not EXCHANGE_API_KEY:
        # Return mock data if API key not configured
        return {
            "base": base,
            "updated_at": current_time.isoformat(),
            "rates": {
                "USD": 0.00075 if base == "KRW" else 1330.0,
                "EUR": 0.00069 if base == "KRW" else 1450.0,
                "JPY": 0.11 if base == "KRW" else 9.1,
                "CNY": 0.0054 if base == "KRW" else 185.0,
                "GBP": 0.00059 if base == "KRW" else 1690.0,
            },
            "mock": True
        }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{BASE_URL}/{EXCHANGE_API_KEY}/latest/{base}")
            response.raise_for_status()
            data = response.json()
            
            result = {
                "base": base,
                "updated_at": data["time_last_update_utc"],
                "rates": {
                    "USD": data["conversion_rates"].get("USD", 0),
                    "EUR": data["conversion_rates"].get("EUR", 0),
                    "JPY": data["conversion_rates"].get("JPY", 0),
                    "CNY": data["conversion_rates"].get("CNY", 0),
                    "GBP": data["conversion_rates"].get("GBP", 0),
                    "KRW": data["conversion_rates"].get("KRW", 0),
                },
                "mock": False
            }
            
            # Update cache
            cache[cache_key] = (result, current_time)
            
            return result
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch exchange rates: {str(e)}")


@router.get("/convert")
async def convert_currency(
    amount: float = Query(..., description="Amount to convert"),
    from_currency: str = Query(..., description="Source currency code"),
    to_currency: str = Query(..., description="Target currency code")
):
    """Convert amount from one currency to another"""
    
    if not EXCHANGE_API_KEY:
        # Mock conversion for development
        mock_rates = {
            "KRW_USD": 0.00075,
            "USD_KRW": 1330.0,
            "KRW_EUR": 0.00069,
            "EUR_KRW": 1450.0,
            "KRW_JPY": 0.11,
            "JPY_KRW": 9.1,
        }
        
        rate_key = f"{from_currency}_{to_currency}"
        rate = mock_rates.get(rate_key, 1.0)
        
        return {
            "from": from_currency,
            "to": to_currency,
            "amount": amount,
            "converted_amount": round(amount * rate, 2),
            "rate": rate,
            "mock": True
        }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{BASE_URL}/{EXCHANGE_API_KEY}/pair/{from_currency}/{to_currency}/{amount}"
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "from": from_currency,
                "to": to_currency,
                "amount": amount,
                "converted_amount": round(data["conversion_result"], 2),
                "rate": data["conversion_rate"],
                "mock": False
            }
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to convert currency: {str(e)}")


@router.get("/supported")
async def get_supported_currencies():
    """Get list of supported currencies"""
    return {
        "currencies": [
            {"code": "KRW", "name": "Korean Won", "symbol": "₩"},
            {"code": "USD", "name": "US Dollar", "symbol": "$"},
            {"code": "EUR", "name": "Euro", "symbol": "€"},
            {"code": "JPY", "name": "Japanese Yen", "symbol": "¥"},
            {"code": "CNY", "name": "Chinese Yuan", "symbol": "¥"},
            {"code": "GBP", "name": "British Pound", "symbol": "£"},
        ]
    }
