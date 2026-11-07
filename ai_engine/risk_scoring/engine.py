"""NATURALGUARD AI — Advanced Calibrated Multi-Hazard Risk Scoring Engine.
Implements Platt Probability Calibration, Dynamic Exposure Weighting,
and Rigorous Multi-Hazard Categorization.
"""
import math
from typing import Dict, Any, Optional


class UnifiedRiskScoringEngine:
    """Scientific Multi-Hazard Risk Scoring & Probability Calibration Engine.
    Formula: R = w_p * P_cal + w_s * S + w_e * E + w_c * C
    Baseline: w_p = 0.40, w_s = 0.25, w_e = 0.20, w_c = 0.15
    """

    CATEGORIES = [
        (20.0, "Low", "#10B981", "Pemantauan rutin dan pembaruan sensor berkala."),
        (40.0, "Moderate", "#3B82F6", "Tingkatkan frekuensi polling sensor dan briefing internal."),
        (60.0, "High", "#F59E0B", "Siagakan tim lapangan, notifikasi analis, dan rilis peringatan waspada."),
        (80.0, "Very High", "#F97316", "Aktivasi posko siaga bencana dan koordinasi langsung dengan BPBD/BMKG."),
        (100.0, "Extreme", "#EF4444", "Peringatan darurat, evakuasi segera warga pada radius KRB/bantaran bahaya.")
    ]

    # Hazard-specific calibrated weighting matrix
    HAZARD_WEIGHTS = {
        "flood": {"p": 0.40, "s": 0.25, "e": 0.20, "c": 0.15},
        "landslide": {"p": 0.42, "s": 0.28, "e": 0.18, "c": 0.12},
        "volcano": {"p": 0.35, "s": 0.35, "e": 0.15, "c": 0.15},
        "thunderstorm": {"p": 0.45, "s": 0.25, "e": 0.15, "c": 0.15},
        "wind": {"p": 0.42, "s": 0.28, "e": 0.18, "c": 0.12},
        "earthquake": {"p": 0.30, "s": 0.40, "e": 0.20, "c": 0.10},
        "wildfire": {"p": 0.38, "s": 0.27, "e": 0.20, "c": 0.15},
        "cyclone": {"p": 0.40, "s": 0.30, "e": 0.18, "c": 0.12},
    }

    @staticmethod
    def platt_calibrate(raw_prob: float, a: float = -0.052, b: float = 2.6) -> float:
        """Platt scaling sigmoidal calibration to correct over/under-confidence:
        P_cal = 1 / (1 + exp(A * raw_P + B))
        """
        p = max(0.0, min(100.0, raw_prob))
        val = a * p + b
        calibrated = 1.0 / (1.0 + math.exp(max(-10.0, min(10.0, val))))
        return round(calibrated * 100.0, 1)

    @classmethod
    def compute(
        cls,
        probability: float,
        severity: float,
        exposure: float,
        confidence: float,
        hazard_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """Calculates calibrated multi-hazard risk score with confidence intervals."""
        weights = cls.HAZARD_WEIGHTS.get(hazard_type.lower() if hazard_type else "default", {"p": 0.40, "s": 0.25, "e": 0.20, "c": 0.15})
        wp, ws, we, wc = weights["p"], weights["s"], weights["e"], weights["c"]

        raw_p = min(max(float(probability), 0.0), 100.0)
        calibrated_p = cls.platt_calibrate(raw_p)

        s = min(max(float(severity), 0.0), 100.0)
        e = min(max(float(exposure), 0.0), 100.0)
        c = min(max(float(confidence), 0.0), 100.0)

        # Unified Multi-Hazard Formulation
        score = (wp * calibrated_p) + (ws * s) + (we * e) + (wc * c)
        score = round(max(0.0, min(100.0, score)), 2)

        # Standard uncertainty margin based on confidence (sigma = (100 - C) * 0.08)
        sigma = round((100.0 - c) * 0.08, 1)

        category = "Extreme"
        color = "#EF4444"
        action = "Evakuasi segera sesuai rilis resmi BPBD."
        for threshold, cat_name, cat_color, cat_action in cls.CATEGORIES:
            if score < threshold:
                category = cat_name
                color = cat_color
                action = cat_action
                break

        return {
            "formula": f"R = {wp:.2f}*P_cal + {ws:.2f}*S + {we:.2f}*E + {wc:.2f}*C",
            "weights": weights,
            "inputs": {
                "raw_probability": raw_p,
                "calibrated_probability": calibrated_p,
                "severity": s,
                "exposure": e,
                "confidence": c
            },
            "score": score,
            "uncertainty_margin": f"+/- {sigma}",
            "category": category,
            "color": color,
            "action_protocol": action
        }
