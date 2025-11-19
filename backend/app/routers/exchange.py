# backend/app/routers/exchange.py
from fastapi import APIRouter, Query, HTTPException
from datetime import datetime
import httpx

from .. import schemas
from ..config import settings

router = APIRouter(prefix="/exchange", tags=["exchange"])


@router.get("/rates", response_model=schemas.ExchangeRateResponse)
async def get_rates(
    base_currency: str = Query("USD", min_length=3, max_length=3),
    target_currencies: str = Query("KRW,JPY,CNY"),
):
    """
    Get exchange rates from ExchangeRate-API
    Official docs: https://www.exchangerate-api.com/docs/overview
    """
    url = f"{settings.EXCHANGE_RATE_API_URL}/{settings.EXCHANGE_RATE_API_KEY}/latest/{base_currency}"
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, timeout=7)
        if resp.status_code != 200:
            raise HTTPException(status_code=502, detail="ExchangeRate API error")
        payload = resp.json()
    
    # Filter only requested currencies
    targets = [c.strip().upper() for c in target_currencies.split(",")]
    filtered = {
        c: payload["conversion_rates"].get(c)
        for c in targets
        if payload["conversion_rates"].get(c)
    }
    
    return schemas.ExchangeRateResponse(
        base=payload["base_code"],
        rates=filtered,
        timestamp=datetime.fromtimestamp(payload["time_last_update_unix"]),
    )
