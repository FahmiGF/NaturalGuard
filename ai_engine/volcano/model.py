"""NATURALGUARD AI — Advanced Volcanological Anomaly & Activity Engine.
Integrates RSAM (Real-time Seismic Amplitude Measurement), Normalized Thermal Index (NTI),
and Official PVMBG MAGMA State Rules.
"""
from typing import Dict, Any


class VolcanoMonitoringEngine:
    """Volcanological Multi-Sensor Anomaly & Official Hazard Zone Engine."""

    PVMBG_LEVELS = {
        1: {"label": "Level I (Normal)", "base_severity": 15.0, "exclusion_radius_km": 2.0, "code": "GREEN"},
        2: {"label": "Level II (Waspada)", "base_severity": 45.0, "exclusion_radius_km": 3.0, "code": "YELLOW"},
        3: {"label": "Level III (Siaga)", "base_severity": 75.0, "exclusion_radius_km": 5.0, "code": "ORANGE"},
        4: {"label": "Level IV (Awas)", "base_severity": 95.0, "exclusion_radius_km": 10.0, "code": "RED"},
    }

    @staticmethod
    def calculate_nti(mir_radiance: float, nir_radiance: float) -> float:
        """Computes Normalized Thermal Index (NTI) from satellite infrared bands:
        NTI = (MIR - NIR) / (MIR + NIR). NTI > -0.80 indicates active surface thermal anomaly.
        """
        denom = mir_radiance + nir_radiance
        if denom <= 0.0001:
            return -1.0
        return round((mir_radiance - nir_radiance) / denom, 3)

    def evaluate(
        self,
        pvmbg_level: int,
        rsam_units: float = 450.0,            # Real-time Seismic Amplitude Measurement
        volcanic_quakes_24h: int = 42,        # VA/VB vulcanian quakes
        mir_radiance: float = 0.85,           # Satellite MIR
        nir_radiance: float = 0.22,           # Satellite NIR
        ash_plume_height_m: float = 700.0
    ) -> Dict[str, Any]:
        """Calculates volcanic activity anomaly index, thermal status, and official safety zone."""
        level_info = self.PVMBG_LEVELS.get(pvmbg_level, self.PVMBG_LEVELS[2])

        # 1. Thermal Anomaly Index
        nti = self.calculate_nti(mir_radiance, nir_radiance)
        thermal_anomaly_present = nti > -0.80

        # 2. RSAM Baseline Anomaly Ratio (baseline is ~150 units for dormant volcanic duct)
        rsam_ratio = rsam_units / 150.0
        seismic_energy_score = min(100.0, (rsam_ratio * 25.0) + (volcanic_quakes_24h * 1.1))

        # 3. Overall Activity Anomaly Index
        activity_index = round(min(100.0, (seismic_energy_score * 0.65) + ((nti + 1.0) * 35.0)), 1)

        # 4. Severity is tied to official level and ash ejection dynamics
        severity = round(min(100.0, level_info["base_severity"] + (ash_plume_height_m / 1000.0) * 5.0), 1)

        return {
            "hazard": "volcano",
            "model_name": "RSAM-NTI-VolcanoAnomaly-v3.0",
            "official_status": level_info["label"],
            "alert_code": level_info["code"],
            "danger_radius_km": level_info["exclusion_radius_km"],
            "activity_anomaly_index": activity_index,
            "severity_score": severity,
            "rsam_value": rsam_units,
            "rsam_energy_ratio": round(rsam_ratio, 2),
            "normalized_thermal_index_nti": nti,
            "thermal_anomaly_detected": thermal_anomaly_present,
            "ash_plume_height_meters": ash_plume_height_m,
            "safety_directive": f"Dilarang beraktivitas dalam radius {level_info['exclusion_radius_km']} km dari kawah aktif.",
            "authority_attribution": "Pusat Vulkanologi dan Mitigasi Bencana Geologi (PVMBG - Badan Geologi ESDM)"
        }
