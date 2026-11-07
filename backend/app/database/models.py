"""NATURALGUARD AI — Data Models & Schemas."""
from __future__ import annotations
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class HazardType(str, Enum):
    FLOOD = "flood"
    LANDSLIDE = "landslide"
    VOLCANO = "volcano"
    THUNDERSTORM = "thunderstorm"
    WIND = "wind"
    EARTHQUAKE = "earthquake"
    WILDFIRE = "wildfire"
    CYCLONE = "cyclone"


class RiskCategory(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"
    EXTREME = "extreme"


class AlertLevel(str, Enum):
    ADVISORY = "advisory"
    WATCH = "watch"
    WARNING = "warning"
    EMERGENCY = "emergency"


class DataQuality(str, Enum):
    VERIFIED = "verified"
    ESTIMATED = "estimated"
    STALE = "stale"


class LocationInfo(BaseModel):
    province: str
    regency: str
    district: Optional[str] = None
    latitude: float
    longitude: float


class RiskScoreBreakdown(BaseModel):
    probability: float = Field(..., ge=0, le=100, description="Hazard Probability P")
    severity: float = Field(..., ge=0, le=100, description="Severity Score S")
    exposure: float = Field(..., ge=0, le=100, description="Population & Infra Exposure E")
    confidence: float = Field(..., ge=0, le=100, description="Model Confidence C")
    total_score: float = Field(..., ge=0, le=100, description="R = 0.40P + 0.25S + 0.20E + 0.15C")
    category: RiskCategory


class DisasterEvent(BaseModel):
    id: str
    hazard_type: HazardType
    title: str
    description: str
    location: LocationInfo
    severity: RiskCategory
    risk_score: RiskScoreBreakdown
    source: str
    is_official_alert: bool = False
    observed_at: str
    valid_until: Optional[str] = None
    data_quality: DataQuality = DataQuality.VERIFIED
    parameters: Dict[str, Any] = Field(default_factory=dict)


class DisasterAlert(BaseModel):
    id: str
    event_id: Optional[str] = None
    hazard_type: HazardType
    alert_level: AlertLevel
    headline: str
    instruction: str
    affected_areas: List[str]
    is_official: bool = True
    risk_score: float
    confidence_score: float
    source: str
    status: str = "active"
    data_quality: DataQuality = DataQuality.VERIFIED
    issued_at: str
    expires_at: Optional[str] = None


class ForecastHorizon(BaseModel):
    horizon_label: str  # '0-6 jam (Nowcasting)', '6-24 jam', '1-3 hari', '4-7 hari', '8-14 hari', '15-30 hari'
    horizon_hours: int
    predicted_probability: float
    predicted_severity: str
    confidence: float
    summary: str
    model_version: str


class ForecastItem(BaseModel):
    hazard_type: HazardType
    region: str
    latitude: float
    longitude: float
    horizons: List[ForecastHorizon]
    last_updated: str


class PredictionVsActual(BaseModel):
    id: str
    hazard_type: HazardType
    region: str
    prediction_date: str
    predicted_risk: float
    predicted_category: str
    actual_occurred: bool
    actual_severity: str
    lead_time_hours: float
    brier_score: float
    notes: str


class DataSourceStatus(BaseModel):
    name: str
    provider: str
    hazard_coverage: List[str]
    status: str  # 'online', 'degraded', 'offline'
    latency_ms: int
    last_sync: str
    records_count: int
    data_quality: DataQuality
    circuit_breaker_state: str  # 'CLOSED', 'HALF-OPEN', 'OPEN'


class CopilotQuery(BaseModel):
    question: str
    user_location: Optional[LocationInfo] = None


class CopilotCitation(BaseModel):
    source: str
    timestamp: str
    confidence: float
    data_type: str


class CopilotResponse(BaseModel):
    answer: str
    citations: List[CopilotCitation]
    related_alerts: List[str]
    safety_guidance: str
