"""NATURALGUARD AI — Initial Seed Data & Multi-Hazard Database."""
from datetime import datetime, timezone, timedelta
from app.database.models import (
    HazardType, RiskCategory, AlertLevel, DataQuality,
    LocationInfo, RiskScoreBreakdown, DisasterEvent, DisasterAlert,
    ForecastHorizon, ForecastItem, PredictionVsActual, DataSourceStatus
)

NOW = datetime.now(timezone.utc)
ISO_NOW = NOW.isoformat()
ISO_MINUS_10M = (NOW - timedelta(minutes=10)).isoformat()
ISO_PLUS_3H = (NOW + timedelta(hours=3)).isoformat()
ISO_PLUS_6H = (NOW + timedelta(hours=6)).isoformat()
ISO_PLUS_24H = (NOW + timedelta(hours=24)).isoformat()
ISO_PLUS_48H = (NOW + timedelta(hours=48)).isoformat()


def get_risk_breakdown(p: float, s: float, e: float, c: float) -> RiskScoreBreakdown:
    total = round(0.40 * p + 0.25 * s + 0.20 * e + 0.15 * c, 1)
    if total < 20:
        cat = RiskCategory.LOW
    elif total < 40:
        cat = RiskCategory.MODERATE
    elif total < 60:
        cat = RiskCategory.HIGH
    elif total < 80:
        cat = RiskCategory.VERY_HIGH
    else:
        cat = RiskCategory.EXTREME
    return RiskScoreBreakdown(
        probability=p, severity=s, exposure=e, confidence=c,
        total_score=total, category=cat
    )


