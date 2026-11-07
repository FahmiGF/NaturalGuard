"""NATURALGUARD AI — Forecasting Center API Router."""
from fastapi import APIRouter, Query
from typing import List, Optional
from app.database.models import ForecastItem
from app.database.seed_data import FORECAST_SEED

router = APIRouter(prefix="/forecast", tags=["Forecasting"])


@router.get("", response_model=List[ForecastItem])
async def get_hazard_forecasts(
    hazard: Optional[str] = Query(None, description="Filter by hazard type (flood, landslide, etc.)"),
    region: Optional[str] = Query(None, description="Filter by region keyword")
):
    """Retrieve multi-horizon risk outlook (Nowcasting 0-6h, Daily 6-24h, 1-3d, 4-7d, 8-14d, 15-30d)."""
    results = FORECAST_SEED
    if hazard:
        results = [f for f in results if f.hazard_type.value == hazard.lower()]
    if region:
        results = [f for f in results if region.lower() in f.region.lower()]
    return results
