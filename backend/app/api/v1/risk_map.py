"""NATURALGUARD AI — Risk Map & GeoJSON API Router."""
from fastapi import APIRouter, Query
from typing import Dict, Any, Optional
from app.database.seed_data import EVENTS_SEED

router = APIRouter(prefix="/risk-map", tags=["Risk Map"])


@router.get("", response_model=Dict[str, Any])
async def get_risk_map_geojson(
    hazard: Optional[str] = Query(None, description="Filter layer by hazard type"),
    min_score: Optional[float] = Query(0.0, description="Minimum risk score threshold (0-100)")
):
    """Returns GeoJSON FeatureCollection for interactive GIS mapping of multi-hazard zones in Indonesia."""
    features = []

    for ev in EVENTS_SEED:
        if hazard and ev.hazard_type.value != hazard.lower():
            continue
        if ev.risk_score.total_score < min_score:
            continue

        # Point feature representing exact hazard observation epicenter / centroid
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [ev.location.longitude, ev.location.latitude]
            },
            "properties": {
                "id": ev.id,
                "title": ev.title,
                "hazard_type": ev.hazard_type.value,
                "province": ev.location.province,
                "regency": ev.location.regency,
                "district": ev.location.district,
                "severity": ev.severity.value,
                "risk_score": ev.risk_score.total_score,
                "probability": ev.risk_score.probability,
                "exposure": ev.risk_score.exposure,
                "confidence": ev.risk_score.confidence,
                "source": ev.source,
                "is_official": ev.is_official_alert,
                "observed_at": ev.observed_at,
                "valid_until": ev.valid_until,
                "data_quality": ev.data_quality.value,
                "parameters": ev.parameters,
                "description": ev.description
            }
        }
        features.append(feature)

    return {
        "type": "FeatureCollection",
        "metadata": {
            "title": "NATURALGUARD Multi-Hazard Geospatial Layer",
            "total_features": len(features),
            "crs": "EPSG:4326"
        },
        "features": features
    }