EVENTS_SEED = [
    # 1. FLOOD
    DisasterEvent(
        id="EVT-FLD-001",
        hazard_type=HazardType.FLOOD,
        title="Banjir Luapan Kali Bekasi & Kali Cikeas",
        description="Peningkatan debit air hulu Cileungsi-Cikeas menyebabkan genangan 40-110 cm di pemukiman bantaran sungai.",
        location=LocationInfo(
            province="Jawa Barat", regency="Kota Bekasi", district="Jatiasih",
            latitude=-6.2383, longitude=106.9756
        ),
        severity=RiskCategory.VERY_HIGH,
        risk_score=get_risk_breakdown(p=85, s=75, e=82, c=90),
        source="PUPR BBWSCC / BMKG Radar",
        is_official_alert=True,
        observed_at=ISO_MINUS_10M,
        valid_until=ISO_PLUS_6H,
        data_quality=DataQuality.VERIFIED,
        parameters={
            "water_level_m": 4.85,
            "danger_threshold_m": 4.20,
            "rainfall_last_3h_mm": 68.4,
            "river_name": "Kali Bekasi"
        }
    ),
    DisasterEvent(
        id="EVT-FLD-002",
        hazard_type=HazardType.FLOOD,
        title="Banjir Rob & Genangan Pesisir Semarang Utara",
        description="Pasang air laut maksimum bertepatan dengan drainase terhambat di kawasan Kaligawe dan Genuk.",
        location=LocationInfo(
            province="Jawa Tengah", regency="Kota Semarang", district="Semarang Utara",
            latitude=-6.9666, longitude=110.4381
        ),
        severity=RiskCategory.HIGH,
        risk_score=get_risk_breakdown(p=78, s=62, e=70, c=88),
        source="BMKG Maritim Tanjung Emas",
        is_official_alert=True,
        observed_at=ISO_MINUS_10M,
        valid_until=ISO_PLUS_6H,
        data_quality=DataQuality.VERIFIED,
        parameters={"tidal_height_cm": 115, "submerged_roads": ["Jalan Kaligawe Raya"]}
    ),

    # 2. LANDSLIDE
    DisasterEvent(
        id="EVT-LND-001",
        hazard_type=HazardType.LANDSLIDE,
        title="Potensi Gerakan Tanah & Longsor Arjasari Bandung",
        description="Hujan kumulatif 7 hari mencapai 240 mm pada lereng dengan kemiringan 34 derajat memicu retakan tanah.",
        location=LocationInfo(
            province="Jawa Barat", regency="Kabupaten Bandung", district="Arjasari",
            latitude=-7.0722, longitude=107.6321
        ),
        severity=RiskCategory.VERY_HIGH,
        risk_score=get_risk_breakdown(p=82, s=80, e=65, c=85),
        source="PVMBG / InaRISK",
        is_official_alert=True,
        observed_at=ISO_MINUS_10M,
        valid_until=ISO_PLUS_24H,
        data_quality=DataQuality.VERIFIED,
        parameters={"slope_angle": 34, "cumulative_rain_7d_mm": 242.0, "soil_type": "Andosol lapuk"}
    ),

    # 3. VOLCANO
    DisasterEvent(
        id="EVT-VOL-001",
        hazard_type=HazardType.VOLCANO,
        title="Gunung Semeru — Status Siaga (Level III)",
        description="Teramati letusan dengan tinggi kolom abu 700 m dari puncak. Arah guguran lava ke Besuk Kobokan radius 5 km.",
        location=LocationInfo(
            province="Jawa Timur", regency="Kabupaten Lumajang", district="Pronojiwo",
            latitude=-8.108, longitude=112.922
        ),
        severity=RiskCategory.EXTREME,
        risk_score=get_risk_breakdown(p=92, s=88, e=74, c=95),
        source="PVMBG MAGMA Indonesia",
        is_official_alert=True,
        observed_at=ISO_MINUS_10M,
        valid_until=ISO_PLUS_24H,
        data_quality=DataQuality.VERIFIED,
        parameters={
            "pvmbg_level": "Level III (Siaga)",
            "danger_radius_km": 5.0,
            "ash_column_m": 700,
            "eruption_count_24h": 46
        }
    ),
    DisasterEvent(
        id="EVT-VOL-002",
        hazard_type=HazardType.VOLCANO,
        title="Gunung Merapi — Status Siaga (Level III)",
        description="Guguran lava dan awan panas guguran terpantau mengarah ke sektor selatan-barat daya (Kali Bebeng & Kali Krasak).",
        location=LocationInfo(
            province="D.I. Yogyakarta", regency="Sleman", district="Pakem",
            latitude=-7.540, longitude=110.446
        ),
        severity=RiskCategory.HIGH,
        risk_score=get_risk_breakdown(p=75, s=70, e=78, c=94),
        source="BPPTKG / PVMBG",
        is_official_alert=True,
        observed_at=ISO_MINUS_10M,
        valid_until=ISO_PLUS_24H,
        data_quality=DataQuality.VERIFIED,
        parameters={"pvmbg_level": "Level III (Siaga)", "active_dome": "Kubah Barat Daya"}
    ),

    # 4. THUNDERSTORM
    DisasterEvent(
        id="EVT-THU-001",
        hazard_type=HazardType.THUNDERSTORM,
        title="Severe Thunderstorm & Lightning Cluster Surabaya Raya",
        description="Sel konvektif kuat terpantau radar BMKG dengan reflektivitas 50-55 dBZ, potensi hujan lebat, kilat, dan petir.",
        location=LocationInfo(
            province="Jawa Timur", regency="Kota Surabaya", district="Wonokromo",
            latitude=-7.2575, longitude=112.7521
        ),
        severity=RiskCategory.HIGH,
        risk_score=get_risk_breakdown(p=88, s=60, e=85, c=88),
        source="BMKG Stasiun Meteorologi Juanda",
        is_official_alert=True,
        observed_at=ISO_MINUS_10M,
        valid_until=ISO_PLUS_3H,
        data_quality=DataQuality.VERIFIED,
        parameters={"radar_reflectivity_dbz": 54, "cape_index": 2450, "lightning_strikes_1h": 320}
    ),

    # 5. TORNADO / PUTING BELIUNG
    DisasterEvent(
        id="EVT-WND-001",
        hazard_type=HazardType.WIND,
        title="Peringatan Dini Angin Kencang & Puting Beliung Rancaekek",
        description="Model mendeteksi anomali shear angin horizontal dan squall line dengan potensi hembusan angin kencang mendadak > 55 km/jam.",
        location=LocationInfo(
            province="Jawa Barat", regency="Kabupaten Bandung", district="Rancaekek",
            latitude=-6.9686, longitude=107.7667
        ),
        severity=RiskCategory.HIGH,
        risk_score=get_risk_breakdown(p=70, s=68, e=72, c=75),
        source="NaturalGuard AI Convective Wind Engine",
        is_official_alert=False,
        observed_at=ISO_MINUS_10M,
        valid_until=ISO_PLUS_3H,
        data_quality=DataQuality.ESTIMATED,
        parameters={"estimated_gust_kmh": 62, "shear_value": "moderate_high"}
    ),

    # 6. EARTHQUAKE
    DisasterEvent(
        id="EVT-EQK-001",
        hazard_type=HazardType.EARTHQUAKE,
        title="Gempabumi M 6.1 Laut Banda Maluku",
        description="Guncangan skala III-IV MMI dirasakan di Saumlaki. Tidak berpotensi tsunami menurut pemodelan BMKG.",
        location=LocationInfo(
            province="Maluku", regency="Kepulauan Tanimbar", district="Saumlaki",
            latitude=-7.12, longitude=129.85
        ),
        severity=RiskCategory.MODERATE,
        risk_score=get_risk_breakdown(p=99, s=55, e=25, c=98),
        source="BMKG TEWS / USGS Earthquake Network",
        is_official_alert=True,
        observed_at=ISO_MINUS_10M,
        valid_until=ISO_PLUS_24H,
        data_quality=DataQuality.VERIFIED,
        parameters={
            "magnitude": 6.1,
            "depth_km": 118,
            "tsunami_potential": False,
            "felt_mmi": "III-IV (Saumlaki)"
        }
    ),
    DisasterEvent(
        id="EVT-EQK-002",
        hazard_type=HazardType.EARTHQUAKE,
        title="Gempabumi M 5.2 Barat Daya Kepulauan Mentawai",
        description="Pusat gempa dangkal 28 km, getaran dirasakan di Tuapejat MMI II-III.",
        location=LocationInfo(
            province="Sumatera Barat", regency="Kepulauan Mentawai", district="Sipora",
            latitude=-2.35, longitude=99.45
        ),
        severity=RiskCategory.LOW,
        risk_score=get_risk_breakdown(p=99, s=40, e=20, c=98),
        source="BMKG TEWS",
        is_official_alert=True,
        observed_at=ISO_MINUS_10M,
        valid_until=ISO_PLUS_24H,
        data_quality=DataQuality.VERIFIED,
        parameters={"magnitude": 5.2, "depth_km": 28, "tsunami_potential": False}
    ),

    # 7. WILDFIRE
    DisasterEvent(
        id="EVT-FIR-001",
        hazard_type=HazardType.WILDFIRE,
        title="Kluster Titik Panas Karhutla Dumai & Rokan Hilir",
        description="Satelit NASA FIRMS VIIRS mendeteksi 14 titik panas dengan tingkat kepercayaan > 80% pada lahan gambut kering.",
        location=LocationInfo(
            province="Riau", regency="Kota Dumai", district="Sungai Sembilan",
            latitude=1.688, longitude=101.442
        ),
        severity=RiskCategory.HIGH,
        risk_score=get_risk_breakdown(p=86, s=65, e=60, c=84),
        source="NASA FIRMS / BPBD Riau",
        is_official_alert=True,
        observed_at=ISO_MINUS_10M,
        valid_until=ISO_PLUS_24H,
        data_quality=DataQuality.VERIFIED,
        parameters={"hotspots_count": 14, "fwi_index": "High", "drought_days": 18}
    ),

    # 8. CYCLONE
    DisasterEvent(
        id="EVT-CYC-001",
        hazard_type=HazardType.CYCLONE,
        title="Bibit Siklon Tropis 99S Samudera Hindia Selatan Jawa",
        description="Pusat tekanan rendah 1002 hPa memicu potensi gelombang laut 2.5 - 4.0 m dan angin kencang di pesisir selatan Jawa-Bali.",
        location=LocationInfo(
            province="D.I. Yogyakarta", regency="Gunungkidul", district="Tanjungsari",
            latitude=-9.80, longitude=110.20
        ),
        severity=RiskCategory.HIGH,
        risk_score=get_risk_breakdown(p=75, s=70, e=58, c=80),
        source="BMKG Tropical Cyclone Warning Centre (TCWC)",
        is_official_alert=True,
        observed_at=ISO_MINUS_10M,
        valid_until=ISO_PLUS_48H,
        data_quality=DataQuality.VERIFIED,
        parameters={
            "central_pressure_hpa": 1002,
            "max_wind_knots": 25,
            "wave_height_meters": "2.5 - 4.0 m"
        }
    )
]


