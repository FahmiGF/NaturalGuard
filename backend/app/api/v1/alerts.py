"""NATURALGUARD AI — Alerts API Router."""
from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from app.database.models import DisasterAlert
from app.database.seed_data import ALERTS_SEED

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("", response_model=List[DisasterAlert])
async def get_alerts(
    hazard: Optional[str] = Query(None, description="Filter by hazard type (flood, volcano, etc.)"),
    is_official: Optional[bool] = Query(None, description="Filter by official vs AI risk alert"),
    status: Optional[str] = Query("active", description="Alert status (active, all)")
):
    """Retrieve active disaster warnings and alerts."""
    results = ALERTS_SEED
    if hazard:
        results = [a for a in results if a.hazard_type.value == hazard.lower()]
    if is_official is not None:
        results = [a for a in results if a.is_official == is_official]
    if status != "all":
        results = [a for a in results if a.status == status]
    return results


@router.get("/{alert_id}", response_model=DisasterAlert)
async def get_alert_by_id(alert_id: str):
    """Retrieve details of a specific alert."""
    for alert in ALERTS_SEED:
        if alert.id == alert_id:
            return alert
    raise HTTPException(status_code=404, detail="Alert not found")
