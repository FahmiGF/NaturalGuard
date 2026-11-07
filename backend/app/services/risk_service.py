"""NATURALGUARD AI — Unified Disaster Risk Scoring & Multi-Hazard Correlation Service."""
from typing import Dict, List, Any
from app.database.models import RiskCategory, RiskScoreBreakdown


def calculate_risk_score(probability: float, severity: float, exposure: float, confidence: float) -> RiskScoreBreakdown:
    """Calculates unified risk score using the NaturalGuard Masterplan formula:
    R = 0.40*P + 0.25*S + 0.20*E + 0.15*C
    """
    p = max(0.0, min(100.0, probability))
    s = max(0.0, min(100.0, severity))
    e = max(0.0, min(100.0, exposure))
    c = max(0.0, min(100.0, confidence))

    total = round(0.40 * p + 0.25 * s + 0.20 * e + 0.15 * c, 1)

    if total < 20.0:
        category = RiskCategory.LOW
    elif total < 40.0:
        category = RiskCategory.MODERATE
    elif total < 60.0:
        category = RiskCategory.HIGH
    elif total < 80.0:
        category = RiskCategory.VERY_HIGH
    else:
        category = RiskCategory.EXTREME

    return RiskScoreBreakdown(
        probability=p,
        severity=s,
        exposure=e,
        confidence=c,
        total_score=total,
        category=category
    )


class MultiHazardCorrelationEngine:
    """Evaluates cascading hazards and interactions between concurrent events."""

    @staticmethod
    def evaluate_correlations(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        correlations = []
        hazards_present = {e["hazard_type"] for e in events}

        # 1. Hujan lebat / Badai + Topografi Lereng -> Peningkatan Risiko Longsor
        if ("thunderstorm" in hazards_present or "cyclone" in hazards_present) and "landslide" in hazards_present:
            correlations.append({
                "type": "CASCADING_LANDSLIDE",
                "title": "Korelasi Hujan Ekstrem & Kerentanan Longsor",
                "severity": "CRITICAL",
                "description": "Presipitasi tinggi dari sel badai/siklon mempercepat saturasi air pori tanah di zona rawan longsor Jawa Barat.",
                "action": "Tingkatkan frekuensi pemantauan ekstensometer dan evakuasi dini pemukiman di bawah tebing curam."
            })

        # 2. Hujan lebat + Hulu Sungai -> Risiko Banjir Bandang Luapan
        if "thunderstorm" in hazards_present and "flood" in hazards_present:
            correlations.append({
                "type": "COMPOUND_FLOOD",
                "title": "Korelasi Hujan Konvektif & Luapan DAS Sungai",
                "severity": "HIGH",
                "description": "Reflektivitas radar tinggi bertepatan dengan kapasitas tampung sungai kritis memicu percepatan waktu tiba banjir (*peak lag time* berkurang).",
                "action": "Aktivasi pompa stasioner dan peringatan siaga bantaran sungai."
            })

        # 3. Erupsi Gunung Api + Hujan Lebat di Puncak -> Ancaman Lahar Hujan
        if "volcano" in hazards_present and ("thunderstorm" in hazards_present or "flood" in hazards_present):
            correlations.append({
                "type": "VOLCANIC_LAHAR_RISK",
                "title": "Ancaman Aliran Lahar Hujan (Lahar Dingin)",
                "severity": "EXTREME",
                "description": "Material endapan piroklastik di lereng Semeru/Merapi berpotensi terhanyut oleh air hujan menuju aliran DAS Besuk Kobokan / Kali Bebeng.",
                "action": "Kosongkan area bantaran sungai lahar hingga radius aman 5-10 km."
            })

        # 4. Gempa Megathrust / Dangkal Bawah Laut -> Potensi Tsunami
        for e in events:
            if e["hazard_type"] == "earthquake":
                params = e.get("parameters", {})
                mag = params.get("magnitude", 0)
                depth = params.get("depth_km", 999)
                if mag >= 7.0 and depth <= 50:
                    correlations.append({
                        "type": "EARTHQUAKE_TSUNAMI_TRIGGER",
                        "title": "Pemicu Gempabumi Berpotensi Tsunami",
                        "severity": "EMERGENCY",
                        "description": f"Gempa bumi dangkal M {mag} (kedalaman {depth} km) memenuhi ambang batas evaluasi tsunami pesisir.",
                        "action": "Segera ikuti rilis resmi BMKG dan evakuasi mandiri ke tempat tinggi jika merasakan guncangan kuat > 20 detik."
                    })

        return correlations