ALERTS_SEED = [
    DisasterAlert(
        id="ALT-OFFICIAL-001",
        event_id="EVT-FLD-001",
        hazard_type=HazardType.FLOOD,
        alert_level=AlertLevel.WARNING,
        headline="Peringatan Dini Banjir Luapan Kali Bekasi (Status Siaga II)",
        instruction="Warga di bantaran Kali Bekasi (Jatiasih, Kemang Pratama, Rawalumbu) dihimbau mengamankan barang berharga dan bersiap evakuasi mandiri.",
        affected_areas=["Kecamatan Jatiasih", "Kecamatan Rawalumbu", "Kecamatan Bekasi Timur"],
        is_official=True,
        risk_score=78.5,
        confidence_score=90.0,
        source="BPBD Kota Bekasi & BMKG",
        status="active",
        data_quality=DataQuality.VERIFIED,
        issued_at=ISO_MINUS_10M,
        expires_at=ISO_PLUS_6H
    ),
    DisasterAlert(
        id="ALT-OFFICIAL-002",
        event_id="EVT-VOL-001",
        hazard_type=HazardType.VOLCANO,
        alert_level=AlertLevel.WARNING,
        headline="Status Gunung Semeru Siaga Level III — Hindari Sektor Besuk Kobokan",
        instruction="Masyarakat tidak boleh melakukan aktivitas apapun di sektor tenggara sepanjang Besuk Kobokan sejauh 13 km dari puncak.",
        affected_areas=["Kecamatan Pronojiwo", "Kecamatan Candipuro"],
        is_official=True,
        risk_score=87.2,
        confidence_score=95.0,
        source="PVMBG Kementerian ESDM",
        status="active",
        data_quality=DataQuality.VERIFIED,
        issued_at=ISO_MINUS_10M,
        expires_at=ISO_PLUS_24H
    ),
    DisasterAlert(
        id="ALT-AI-001",
        event_id="EVT-WND-001",
        hazard_type=HazardType.WIND,
        alert_level=AlertLevel.WATCH,
        headline="[AI Risk Estimate] Potensi Angin Kencang / Puting Beliung Rancaekek",
        instruction="Sistem mendeteksi sel badai konvektif dengan pusaran lokal. Harap waspada pohon tumbang dan atap rumah lapuk. Pantau info resmi BMKG.",
        affected_areas=["Kecamatan Rancaekek", "Kecamatan Jatinangor"],
        is_official=False,
        risk_score=71.2,
        confidence_score=75.0,
        source="NATURALGUARD AI Convective Engine",
        status="active",
        data_quality=DataQuality.ESTIMATED,
        issued_at=ISO_MINUS_10M,
        expires_at=ISO_PLUS_3H
    ),
    DisasterAlert(
        id="ALT-OFFICIAL-003",
        event_id="EVT-LND-001",
        hazard_type=HazardType.LANDSLIDE,
        alert_level=AlertLevel.WARNING,
        headline="Peringatan Dini Gerakan Tanah / Longsor Arjasari Bandung",
        instruction="Warga lereng bukit dihimbau mengungsi saat hujan lebat berturut-turut lebih dari 2 jam.",
        affected_areas=["Desa Wargaluyu", "Desa Pinggirsari", "Kecamatan Arjasari"],
        is_official=True,
        risk_score=76.8,
        confidence_score=85.0,
        source="PVMBG & BPBD Jabar",
        status="active",
        data_quality=DataQuality.VERIFIED,
        issued_at=ISO_MINUS_10M,
        expires_at=ISO_PLUS_24H
    ),
    DisasterAlert(
        id="ALT-OFFICIAL-004",
        event_id="EVT-THU-001",
        hazard_type=HazardType.THUNDERSTORM,
        alert_level=AlertLevel.WATCH,
        headline="Peringatan Dini Cuaca Ekstrem Hujan Lebat & Petir Surabaya",
        instruction="Kurangi aktivitas di luar ruangan. Jauhi tiang listrik, baliho, dan pohon besar.",
        affected_areas=["Surabaya Timur", "Surabaya Selatan", "Sidoarjo Utara"],
        is_official=True,
        risk_score=68.4,
        confidence_score=88.0,
        source="BMKG Juanda",
        status="active",
        data_quality=DataQuality.VERIFIED,
        issued_at=ISO_MINUS_10M,
        expires_at=ISO_PLUS_3H
    )
]


