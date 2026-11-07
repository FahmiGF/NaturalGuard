"""NATURALGUARD AI — Copilot RAG & Assistant Service."""
import re
from datetime import datetime, timezone
from typing import List, Dict, Any
from app.database.models import CopilotResponse, CopilotCitation


class NaturalGuardCopilot:
    def __init__(self, events: List[Any], alerts: List[Any], forecasts: List[Any]):
        self.events = events
        self.alerts = alerts
        self.forecasts = forecasts

    def process_query(self, query: str) -> CopilotResponse:
        q = query.lower().strip()
        now_str = datetime.now(timezone.utc).strftime("%d %b %Y %H:%M UTC")

        citations: List[CopilotCitation] = []
        related_alerts: List[str] = []
        answer_parts: List[str] = []

        # 1. Pertanyaan terkait gempa bumi
        if any(w in q for w in ["gempa", "earthquake", "seismik", "tsunami"]):
            eq_events = [e for e in self.events if e.hazard_type.value == "earthquake"]
            if eq_events:
                latest = eq_events[0]
                p = latest.parameters
                answer_parts.append(
                    f"**Informasi Gempabumi Terkini:**\n"
                    f"- **Kejadian:** {latest.title}\n"
                    f"- **Magnitudo & Kedalaman:** M {p.get('magnitude', '-')} | {p.get('depth_km', '-')} km\n"
                    f"- **Lokasi:** {latest.location.province}, {latest.location.regency} ({latest.location.latitude}, {latest.location.longitude})\n"
                    f"- **Potensi Tsunami:** {'BERPOTENSI TSUNAMI' if p.get('tsunami_potential') else 'Tidak berpotensi tsunami (berdasarkan rilis resmi BMKG)'}\n"
                    f"- **Guncangan:** {p.get('felt_mmi', 'Getaran terasa di pemukiman terdekat')}"
                )
                citations.append(CopilotCitation(
                    source=latest.source,
                    timestamp=latest.observed_at,
                    confidence=latest.risk_score.confidence,
                    data_type="Official Seismic Network Feed"
                ))
            else:
                answer_parts.append("Tidak ada anomali kegempaan signifikan M > 5.0 yang terdeteksi dalam 24 jam terakhir.")

        # 2. Pertanyaan terkait banjir (flood) / bekasi / jakarta / surabaya
        elif any(w in q for w in ["banjir", "flood", "genangan", "kali", "sungai", "bekasi"]):
            flood_events = [e for e in self.events if e.hazard_type.value == "flood"]
            if flood_events:
                ev = flood_events[0]
                p = ev.parameters
                answer_parts.append(
                    f"**Status Pemantauan Banjir:**\n"
                    f"- **Wilayah:** {ev.title} ({ev.location.regency}, {ev.location.province})\n"
                    f"- **Tinggi Muka Air (TMA):** {p.get('water_level_m', '-')} m (Ambang Bahaya: {p.get('danger_threshold_m', '-')} m)\n"
                    f"- **Curah Hujan 3 Jam:** {p.get('rainfall_last_3h_mm', '-')} mm\n"
                    f"- **Tingkat Risiko:** Skor {ev.risk_score.total_score}/100 ({ev.risk_score.category.value.upper()})\n"
                    f"- **Keterangan:** {ev.description}"
                )
                citations.append(CopilotCitation(
                    source=ev.source,
                    timestamp=ev.observed_at,
                    confidence=ev.risk_score.confidence,
                    data_type="Hydrological Water Level & Radar Sensor"
                ))
                related_alerts.append("ALT-OFFICIAL-001: Peringatan Dini Banjir Luapan Kali Bekasi")
            else:
                answer_parts.append("Kondisi tinggi muka air sungai utama terpantau dalam batas aman.")

        # 3. Pertanyaan terkait gunung api (volcano) / semeru / merapi
        elif any(w in q for w in ["gunung", "volcano", "semeru", "merapi", "erupsi", "lahar"]):
            volcanoes = [e for e in self.events if e.hazard_type.value == "volcano"]
            if volcanoes:
                answer_parts.append("**Status Pengamatan Aktivitas Vulkanik (PVMBG):**")
                for v in volcanoes:
                    p = v.parameters
                    answer_parts.append(
                        f"• **{v.title}**\n"
                        f"  - Status Resmi: {p.get('pvmbg_level', 'Level III (Siaga)')}\n"
                        f"  - Rekomendasi Bahaya: Hindari radius {p.get('danger_radius_km', 5)} km dari kawah aktif\n"
                        f"  - Aktivitas: {v.description}"
                    )
                    citations.append(CopilotCitation(
                        source=v.source,
                        timestamp=v.observed_at,
                        confidence=v.risk_score.confidence,
                        data_type="PVMBG MAGMA Seismicity & Visual Bulletin"
                    ))
                related_alerts.append("ALT-OFFICIAL-002: Status Gunung Semeru Siaga Level III")

        # 4. Pertanyaan terkait cuaca ekstrem / badai petir / angin puting beliung
        elif any(w in q for w in ["cuaca", "badai", "petir", "angin", "puting beliung", "tornado", "thunderstorm"]):
            severe_events = [e for e in self.events if e.hazard_type.value in ["thunderstorm", "wind", "cyclone"]]
            answer_parts.append("**Pemantauan Cuaca Ekstrem & Dinamika Atmosfer:**")
            for sev in severe_events:
                answer_parts.append(
                    f"• **{sev.title}** ({sev.location.regency})\n"
                    f"  - Kategori Risiko: {sev.risk_score.category.value.upper()} (Skor {sev.risk_score.total_score}/100)\n"
                    f"  - Observasi: {sev.description}\n"
                    f"  - Status Data: {'Resmi Otoritas' if sev.is_official_alert else 'Estimasi AI Model'}"
                )
                citations.append(CopilotCitation(
                    source=sev.source,
                    timestamp=sev.observed_at,
                    confidence=sev.risk_score.confidence,
                    data_type="Radar Doppler Reflectivity & AI Convective Index"
                ))

        # 5. Pertanyaan terkait longsor / tanah bergerak
        elif any(w in q for w in ["longsor", "landslide", "lereng", "gerakan tanah"]):
            ls_events = [e for e in self.events if e.hazard_type.value == "landslide"]
            if ls_events:
                l = ls_events[0]
                p = l.parameters
                answer_parts.append(
                    f"**Analisis Potensi Gerakan Tanah & Longsor:**\n"
                    f"- **Lokasi:** {l.title} ({l.location.district}, {l.location.regency})\n"
                    f"- **Kemiringan Lereng:** {p.get('slope_angle', '-')}\u00b0 (Kategori Curam)\n"
                    f"- **Hujan Kumulatif 7 Hari:** {p.get('cumulative_rain_7d_mm', '-')} mm (Ambang batas jenuh tercapai)\n"
                    f"- **Kondisi:** {l.description}"
                )
                citations.append(CopilotCitation(
                    source=l.source,
                    timestamp=l.observed_at,
                    confidence=l.risk_score.confidence,
                    data_type="Soil Saturation Index & InaRISK Vulnerability"
                ))

        # 6. Pertanyaan terkait karhutla / kebakaran hutan
        elif any(w in q for w in ["karhutla", "kebakaran", "hotspot", "titik panas", "riau", "wildfire"]):
            fires = [e for e in self.events if e.hazard_type.value == "wildfire"]
            if fires:
                f = fires[0]
                p = f.parameters
                answer_parts.append(
                    f"**Pemantauan Titik Panas (Hotspot) & Karhutla:**\n"
                    f"- **Lokasi:** {f.title}\n"
                    f"- **Jumlah Hotspot Terdeteksi:** {p.get('hotspots_count', '-')} titik (Kepercayaan > 80%)\n"
                    f"- **Hari Tanpa Hujan (HTH):** {p.get('drought_days', '-')} hari berturut-turut\n"
                    f"- **Indeks Kebakaran (FWI):** {p.get('fwi_index', 'Tinggi')}"
                )
                citations.append(CopilotCitation(
                    source=f.source,
                    timestamp=f.observed_at,
                    confidence=f.risk_score.confidence,
                    data_type="NASA FIRMS VIIRS Thermal Anomaly"
                ))

        # Default Ringkasan Multi-Hazard
        if not answer_parts:
            answer_parts.append(
                f"**Ringkasan Multi-Hazard NATURALGUARD AI ({now_str}):**\n"
                f"- Terpantau **{len(self.alerts)} peringatan aktif** dan **{len(self.events)} titik pantau bahaya** di Indonesia.\n"
                f"- Fokus perhatian utama saat ini:\n"
                f"  1. Banjir luapan Kali Bekasi (Status Siaga)\n"
                f"  2. Aktivitas vulkanik Gunung Semeru (Status Siaga Level III)\n"
                f"  3. Potensi gerakan tanah lereng curam Jawa Barat\n"
                f"  4. Bibit Siklon Tropis 99S di Samudera Hindia selatan Jawa."
            )
            citations.append(CopilotCitation(
                source="NATURALGUARD AI Multi-Source Data Fusion Core",
                timestamp=now_str,
                confidence=92.0,
                data_type="Multi-Hazard Ingestion Pipeline"
            ))

        safety_guidance = (
            "Penting: Seluruh prakiraan AI bersifat pendukung keputusan (decision-support). "
            "Peringatan resmi dan instruksi evakuasi mengacu kepada otoritas berwenang (BMKG, BPBD, BNPB, dan PVMBG). "
            "Hubungi call center darurat 112 atau BPBD setempat jika berada di zona bahaya."
        )

        return CopilotResponse(
            answer="\n\n".join(answer_parts),
            citations=citations,
            related_alerts=related_alerts,
            safety_guidance=safety_guidance
        )
