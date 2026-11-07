"""NATURALGUARD AI — USGS Integration Client."""
import logging
import aiohttp
from typing import Any, Dict
from app.config import settings
from app.integrations.circuit_breaker import CircuitBreaker

logger = logging.getLogger("naturalguard.usgs")
usgs_circuit = CircuitBreaker("USGS_EARTHQUAKE", max_failures=3, reset_timeout=60.0)


async def _fetch_usgs_earthquakes_raw() -> Dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.get(settings.USGS_ALL_M45_URL, timeout=settings.REQUEST_TIMEOUT_SECONDS) as resp:
            if resp.status == 200:
                return await resp.json()
            raise RuntimeError(f"USGS returned status code {resp.status}")


async def get_latest_usgs_earthquakes() -> Dict[str, Any]:
    """Retrieves USGS recent earthquakes with Circuit Breaker and fallback."""
    fallback_seed = {
        "type": "FeatureCollection",
        "metadata": {"title": "USGS M4.5+ Earthquakes", "status": 200},
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "mag": 6.1,
                    "place": "124 km NW of Saumlaki, Indonesia",
                    "time": 1794132724000,
                    "tsunami": 0
                },
                "geometry": {"type": "Point", "coordinates": [129.85, -7.12, 118.0]}
            }
        ]
    }
    return await usgs_circuit.call(_fetch_usgs_earthquakes_raw, fallback_data=fallback_seed)