FORECAST_SEED = [
    ForecastItem(
        hazard_type=HazardType.FLOOD,
        region="Jabodetabek (Ciliwung & Kali Bekasi)",
        latitude=-6.2088,
        longitude=106.8456,
        last_updated=ISO_NOW,
        horizons=[
            ForecastHorizon(
                horizon_label="0–6 jam (Nowcasting)",
                horizon_hours=6,
                predicted_probability=85.0,
                predicted_severity="Very High",
                confidence=91.0,
                summary="Debit TMA Pos Pantau Pasar Baru & Bendung Katulampa meningkat cepat akibat hujan lebat hulu.",
                model_version="FloodXGB-v2.4"
            ),
            ForecastHorizon(
                horizon_label="6–24 jam (Daily Outlook)",
                horizon_hours=24,
                predicted_probability=70.0,
                predicted_severity="High",
                confidence=85.0,
                summary="Potensi genangan air surut perlahan apabila tidak terjadi hujan susulan di kawasan Bogor.",
                model_version="FloodXGB-v2.4"
            ),
            ForecastHorizon(
                horizon_label="1–3 hari (Short-Term)",
                horizon_hours=72,
                predicted_probability=55.0,
                predicted_severity="Moderate",
                confidence=78.0,
                summary="Prakiraan curah hujan moderat harian 20-40 mm/hari di DAS Jabodetabek.",
                model_version="HydroLSTM-v3.1"
            ),
            ForecastHorizon(
                horizon_label="4–7 hari (Extended)",
                horizon_hours=168,
                predicted_probability=42.0,
                predicted_severity="Moderate",
                confidence=70.0,
                summary="Monsun Asia aktif berpotensi menambah suplai uap air.",
                model_version="HydroLSTM-v3.1"
            ),
            ForecastHorizon(
                horizon_label="8–14 hari (Probabilistic)",
                horizon_hours=336,
                predicted_probability=38.0,
                predicted_severity="Low",
                confidence=58.0,
                summary="Estimasi probabilistik model menunjukkan kecenderungan penurunan curah hujan dasarian.",
                model_version="EnsembleHydro-v1.2"
            ),
            ForecastHorizon(
                horizon_label="15–30 hari (Seasonal Trend)",
                horizon_hours=720,
                predicted_probability=30.0,
                predicted_severity="Low",
                confidence=45.0,
                summary="Proyeksi tren musiman bukan kepastian kejadian spesifik; kondisi netral ENSO.",
                model_version="ClimateOutlook-v1.0"
            )
        ]
    ),
    ForecastItem(
        hazard_type=HazardType.LANDSLIDE,
        region="Jawa Barat Bagian Selatan (Bandung-Cianjur)",
        latitude=-7.0500,
        longitude=107.5000,
        last_updated=ISO_NOW,
        horizons=[
            ForecastHorizon(
                horizon_label="0–6 jam (Nowcasting)",
                horizon_hours=6,
                predicted_probability=80.0,
                predicted_severity="Very High",
                confidence=84.0,
                summary="Kejenuhan air tanah mencapai 92%; potensi longsor tinggi saat hujan mencapai > 30 mm/jam.",
                model_version="SlopeRF-v1.8"
            ),
            ForecastHorizon(
                horizon_label="6–24 jam (Daily Outlook)",
                horizon_hours=24,
                predicted_probability=75.0,
                predicted_severity="High",
                confidence=81.0,
                summary="Pergerakan tanah lambat terdeteksi pada 3 titik jalan provinsi.",
                model_version="SlopeRF-v1.8"
            ),
            ForecastHorizon(
                horizon_label="1–3 hari (Short-Term)",
                horizon_hours=72,
                predicted_probability=62.0,
                predicted_severity="Moderate",
                confidence=72.0,
                summary="Prakiraan hujan berkurang, stabilitas lereng perlahan pulih.",
                model_version="SlopeRF-v1.8"
            ),
            ForecastHorizon(
                horizon_label="4–7 hari (Extended)",
                horizon_hours=168,
                predicted_probability=48.0,
                predicted_severity="Moderate",
                confidence=65.0,
                summary="Waspada rembesan air pada lereng curam bertutupan vegetasi minim.",
                model_version="SlopeRF-v1.8"
            ),
            ForecastHorizon(
                horizon_label="8–14 hari (Probabilistic)",
                horizon_hours=336,
                predicted_probability=35.0,
                predicted_severity="Low",
                confidence=52.0,
                summary="Model probabilistik menunjukkan risiko longsor di bawah batas rata-rata historis.",
                model_version="SlopeProb-v1.0"
            ),
            ForecastHorizon(
                horizon_label="15–30 hari (Seasonal Trend)",
                horizon_hours=720,
                predicted_probability=25.0,
                predicted_severity="Low",
                confidence=40.0,
                summary="Outlook musiman: transisi musim berisiko mengurangi kejadian longsor.",
                model_version="ClimateOutlook-v1.0"
            )
        ]
    )
]


