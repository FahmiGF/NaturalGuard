"""NATURALGUARD AI — Voice Announcement Service (Indonesian TTS)."""
from datetime import datetime, timezone
from typing import Dict, Any


def generate_voice_script(alert_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generates a natural Indonesian emergency voice announcement script.
    Follows Section 11 guidelines:
    - Mentions region and time
    - States hazard type
    - Clearly distinguishes between Official Warning vs AI Estimate
    - Cites official sources and instructions
    """
    now_time = datetime.now(timezone.utc).strftime("%H lewat %M waktu Indonesia barat")
    is_official = alert_data.get("is_official", True)
    hazard = alert_data.get("hazard_type", "bencana")
    headline = alert_data.get("headline", "Peringatan Dini")
    areas = ", ".join(alert_data.get("affected_areas", ["wilayah terkait"]))
    instruction = alert_data.get("instruction", "Harap tetap waspada dan ikuti arahan petugas.")
    source = alert_data.get("source", "BMKG")

    if is_official:
        script = (
            f"Perhatian, ini adalah pengumuman resmi darurat bencana. "
            f"Pada pukul {now_time}, {source} menerbitkan {headline} untuk wilayah {areas}. "
            f"Instruksi keselamatan: {instruction} "
            f"Segera amankan diri dan pantau informasi berkala dari BPBD dan BMKG."
        )
    else:
        script = (
            f"Perhatian, sistem kecerdasan buatan NATURALGUARD mendeteksi indikasi peningkatan risiko {hazard} "
            f"untuk wilayah {areas}. "
            f"Informasi ini merupakan estimasi awal analitik model. "
            f"Masyarakat dihimbau tetap tenang, memeriksa rilis resmi BMKG, dan mengikuti arahan petugas setempat."
        )

    return {
        "text": script,
        "language": "id-ID",
        "speed": 0.95,
        "pitch": 1.0,
        "is_official": is_official,
        "hazard_type": hazard,
        "headline": headline
    }
