"""NATURALGUARD AI — Energy Helicity Index (EHI) & Convective Wind Anomaly Engine.
Evaluates Energy Helicity Index (EHI), Storm-Relative Environmental Helicity (SREH),
and Downburst Gust Factors for Puting Beliung & Squall Lines.
"""
from typing import Dict, Any


class ExtremeWindEngine:
    """Atmospheric Helicity & Convective Vortex Anomaly Engine."""

    @staticmethod
    def calculate_ehi(cape_jkg: float, sreh_m2s2: float) -> float:
        """Energy Helicity Index (EHI):
        EHI = (CAPE * SREH) / 160,000. EHI > 1.0 suggests high tornadic / puting beliung potential.
        """
        return round((cape_jkg * sreh_m2s2) / 160000.0, 3)

    def evaluate(
        self,
        wind_speed_kmh: float,
        gust_speed_kmh: float,
        vertical_shear_0_6km_ms: float = 22.0,
        cape_jkg: float = 2300.0,
        sreh_0_3km_m2s2: float = 160.0
    ) -> Dict[str, Any]:
        """Calculates vortex anomaly probability, EHI index, and gust severity."""
        ehi = self.calculate_ehi(cape_jkg, sreh_0_3km_m2s2)
        gust_ratio = round(gust_speed_kmh / max(wind_speed_kmh, 5.0), 2)

        # 1. Kinematic shear score
        shear_score = min(100.0, (vertical_shear_0_6km_ms / 28.0) * 100.0)

        # 2. Helicity vortex potential
        ehi_score = min(100.0, (ehi / 1.5) * 100.0)

        # 3. Dynamic surface gust score
        gust_score = min(100.0, (gust_speed_kmh / 90.0) * 100.0)

        # Probability
        probability = round(min(95.0, (ehi_score * 0.40) + (gust_score * 0.35) + (shear_score * 0.25)), 1)
        severity = round(min(100.0, gust_score), 1)

        # Indonesian classification (Puting Beliung / Angin Kencang Lokal)
        if ehi >= 1.0 and gust_speed_kmh >= 63.0:
            classification = "POTENSI_PUTING_BELIUNG_SIGNIFIKAN (Severe Tornadic Vortex)"
        elif gust_speed_kmh >= 50.0:
            classification = "ANGIN_KENCANG_DOWNBURST (Convective Microburst)"
        else:
            classification = "ANGIN_GUST_MODERAT (Local Strong Gust)"

        return {
            "hazard": "wind",
            "model_name": "EHI-SREH-ConvectiveVortex-v3.0",
            "probability": probability,
            "severity_score": severity,
            "gust_speed_kmh": gust_speed_kmh,
            "gust_ratio": gust_ratio,
            "energy_helicity_index_ehi": ehi,
            "sreh_m2s2": sreh_0_3km_m2s2,
            "vertical_shear_ms": vertical_shear_0_6km_ms,
            "phenomenon_classification": classification,
            "meteorological_disclaimer": (
                "Puting beliung di Indonesia berskala mikro-alfa; "
                "sistem menyajikan estimasi probabilitas dinamika atmosfer."
            ),
            "confidence": 76.0
        }