DATA_SOURCES_SEED = [
    DataSourceStatus(
        name="BMKG Open Data & TEWS",
        provider="Badan Meteorologi, Klimatologi, dan Geofisika",
        hazard_coverage=["earthquake", "tsunami", "weather", "cyclone", "thunderstorm"],
        status="online",
        latency_ms=184,
        last_sync=ISO_NOW,
        records_count=1420,
        data_quality=DataQuality.VERIFIED,
        circuit_breaker_state="CLOSED"
    ),
    DataSourceStatus(
        name="BNPB InaRISK & Geoportal",
        provider="Badan Nasional Penanggulangan Bencana",
        hazard_coverage=["flood", "landslide", "volcano", "earthquake", "wildfire"],
        status="online",
        latency_ms=240,
        last_sync=ISO_NOW,
        records_count=892,
        data_quality=DataQuality.VERIFIED,
        circuit_breaker_state="CLOSED"
    ),
    DataSourceStatus(
        name="PVMBG MAGMA Indonesia",
        provider="Pusat Vulkanologi dan Mitigasi Bencana Geologi",
        hazard_coverage=["volcano", "landslide"],
        status="online",
        latency_ms=310,
        last_sync=ISO_NOW,
        records_count=127,
        data_quality=DataQuality.VERIFIED,
        circuit_breaker_state="CLOSED"
    ),
    DataSourceStatus(
        name="USGS Global Earthquake API",
        provider="United States Geological Survey",
        hazard_coverage=["earthquake"],
        status="online",
        latency_ms=420,
        last_sync=ISO_NOW,
        records_count=2150,
        data_quality=DataQuality.VERIFIED,
        circuit_breaker_state="CLOSED"
    ),
    DataSourceStatus(
        name="NASA FIRMS VIIRS/MODIS",
        provider="NASA Earth Observing System Data and Information System",
        hazard_coverage=["wildfire"],
        status="online",
        latency_ms=530,
        last_sync=ISO_NOW,
        records_count=640,
        data_quality=DataQuality.VERIFIED,
        circuit_breaker_state="CLOSED"
    ),
    DataSourceStatus(
        name="SITABA Tanggap Darurat PU",
        provider="Kementerian Pekerjaan Umum",
        hazard_coverage=["flood", "infrastructure"],
        status="online",
        latency_ms=290,
        last_sync=ISO_NOW,
        records_count=312,
        data_quality=DataQuality.VERIFIED,
        circuit_breaker_state="CLOSED"
    )
]


