"""NATURALGUARD AI — Official Portals & External References API Router."""
from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter(prefix="/references", tags=["Official References & Portals"])

OFFICIAL_PORTALS = [
    {
        "id": "bmkg-inatews",
        "name": "BMKG InaTEWS (Indonesia Tsunami Early Warning System)",
        "agency": "Badan Meteorologi, Klimatologi, dan Geofisika (BMKG)",
        "category": "Seismology & Tsunami",
        "url": "https://inatews.bmkg.go.id/",
        "api_url": "https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json",
        "description": "Pusat informasi gempabumi real-time dan diseminasi peringatan dini tsunami nasional.",
        "badge": "Prioritas Utama Indonesia",
        "features": ["Peta Guncangan MMI", "Katalog Gempa M > 5.0", "Status Potensi Tsunami Pesisir", "Pemberitahuan WRS-CAP"],
        "attribution": "BMKG Republik Indonesia"
    },
    {
        "id": "bnpb-inarisk",
        "name": "BNPB InaRISK WebGIS Portal",
        "agency": "Badan Nasional Penanggulangan Bencana (BNPB)",
        "category": "Disaster Risk & Vulnerability",
        "url": "https://inarisk.bnpb.go.id/webgis/",
        "api_url": "https://inarisk.bnpb.go.id/v4/about",
        "description": "Geoportal spasial risiko bencana resmi Indonesia mencakup layer banjir, longsor, likuifaksi, dan kerentanan warga.",
        "badge": "Prioritas Utama Indonesia",
        "features": ["Layer Rawan Banjir Bandang", "Peta Kerentanan Longsor", "Indeks Keterpaparan Penduduk", "Peta Bahaya Multi-Bencana"],
        "attribution": "BNPB InaRISK Geoportal"
    },
    {
        "id": "pvmbg-magma",
        "name": "PVMBG MAGMA Indonesia",
        "agency": "Pusat Vulkanologi dan Mitigasi Bencana Geologi (Badan Geologi ESDM)",
        "category": "Volcanology & Geotechnical",
        "url": "https://magma.esdm.go.id/",
        "api_url": "https://magma.esdm.go.id/v1/home",
        "description": "Multiplatform Application for Geohazard Mitigation and Assessment, memonitor status 127 gunung api aktif dan gerakan tanah.",
        "badge": "Otoritas Vulkanologi Resmi",
        "features": ["Status Gunung Api Level I-IV", "VONA (Volcano Observatory Notice for Aviation)", "Laporan Aktivitas Harian", "Peta Kawasan Rawan Bencana (KRB)"],
        "attribution": "PVMBG Kementerian ESDM"
    },
    {
        "id": "nasa-firms",
        "name": "NASA FIRMS (Fire Information for Resource Management System)",
        "agency": "National Aeronautics and Space Administration (NASA EOSDIS)",
        "category": "Thermal Anomaly & Wildfire",
        "url": "https://firms.modaps.eosdis.nasa.gov/map/",
        "api_url": "https://firms.modaps.eosdis.nasa.gov/api/data_availability/",
        "description": "Peta interaktif global satelit VIIRS (375m) dan MODIS (1km) mendeteksi titik panas aktif dan kebakaran hutan tropis.",
        "badge": "Global Remote Sensing",
        "features": ["Deteksi Hotspot Real-Time NRT", "Fire Radiative Power (FRP)", "Filter Kepercayaan Sensor (Confidence)", "Pemantauan Gambut Riau/Kalteng"],
        "attribution": "NASA Earth Science Data Systems"
    },
    {
        "id": "usgs-earthquakes",
        "name": "USGS Latest Earthquakes Interactive Map",
        "agency": "United States Geological Survey (USGS)",
        "category": "Seismology",
        "url": "https://earthquake.usgs.gov/earthquakes/map/",
        "api_url": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_month.geojson",
        "description": "Pusat pengamatan kegempaan global dan mekanisme patahan lempeng tektonik.",
        "badge": "Global Seismic Network",
        "features": ["Katalog Gempa Global Real-time", "ShakeMap Pager", "Mekanisme Solusi Fokal Patahan", "Atenuasi Guncangan"],
        "attribution": "USGS Earthquake Hazards Program"
    },
    {
        "id": "gdacs-global",
        "name": "GDACS (Global Disaster Alert and Coordination System)",
        "agency": "United Nations (UN) & European Commission (EC)",
        "category": "Global Multi-Hazard",
        "url": "https://www.gdacs.org/",
        "api_url": "https://www.gdacs.org/xml/rss.xml",
        "description": "Sistem koordinasi dan peringatan bencana darurat global PBB untuk gempa, tsunami, siklon, banjir, dan erupsi.",
        "badge": "United Nations EWS",
        "features": ["Peringatan Level Merah/Oranye/Hijau", "Estimasi Populasi Terdampak Global", "Analisis Satelit Darurat UNOSAT", "Laporan Situasi Kemanusiaan"],
        "attribution": "UN OCHA & European Commission JRC"
    },
    {
        "id": "bmkg-cuaca",
        "name": "BMKG Peta Cuaca & Radar Maritim",
        "agency": "Badan Meteorologi, Klimatologi, dan Geofisika (BMKG)",
        "category": "Meteorology & Marine",
        "url": "https://cuaca.bmkg.go.id/",
        "api_url": "https://data.bmkg.go.id/DataMKG/MEWS/dini/peringatan-dini-cuaca.json",
        "description": "Citra satelit cuaca Himawari-9, mosaik radar Doppler nasional, dan peringatan dini cuaca ekstrem kecamatan.",
        "badge": "Prakiraan Cuaca Resmi",
        "features": ["Mosaik Radar Cuaca Doppler", "Satelit Inframerah Awan Himawari", "Prospek Cuaca Mingguan", "TCWC Peringatan Siklon Tropis"],
        "attribution": "BMKG Meteorologi Publik"
    },
    {
        "id": "pupr-sitaba",
        "name": "Kementerian PU SITABA (Sistem Tanggap Bencana)",
        "agency": "Kementerian Pekerjaan Umum Republik Indonesia",
        "category": "Hydrology & Infrastructure",
        "url": "https://sitaba.pu.go.id/",
        "api_url": "https://sitaba.pu.go.id/portal",
        "description": "Pemantauan infrastruktur ke-PU-an yang terdampak bencana, tinggi muka air pos duga sungai, dan sumber daya tanggap darurat.",
        "badge": "Infrastruktur & Sumber Daya Air",
        "features": ["Pos Duga TMA Sungai", "Sebaran Pompa Pengendali Banjir", "Kerusakan Jembatan & Tanggul", "Logistik Ekskavator PU"],
        "attribution": "Kementerian Pekerjaan Umum"
    }
]


@router.get("", response_model=List[Dict[str, Any]])
async def list_official_references():
    """Retrieve full catalog of authoritative disaster portals, WebGIS maps, and API endpoints."""
    return OFFICIAL_PORTALS
