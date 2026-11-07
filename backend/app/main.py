"""NATURALGUARD AI — FastAPI Application Root."""
import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import settings
from app.api.v1.alerts import router as alerts_router
from app.api.v1.disasters import router as disasters_router
from app.api.v1.forecast import router as forecast_router
from app.api.v1.hazards import router as hazards_router
from app.api.v1.risk_map import router as risk_map_router
from app.api.v1.copilot import router as copilot_router
from app.api.v1.data_sources import router as data_sources_router
from app.api.v1.evaluation import router as evaluation_router
from app.api.v1.correlation import router as correlation_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("naturalguard-ai")

STATIC_DIR = Path(__file__).resolve().parent / "static"

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=(
        "NATURALGUARD AI — Multi-Hazard Early Warning & Natural Disaster Monitoring Platform. "
        "Menggabungkan data cuaca BMKG, BNPB InaRISK, PVMBG MAGMA, USGS, NASA FIRMS, "
        "Machine Learning Anomaly Detection, serta RAG Copilot dan Indonesian Voiceover."
    ),
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for external frontend or local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API v1 Routers
app.include_router(alerts_router, prefix=settings.API_V1_STR)
app.include_router(disasters_router, prefix=settings.API_V1_STR)
app.include_router(forecast_router, prefix=settings.API_V1_STR)
app.include_router(hazards_router, prefix=settings.API_V1_STR)
app.include_router(risk_map_router, prefix=settings.API_V1_STR)
app.include_router(copilot_router, prefix=settings.API_V1_STR)
app.include_router(data_sources_router, prefix=settings.API_V1_STR)
app.include_router(evaluation_router, prefix=settings.API_V1_STR)
app.include_router(correlation_router, prefix=settings.API_V1_STR)

# Mount static directory for the Command Center Dashboard
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", include_in_schema=False)
async def serve_index():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {
        "status": "online",
        "platform": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
        "api": settings.API_V1_STR
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "system": "NATURALGUARD AI Core",
        "circuit_breaker": "ACTIVE",
        "timestamp": "2026-11-07T22:30:00Z"
    }
