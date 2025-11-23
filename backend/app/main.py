# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config import settings
from .db import init_db
from .routers import auth, users, itineraries, items, budgets, search, exchange
from .routers import tour, currency, kakao, delivery, places


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database
    await init_db()
    yield
    # Shutdown: cleanup if needed


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers - Original
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)
app.include_router(itineraries.router, prefix=settings.API_V1_STR)
app.include_router(items.router, prefix=settings.API_V1_STR)
app.include_router(budgets.router, prefix=settings.API_V1_STR)
app.include_router(search.router, prefix=settings.API_V1_STR)
app.include_router(exchange.router, prefix=settings.API_V1_STR)

# Routers - New integrations
app.include_router(tour.router, tags=["tour"])
app.include_router(currency.router, tags=["currency"])
app.include_router(kakao.router, tags=["kakao"])
app.include_router(delivery.router, tags=["delivery"])
app.include_router(places.router, tags=["places"])


@app.get("/")
async def root():
    return {"message": "UltimateKorea API", "docs": "/docs", "version": "2.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
