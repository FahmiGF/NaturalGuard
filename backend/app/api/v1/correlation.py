"""NATURALGUARD AI — Multi-Hazard Correlation API Router."""
from fastapi import APIRouter
from typing import List, Dict, Any
from app.database.seed_data import EVENTS_SEED
from app.services.risk_service import MultiHazardCorrelationEngine

router = APIRouter(prefix="/correlation", tags=["Multi-Hazard Correlation"])


@router.get("", response_model=List[Dict[str, Any]])
async def get_multi_hazard_correlations():
    """Evaluate compound multi-hazard interactions and cascading disaster triggers."""
    events_payload = [e.model_dump() for e in EVENTS_SEED]
    return MultiHazardCorrelationEngine.evaluate_correlations(events_payload)
