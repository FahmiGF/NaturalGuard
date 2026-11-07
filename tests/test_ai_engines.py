"""NATURALGUARD AI — Unit & Boundary Tests for 8 Hazard AI Engines."""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from ai_engine.risk_scoring.engine import UnifiedRiskScoringEngine
from ai_engine.flood.model import FloodPredictionEngine
from ai_engine.landslide.model import LandslidePredictionEngine
from ai_engine.volcano.model import VolcanoMonitoringEngine
from ai_engine.thunderstorm.model import ThunderstormPredictionEngine
from ai_engine.wind.model import ExtremeWindEngine
from ai_engine.earthquake.model import EarthquakeAssessmentEngine
from ai_engine.wildfire.model import WildfireRiskEngine
from ai_engine.cyclone.model import TropicalCycloneEngine
from ai_engine.evaluation.metrics import ModelEvaluationToolkit


def test_unified_risk_scoring_boundary():
    """Verify risk scores never exceed [0, 100] across extreme inputs."""
    # Test zero
    res_zero = UnifiedRiskScoringEngine.compute(0, 0, 0, 0)
    assert 0.0 <= res_zero["score"] <= 100.0, "Zero score out of bounds"
    assert res_zero["category"] in ["Low", "Moderate"]

    # Test max
    res_max = UnifiedRiskScoringEngine.compute(100, 100, 100, 100)
    assert 0.0 <= res_max["score"] <= 100.0, "Max score out of bounds"
    assert res_max["category"] == "Extreme"

    # Test extreme out-of-range inputs
    res_overflow = UnifiedRiskScoringEngine.compute(9999, -500, 120, -10)
    assert 0.0 <= res_overflow["score"] <= 100.0, "Overflow input handled safely"


def test_flood_engine():
    """Verify flood SCS-CN and Manning hydraulics calculations."""
    engine = FloodPredictionEngine(danger_water_level_m=4.20)
    # Normal stage
    res_normal = engine.predict(water_level_m=2.10, rainfall_3h_mm=5.0)
    assert res_normal["overflow_risk"] == "MONITORED"
    assert res_normal["probability"] < 50.0

    # Flood critical stage
    res_flood = engine.predict(water_level_m=4.85, rainfall_3h_mm=75.0)
    assert res_flood["overflow_risk"] == "CRITICAL"
    assert res_flood["overflow_depth_cm"] > 0.0
    assert 0.0 <= res_flood["probability"] <= 100.0


def test_landslide_engine():
    """Verify Infinite Slope Stability FS and Caine rainfall threshold."""
    engine = LandslidePredictionEngine()
    # Flat terrain (10 degrees)
    res_flat = engine.predict(slope_deg=10.0, cumulative_rain_3d_mm=20.0, cumulative_rain_7d_mm=50.0, rain_intensity_1h_mm=5.0)
    assert res_flat["factor_of_safety_fs"] > 1.3
    assert res_flat["probability"] < 50.0

    # Steep terrain (38 degrees) with heavy antecedent rain
    res_steep = engine.predict(slope_deg=38.0, cumulative_rain_3d_mm=180.0, cumulative_rain_7d_mm=260.0, rain_intensity_1h_mm=45.0)
    assert res_steep["factor_of_safety_fs"] < 1.3
    assert res_steep["probability"] > 60.0


def test_volcano_engine():
    """Verify RSAM and NTI infrared anomaly scoring."""
    engine = VolcanoMonitoringEngine()
    res = engine.evaluate(pvmbg_level=3, rsam_units=520.0, volcanic_quakes_24h=55, mir_radiance=1.1, nir_radiance=0.15)
    assert res["official_status"] == "Level III (Siaga)"
    assert res["thermal_anomaly_detected"] is True
    assert res["danger_radius_km"] == 5.0


def test_thunderstorm_engine():
    """Verify Marshall-Palmer rain rate and CAPE nowcasting."""
    engine = ThunderstormPredictionEngine()
    res = engine.predict(radar_dbz=54.0, cape_jkg=2600.0, lifted_index_c=-5.8, vil_kg_m2=44.0, lightning_strikes_1h=350)
    assert res["estimated_rain_rate_mmh"] > 40.0
    assert res["hail_threat_detected"] is True
    assert res["probability"] > 70.0


def test_wind_engine():
    """Verify EHI and severe gust anomaly detection."""
    engine = ExtremeWindEngine()
    res = engine.evaluate(wind_speed_kmh=20.0, gust_speed_kmh=72.0, vertical_shear_0_6km_ms=25.0, cape_jkg=2400.0, sreh_0_3km_m2s2=180.0)
    assert res["energy_helicity_index_ehi"] > 1.0
    assert "PUTING_BELIUNG" in res["phenomenon_classification"]


def test_earthquake_engine():
    """Verify Atkinson-Boore GMPE and InaTEWS tsunami criteria."""
    engine = EarthquakeAssessmentEngine()
    # Shallow offshore M 7.9
    res_tsunami = engine.assess_event(magnitude=7.9, depth_km=18.0, is_underwater=True)
    assert res_tsunami["tsunami_evaluation"]["tsunami_threat"] is True
    assert "AWAS" in res_tsunami["tsunami_evaluation"]["warning_status"]

    # Deep inland M 6.1
    res_deep = engine.assess_event(magnitude=6.1, depth_km=120.0, is_underwater=False)
    assert res_deep["tsunami_evaluation"]["tsunami_threat"] is False
    assert res_deep["peak_ground_acceleration_pct_g"] > 0.0


def test_wildfire_engine():
    """Verify complete Canadian FWI and peatland vulnerability."""
    engine = WildfireRiskEngine()
    res = engine.evaluate_hotspots(hotspot_count=18, max_frp_mw=85.0, temp_c=36.0, rh_percent=38.0, wind_kmh=22.0, rain_24h_mm=0.0, is_peatland=True)
    assert res["fwi_subindices"]["dc"] > 200.0
    assert res["peatland_combustion_threat"] is True
    assert res["probability"] > 75.0


def test_cyclone_engine():
    """Verify Holland vortex wind and Bretschneider wave heights."""
    engine = TropicalCycloneEngine()
    res = engine.evaluate(central_pressure_hpa=985.0, observed_max_knots=55.0, sea_surface_temp_c=30.0)
    assert res["significant_wave_height_meters"] >= 3.0
    assert res["marine_gale_warning"] is True
    assert "KATEGORI" in res["cyclone_category"]


if __name__ == "__main__":
    print("Running AI Engine Scientific Verification...")
    test_unified_risk_scoring_boundary()
    test_flood_engine()
    test_landslide_engine()
    test_volcano_engine()
    test_thunderstorm_engine()
    test_wind_engine()
    test_earthquake_engine()
    test_wildfire_engine()
    test_cyclone_engine()
    print("ALL 9 AI ENGINE TESTS PASSED WITH 100% SUCCESS!")
