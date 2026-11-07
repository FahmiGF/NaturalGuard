# 🛡️ NATURALGUARD AI
**AI Multi-Hazard Early Warning & Natural Disaster Monitoring Platform**

Platform pemantauan, analisis, prediksi, dan peringatan dini berbagai bencana alam di Indonesia berbasis **AI + Geospatial Intelligence (GIS) + Real-Time Multi-Source Data Fusion**.

---

## 🌟 Prinsip Inti Sistem
1. **Official Data First, AI-Assisted Second**: Peringatan resmi otoritas berwenang (BMKG, BNPB, PVMBG, PUPR) memiliki prioritas mutlak dan tidak boleh ditimpa oleh estimasi AI.
2. **Tanpa Klaim Kepastian Palsu**: Gempa bumi dan letusan gunung api tidak dapat diprediksi secara pasti waktu dan tempatnya. Sistem hanya memonitor kejadian, anomali, estimasi probabilitas, dan guncangan dampak.
3. **Multi-Source Data Provenance**: Setiap data memiliki penanda sumber, stempel waktu `observed_at`, `valid_until`, serta status mutu data (`verified`, `estimated`, `stale`).

---

## 🌪️ 8 Hazard Engines yang Didukung

| # | Hazard Engine | Data Input Kunci | Algoritma / Pendekatan | Horizon |
|---|---|---|---|---|
| **1** | **Banjir (Flood)** | TMA sungai (PUPR), radar presipitasi BMKG, elevasi DEM, kurva limpasan DAS. | XGBoost Classifier + LSTM Hydrology Runoff | 0–24 Jam |
| **2** | **Tanah Longsor (Landslide)** | Hujan kumulatif 1/3/7/14 hari, sudut kemiringan lereng (>25°), kelembapan tanah, tutupan lahan. | Rainfall-Slope Empirical Thresholds + Random Forest | 0–72 Jam |
| **3** | **Gunung Api (Volcano)** | Status resmi PVMBG (Level I-IV), seismik vulkanik (VA/VB), tremor, anomali termal satelit VIIRS. | Isolation Forest Anomaly Detection + PVMBG State Rules | Real-Time |
| **4** | **Badai Petir (Thunderstorm)** | Reflektivitas radar (dBZ), indeks labilitas CAPE, deteksi sambaran kilat/petir, suhu puncak awan. | Optical Flow Convective Nowcasting + ConvLSTM | 0–6 Jam |
| **5** | **Puting Beliung (Wind)** | Anomali kecepatan hembusan (*wind gust*), vertical wind shear, deteksi squall line Doppler. | Statistical Anomaly Detection + Convective Wind Index | 0–3 Jam |
| **6** | **Gempabumi & Tsunami** | Parameter hiposenter BMKG/USGS, kedalaman, magnitudo, evaluasi potensi tsunami, atenuasi MMI. | USGS/BMKG Ingestion + Empirical GMPE MMI Shaking | Real-Time |
| **7** | **Kebakaran Hutan (Wildfire)** | Hotspot NASA FIRMS (VIIRS/MODIS), hari tanpa hujan (HTH), Fire Weather Index (FWI), lahan gambut. | Thermal Anomaly Clustering + FWI Drought Index | 24–48 Jam |
| **8** | **Siklon Tropis & Cuaca Ekstrem** | Tekanan pusat (hPa), kecepatan angin TCWC, suhu muka laut (SST), prakiraan tinggi gelombang laut. | Numerical Weather Prediction Ensemble + Track Model | 24–72 Jam |

---

## ⚖️ Unified Disaster Risk Scoring Framework

Seluruh hasil analisis dinormalisasi ke skala 0–100 dan dihitung dengan formula:

$$R = 0.40 \cdot P + 0.25 \cdot S + 0.20 \cdot E + 0.15 \cdot C$$

- **$P$ (Hazard Probability)**: Probabilitas kemunculan fenomena (bobot 40%).
- **$S$ (Severity Index)**: Estimasi keparahan fisik fenomena (bobot 25%).
- **$E$ (Exposure Score)**: Kepadatan penduduk & infrastruktur kritis terdampak (bobot 20%).
- **$C$ (Confidence Score)**: Kualitas dan konsistensi data pendukung (bobot 15%).

### Skala Kategori Risiko:
- **0 – 19**: 🟢 **Low** (Pemantauan rutin)
- **20 – 39**: 🔵 **Moderate** (Perlu perhatian)
- **40 – 59**: 🟡 **High** (Peningkatan kewaspadaan)
- **60 – 79**: 🟠 **Very High** (Kesiapsiagaan posko darurat)
- **80 – 100**: 🔴 **Extreme** (Peringatan evakuasi berkoordinasi dengan BPBD)

---

## 🚀 Panduan Memulai Cepat (Quick Start)

> [!TIP]
> Panduan instalasi dan operasional lengkap tersedia di **[HOW_TO_START.md](HOW_TO_START.md)**.

### Opsi A: 1-Klik di Windows (Paling Mudah)
Cukup klik dua kali file:
```bash
Buka_NaturalGuard_AI.bat
```
Browser otomatis membuka Command Center di `http://localhost:8000`.

### Opsi B: Terminal Manual (Windows / Mac / Linux)
```bash
cd backend
pip install -r requirements.txt
python run.py
```
Akses di browser: `http://localhost:8000`.

### Opsi C: Docker Containerization
```bash
docker-compose up --build -d
```

---

## 📡 Sumber Data yang Diintegrasikan
- **BMKG**: Open Data Cuaca, Peringatan Dini CAP, Katalog Gempabumi TEWS, TCWC.
- **BNPB**: InaRISK WebGIS & Sebaran Risiko Wilayah.
- **PVMBG**: MAGMA Indonesia status tingkat aktivitas gunung api.
- **Kementerian PUPR**: SITABA Sistem Informasi Tanggap Bencana & TMA Sungai.
- **USGS**: Real-Time Earthquake GeoJSON API.
- **NASA FIRMS**: Hotspot deteksi aktif VIIRS 375m & MODIS 1km.

---

## 🤖 Fitur AI Tambahan
1. **NaturalGuard Copilot**: RAG AI Assistant dalam Bahasa Indonesia yang menjawab pertanyaan risiko bencana dengan sitasi sumber resmi dan stempel waktu.
2. **AI Voice Broadcast (TTS)**: Pembacaan naskah peringatan resmi otomatis dengan Web Speech API Bahasa Indonesia.
3. **Multi-Hazard Correlation Engine**: Mendeteksi interaksi bencana berantai (contoh: erupsi Semeru + hujan lebat $\to$ lahar dingin; hujan kumulatif + lereng curam $\to$ tanah longsor).
4. **Prediction vs Actual Backtesting**: Evaluasi akurasi model historis menggunakan metrik Brier Score, PR-AUC, F1, dan Lead Time.