PREDICTION_VS_ACTUAL_SEED = [
    PredictionVsActual(
        id="EVAL-2026-001",
        hazard_type=HazardType.FLOOD,
        region="Bekasi Barat, Jawa Barat",
        prediction_date="2026-11-02",
        predicted_risk=82.0,
        predicted_category="Very High",
        actual_occurred=True,
        actual_severity="Tinggi (Genangan 80 cm)",
        lead_time_hours=4.5,
        brier_score=0.032,
        notes="Prediksi XGBoost akurat 4.5 jam sebelum luapan Kali Bekasi menggenangi pemukiman."
    ),
    PredictionVsActual(
        id="EVAL-2026-002",
        hazard_type=HazardType.LANDSLIDE,
        region="Cianjur Selatan, Jawa Barat",
        prediction_date="2026-10-28",
        predicted_risk=74.0,
        predicted_category="High",
        actual_occurred=True,
        actual_severity="Sedang (Tebing longsor menutup jalan desa)",
        lead_time_hours=12.0,
        brier_score=0.067,
        notes="Ambang hujan kumulatif 7 hari terlewati; warga sempat mengevakuasi ternak."
    ),
    PredictionVsActual(
        id="EVAL-2026-003",
        hazard_type=HazardType.THUNDERSTORM,
        region="Surabaya Barat, Jawa Timur",
        prediction_date="2026-10-25",
        predicted_risk=65.0,
        predicted_category="High",
        actual_occurred=True,
        actual_severity="Sedang (Hujan es & angin kencang lokal)",
        lead_time_hours=1.8,
        brier_score=0.120,
        notes="Nowcasting radar berhasil memproyeksikan pergerakan sel badai 1.8 jam sebelumnya."
    ),
    PredictionVsActual(
        id="EVAL-2026-004",
        hazard_type=HazardType.WIND,
        region="Sidoarjo, Jawa Timur",
        prediction_date="2026-10-20",
        predicted_risk=58.0,
        predicted_category="High",
        actual_occurred=False,
        actual_severity="Tidak Terjadi (False Alarm)",
        lead_time_hours=2.0,
        brier_score=0.336,
        notes="Shear vertikal mereda akibat perubahan divergensi angin lapisan atas."
    ),
    PredictionVsActual(
        id="EVAL-2026-005",
        hazard_type=HazardType.WILDFIRE,
        region="Pelalawan, Riau",
        prediction_date="2026-10-15",
        predicted_risk=85.0,
        predicted_category="Very High",
        actual_occurred=True,
        actual_severity="Tinggi (Kebakaran 12 hektar gambut)",
        lead_time_hours=24.0,
        brier_score=0.022,
        notes="Indeks FWI dan deteksi suhu permukaan mengonfirmasi kebakaran aktif."
    )
]
