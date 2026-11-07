"""NATURALGUARD AI — Data Sources Status API Router."""
from fastapi import APIRouter
from typing import List
from app.database.models import DataSourceStatus
from app.database.seed_data import DATA_SOURCES_SEED

router = APIRouter(prefix="/data-sources", tags=["Data Sources"])


@router.get("", response_model=List[DataSourceStatus])
async def list_data_sources():
    """Retrieve health, latency, synchronization timestamps and circuit breaker states for all integrated data feeds."""
    return DATA_SOURCES_SEED
