"""NATURALGUARD AI — Copilot Assistant & Voice API Router."""
from fastapi import APIRouter, Query
from typing import Dict, Any, Optional
from app.database.models import CopilotQuery, CopilotResponse
from app.database.seed_data import EVENTS_SEED, ALERTS_SEED, FORECAST_SEED
from app.services.copilot_service import NaturalGuardCopilot
from app.services.voice_service import generate_voice_script

router = APIRouter(prefix="/copilot", tags=["Copilot & Voice"])
copilot_engine = NaturalGuardCopilot(EVENTS_SEED, ALERTS_SEED, FORECAST_SEED)


@router.post("/chat", response_model=CopilotResponse)
async def chat_with_copilot(query: CopilotQuery):
    """Ask NaturalGuard AI Assistant questions regarding active hazards, weather, and safety protocols."""
    return copilot_engine.process_query(query.question)


@router.get("/voice-script", response_model=Dict[str, Any])
async def get_emergency_voice_script(
    alert_id: Optional[str] = Query(None, description="Optional alert ID to generate announcement for")
):
    """Retrieve an Indonesian voice script formatted for Text-to-Speech (TTS) emergency broadcasting."""
    target_alert = ALERTS_SEED[0]  # default to highest priority alert
    if alert_id:
        for a in ALERTS_SEED:
            if a.id == alert_id:
                target_alert = a
                break

    alert_dict = target_alert.model_dump()
    return generate_voice_script(alert_dict)
