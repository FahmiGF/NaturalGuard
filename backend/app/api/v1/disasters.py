"""NATURALGUARD AI — Disaster Events API Router."""
from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from app.database.models import DisasterEvent
from app.database.seed_data import EVENTS_SEED

router = APIRouter(prefix="/disasters", tags=["Disasters"])


@router.get("", response_model=List[DisasterEvent])
async def list_disasters(
    hazard: Optional[str] = Query(None, description="Filter by hazard type"),
    min_risk: Optional[float] = Query(None, description="Filter by minimum risk score (0-100)"),
    province: Optional[str] = Query(None, description="Filter by province"),
    is_official: Optional[bool] = Query(None, description="Filter official alerts only")
):
    """Retrieve monitored disaster events across Indonesia."""
    results = EVENTS_SEED
    if hazard:
        results = [e for e in results if e.hazard_type.value == hazard.lower()]
    if min_risk is not None:
        results = [e for e in results if e.risk_score.total_score >= min_risk]
    if province:
        results = [e for e in results if province.lower() in e.location.province.lower()]
    if is_official is not None:
        results = [e for e in results if e.is_official_alert == is_official]
    return results


@router.get("/{event_id}", response_model=DisasterEvent)
async def get_disaster_by_id(event_id: str):
    """Retrieve details for a specific disaster event."""
    for event in EVENTS_SEED:
        if event.id == event_id:
            return event
    raise HTTPException(status_code=404, detail="Disaster event not found")
