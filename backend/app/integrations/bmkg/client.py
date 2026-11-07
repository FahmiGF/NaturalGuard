"""NATURALGUARD AI — BMKG Integration Client."""
import logging
import aiohttp
from typing import Any, Dict
from app.config import settings
from app.integrations.circuit_breaker import CircuitBreaker

logger = logging.getLogger("naturalguard.bmkg")
bmkg_circuit = CircuitBreaker("BMKG_TEWS", max_failures=3, reset_timeout=60.0)


async def _fetch_bmkg_autogempa_raw() -> Dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.get(settings.BMKG_AUTOGEMPA_URL, timeout=settings.REQUEST_TIMEOUT_SECONDS) as resp:
            if resp.status == 200:
                return await resp.json()
            raise RuntimeError(f"BMKG returned status code {resp.status}")


async def get_latest_bmkg_earthquake() -> Dict[str, Any]:
    """Retrieves latest earthquake from BMKG Open Data with Circuit Breaker and fallback."""
    fallback_seed = {
        "Infogempa": {
            "gempa": {
                "Tanggal": "07 Nov 2026",
                "Jam": "15:12:04 WIB",
                "DateTime": "2026-11-07T08:12:04+00:00",
                "Coordinates": "-7.12,129.85",
                "Lintang": "7.12 LS",
                "Bujur": "129.85 BT",
                "Magnitude": "6.1",
                "Kedalaman": "118 km",
                "Wilayah": "Laut Banda Maluku Tenggara",
                "Potensi": "Tidak berpotensi TSUNAMI",
                "Dirasakan": "III-IV Saumlaki"
            }
        }
    }
    return await bmkg_circuit.call(_fetch_bmkg_autogempa_raw, fallback_data=fallback_seed)
