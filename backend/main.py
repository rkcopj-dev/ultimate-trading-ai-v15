"""Ultimate Trading AI v15 - Main FastAPI Application"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

from api.routes_health import router as health_router
from api.routes_tradingview import router as tv_router
from api.routes_orders import router as orders_router
from core.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="Ultimate Trading AI v15",
    description="AI-Powered Trading System with Delta Exchange, TradingView & Telegram",
    version="15.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(tv_router, prefix="/webhook", tags=["tradingview"])
app.include_router(orders_router, prefix="/orders", tags=["orders"])


@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Ultimate Trading AI v15 Backend Started")
    logger.info(f"📊 Environment: {os.getenv('ENVIRONMENT', 'development')}")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 Ultimate Trading AI v15 Backend Shutdown")


@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "Ultimate Trading AI v15 is running",
        "version": "15.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=os.getenv("ENVIRONMENT") == "development"
    )
