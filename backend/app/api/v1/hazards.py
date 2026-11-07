"""NATURALGUARD AI — Hazard Specific Centers API Router."""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.database.seed_data import EVENTS_SEED

router = APIRouter(prefix="/hazard", tags=["Hazard Centers"])


HAZARD_DESCRIPTIONS = {
    "flood": {
        "title": "Flood Prediction & River Monitoring Center",
        "primary_agencies": ["BMKG", "PUPR BBWS", "BNPB InaRISK"],
        "algorithms": ["XGBoost Inundation Classifier", "LSTM River Runoff Model"],
        "parameters_monitored": ["Water level (TMA)", "Rainfall rate (mm/h)", "Soil curve number", "Drainage capacity"]
    },
    "landslide": {
        "title": "Landslide & Slope Instability Center",
        "primary_agencies": ["PVMBG", "InaRISK BNPB", "Badan Geologi"],
        "algorithms": ["Rainfall-Slope Empirical Threshold", "Random Forest Susceptibility"],
        "parameters_monitored": ["Slope angle (>25°)", "Cumulative rain (1/3/7/14 days)", "Vegetation cover", "Extensometer"]
    },
    "volcano": {
        "title": "Volcanic Activity & Eruption Monitoring Center",
        "primary_agencies": ["PVMBG MAGMA Indonesia", "BPPTKG"],
        "algorithms": ["Isolation Forest Anomaly Detection", "Thermal Anomaly Tracking"],
        "parameters_monitored": ["Volcanic earthquakes (VA/VB)", "Tremor", "Ash column height", "Thermal hotspot", "KRB Radius"]
    },
    "thunderstorm": {
        "title": "Convective Thunderstorm & Lightning Center",
        "primary_agencies": ["BMKG Juanda/Cengkareng", "Himawari-9 Satellite"],
        "algorithms": ["Optical Flow Radar Nowcasting", "ConvLSTM Rain Rate"],
        "parameters_monitored": ["Reflectivity (dBZ)", "CAPE index", "Lightning flash rate", "Cloud top temp"]
    },
    "wind": {
        "title": "Tornado, Squall Line & Extreme Wind Center",
        "primary_agencies": ["BMKG Open Data", "AWS Surface Network"],
        "algorithms": ["Severe Convective Wind Gust Anomaly", "Vorticity Signature Model"],
        "parameters_monitored": ["Gust speed (km/h)", "Vertical wind shear", "Pressure drop rate"]
    },
    "earthquake": {
        "title": "Seismic & Tsunami Early Warning Center",
        "primary_agencies": ["BMKG TEWS", "USGS Earthquake Hazards", "InaTEWS"],
        "algorithms": ["Hypocenter Ingestion Engine", "MMI Attenuation Shaking Estimator", "Tsunami Propagation Trigger"],
        "parameters_monitored": ["Magnitude", "Depth (km)", "Fault mechanism", "MMI Felt Intensity"]
    },
    "wildfire": {
        "title": "Wildfire & Peatland Thermal Anomaly Center",
        "primary_agencies": ["NASA FIRMS", "KLHK Sipongi", "LAPAN/BRIN"],
        "algorithms": ["VIIRS 375m Spatial Clustering", "Fire Weather Index (FWI)"],
        "parameters_monitored": ["Hotspot confidence (%)", "FRP (Fire Radiative Power)", "Days without rain", "Peat depth"]
    },
    "cyclone": {
        "title": "Tropical Cyclone & Extreme Sea Hazard Center",
        "primary_agencies": ["BMKG TCWC Jakarta", "JTWC", "BoM Australia"],
        "algorithms": ["Numerical Weather Track Interpolation", "Wave Height Dispersion"],
        "parameters_monitored": ["Central pressure (hPa)", "Max wind speed (knots)", "Wave height (meters)", "SST (°C)"]
    }
}


@router.get("/{hazard_type}", response_model=Dict[str, Any])
async def get_hazard_center(hazard_type: str):
    """Retrieve full monitoring telemetry and active events for a specific hazard engine."""
    h_type = hazard_type.lower()
    if h_type not in HAZARD_DESCRIPTIONS:
        raise HTTPException(status_code=404, detail=f"Hazard engine '{hazard_type}' not found")

    events = [e for e in EVENTS_SEED if e.hazard_type.value == h_type]
    meta = HAZARD_DESCRIPTIONS[h_type]

    return {
        "hazard_type": h_type,
        "metadata": meta,
        "active_events_count": len(events),
        "events": events
    }
