"""NATURALGUARD AI — Configuration Module."""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "NATURALGUARD AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # External APIs
    BMKG_AUTOGEMPA_URL: str = "https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json"
    BMKG_M5_URL: str = "https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json"
    USGS_SIGNIFICANT_URL: str = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_month.geojson"
    USGS_ALL_M45_URL: str = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_week.geojson"
    
    # Reliability & Cache
    REQUEST_TIMEOUT_SECONDS: int = 6
    CIRCUIT_BREAKER_MAX_FAILURES: int = 3
    CACHE_TTL_SECONDS: int = 300
    
    # Host & Port
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"


settings = Settings()
