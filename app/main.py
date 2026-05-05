from fastapi import FastAPI

from app.api.analytics import router as analytics_router
from app.api.assets import router as assets_router
from app.api.data import router as data_router
from app.api.data_sources import router as data_sources_router

app = FastAPI(
    title="Financial Market Data Warehouse",
    version="0.1.0",
)

app.include_router(assets_router)
app.include_router(data_sources_router)
app.include_router(data_router)
app.include_router(analytics_router)


@app.get("/")
def root():
    return {
        "message": "Financial Market Data Warehouse API",
        "status": "running",
    }
