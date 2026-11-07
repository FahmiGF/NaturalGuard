# 📖 NATURALGUARD AI — Panduan Pengguna, Tutorial & FAQ

Selamat datang di Pusat Bantuan Resmi **NATURALGUARD AI**. Dokumen ini dirancang untuk memandu masyarakat umum, analis kebencanaan, dan operator posko darurat dalam mengoperasikan platform pemantauan multi-bencana dan sistem peringatan dini nasional.

---

## 📌 DAFTAR ISI
1. [Panduan Membaca Dashboard & Peta GIS](#1-panduan-membaca-dashboard--peta-gis)
2. [Perbedaan Resmi Otoritas vs Estimasi AI](#2-perbedaan-peringatan-resmi-vs-estimasi-ai)
3. [Penjelasan Skor Risiko Terpadu (0–100)](#3-penjelasan-skor-risiko-terpadu-0100)
4. [Panduan Operasional 8 Hazard Centers](#4-panduan-operasional-8-hazard-centers)
5. [Penggunaan RAG Copilot & Voice Broadcast](#5-penggunaan-rag-copilot--voice-broadcast)
6. [Frequently Asked Questions (FAQ)](#6-frequently-asked-questions-faq)
7. [Panduan Integrasi REST API bagi Pengembang](#7-panduan-integrasi-rest-api-bagi-pengembang)

---

## 1. Panduan Membaca Dashboard & Peta GIS

Dashboard NATURALGUARD AI dirancang dengan standar Command Center kebencanaan modern:

- **Peta GIS Interaktif (Leaflet Engine)**:
  - Lingkaran berwarna merepresentasikan lokasi bencana atau titik pantau bahaya.
  - Klik marker mana pun untuk menampilkan popup rincian: nama wilayah (desa/kecamatan/kabupaten), jenis bahaya, nilai parameter fisik (misal: TMA sungai, kedalaman gempa, level kawah), stempel waktu data, dan status verifikasi.
  - Gunakan tombol filter di atas peta (*All, Banjir, Longsor, Gunung Api, Badai, Puting Beliung, Gempa, Karhutla*) untuk mengisolasi layer tertentu.

- **Status Banner Sinkronisasi**:
  - 🟢 **Live & Synchronized**: Data diterima langsung dari API BMKG/USGS/PVMBG dalam kurun < 15 menit.
  - 🟡 **Cached / Degraded**: Jaringan eksternal mengalami latensi; sistem menyajikan data pengamatan terakhir yang tersimpan aman (*Circuit Breaker* aktif).

---

## 2. Perbedaan Peringatan Resmi vs Estimasi AI

Sistem menerapkan prinsip **Dual-Track Early Warning**:

| Fitur | 🔴 OFFICIAL GOVERNMENT ALERT | 🟡 AI RISK ESTIMATE |
|---|---|---|
| **Penerbit** | BMKG, PVMBG (ESDM), BNPB, BPBD, PUPR | Algoritma Pembelajaran Mesin NATURALGUARD AI |
| **Karakteristik** | Mandat hukum formal, mengikat secara operasional | Prakiraan probabilistik awal (*decision-support*) |
| **Tujuan** | Perintah evakuasi resmi, penutupan jalur penerbangan | Peningkatan kewaspadaan dini, deteksi anomali dini |
| **Sifat** | Tidak boleh ditimpa oleh skor model AI mana pun | Melengkapi area blind-spot yang belum terbit rilis resmi |

> [!IMPORTANT]
> Jika arahan evakuasi resmi BPBD/PVMBG telah diterbitkan, seluruh masyarakat diwajibkan mengikuti arahan resmi tersebut tanpa menunggu pembaruan skor AI.

---

## 3. Penjelasan Skor Risiko Terpadu (0–100)

Skor risiko dihitung menggunakan model multivariat terkalibrasi Platt Sigmoid:

$$R = 0.40 \cdot P_{cal} + 0.25 \cdot S + 0.20 \cdot E + 0.15 \cdot C$$

- **$P_{cal}$ (Hazard Probability, 0–100)**: Peluang terjadinya fenomena dalam jendela waktu prediksi.
- **$S$ (Severity Index, 0–100)**: Skala keparahan fisik (kecepatan angin, intensitas gempa MMI, tinggi genangan air).
- **$E$ (Exposure Score, 0–100)**: Jumlah populasi dan infrastruktur kritis (RS, sekolah, jalan nasional) dalam poligon bahaya.
- **$C$ (Confidence Score, 0–100)**: Kualitas dan kelengkapan sensor yang memvalidasi sinyal.

### Klasifikasi & Protokol Tanggap:
1. **0 – 19 (Low / Hijau)**: Kondisi normal. Pemantauan rutin harian.
2. **20 – 39 (Moderate / Biru)**: Peningkatan kelembapan/anomali kecil. Analis memantau tren sensor.
3. **40 – 59 (High / Kuning)**: Ambang waspada terlampaui. Notifikasi dikirimkan ke analis dan posko BPBD.
4. **60 – 79 (Very High / Oranye)**: Kondisi kritis. Kesiapsiagaan personil SAR dan relawan evakuasi.
5. **80 – 100 (Extreme / Merah)**: Bahaya ekstrem mengancam keselamatan jiwa. Evakuasi mandiri segera.

---

## 4. Panduan Operasional 8 Hazard Centers

1. **🌊 Banjir (Flood)**:
   - Menggunakan metode hidrologi *SCS-CN (Soil Conservation Service Curve Number)* dan persamaan hidraulika saluran terbuka *Manning*.
   - Parameter kritis: **Tinggi Muka Air (TMA)** terhadap ambang batas bahaya tanggul sungai.
2. **⛰️ Tanah Longsor (Landslide)**:
   - Menggunakan model stabilitas lereng tak hingga (*Infinite Slope Stability Factor of Safety / FS*) dan kurva empiris intensitas-durasi hujan tropis *Caine (1980)*.
   - Jika nilai $FS < 1.0$, lereng dalam kondisi labil kritis dan rentan runtuh.
3. **🌋 Gunung Api (Volcano)**:
   - Menggabungkan indeks anomali seismik termal *RSAM* dan *Normalized Thermal Index (NTI)* satelit inframerah gelombang menengah (MIR/NIR).
   - Selalu memetakan radius aman Kawasan Rawan Bencana (KRB) resmi PVMBG.
4. **⚡ Badai Petir (Thunderstorm)**:
   - Menggunakan konversi reflektivitas radar Doppler Marshall-Palmer ($Z-R$), indeks labilitas konvektif atmosfer *CAPE*, dan kerapatan sambaran petir real-time.
5. **🌪️ Angin Kencang & Puting Beliung (Wind)**:
   - Menggunakan indeks *Energy Helicity Index (EHI)* dan *Storm-Relative Environmental Helicity (SREH)* untuk mendeteksi potensi pusaran angin konvektif lokal.
6. **📈 Gempabumi & Tsunami (Earthquake)**:
   - Menggunakan persamaan atenuasi guncangan *Atkinson-Boore GMPE* untuk menghitung percepatan tanah puncak ($PGA$) dan skala intensitas $MMI$.
   - Mengevaluasi parameter pemicu tsunami InaTEWS (hiposenter bawah laut, kedalaman $\le 50$ km, $M \ge 7.0$).
7. **🔥 Kebakaran Hutan (Wildfire)**:
   - Menerapkan *Canadian Forest Fire Weather Index (FWI)* lengkap (FFMC, DMC, DC, ISI, BUI) dipadukan dengan deteksi termal satelit NASA FIRMS VIIRS 375m pada lahan gambut.
8. **🌀 Siklon Tropis & Cuaca Maritim (Cyclone)**:
   - Menggunakan profil tekanan-angin vorteks atmosfer *Holland (1980)* dan estimasi tinggi gelombang laut signifikan *Bretschneider*.

---

## 5. Penggunaan RAG Copilot & Voice Broadcast

- **NaturalGuard Copilot**:
  - Masuk ke tab **NaturalGuard Copilot**.
  - Ketikkan pertanyaan menggunakan Bahasa Indonesia natural (contoh: *"Bagaimana status Gunung Semeru?"*, *"Apakah ada peringatan cuaca di Surabaya hari ini?"*).
  - Copilot mengambil data langsung dari basis data sensor dan menyertakan sitasi sumber lembaga serta stempel waktu observasi.
- **AI Voice Broadcast (TTS)**:
  - Klik tombol **📢 Siarkan Peringatan (TTS)** di pojok kanan atas.
  - Peramban akan membacakan instruksi evakuasi atau peringatan dini aktif dengan suara natural Bahasa Indonesia.

---

## 6. Frequently Asked Questions (FAQ)

### Q1: Apakah NATURALGUARD AI memprediksi gempa bumi di masa depan?
**Jawab**: **TIDAK.** Sesuai konsensus ilmu geofisika global dan aturan resmi BMKG, waktu, lokasi, dan magnitudo pasti gempabumi tidak dapat diprediksi secara deterministik sebelum terjadi. NATURALGUARD AI hanya mendeteksi gempa yang telah terjadi, menghitung estimasi guncangan di berbagai kota, menghitung laju gempa susulan (*Omori-Utsu*), dan mengevaluasi potensi tsunami.

### Q2: Mengapa status data saya tertulis "STALE" atau "CACHED"?
**Jawab**: Jika server penyedia (misalnya API BMKG atau NASA) sedang mengalami gangguan koneksi atau perawatan server, arsitektur *Circuit Breaker* NATURALGUARD AI otomatis mencegah aplikasi crash dan menyajikan data observasi terakhir yang berhasil diunduh dengan label transparan `STALE`.

### Q3: Apakah masyarakat umum boleh menggunakan platform ini?
**Jawab**: Ya! Gunakan pemilih peran (*Role Selector*) di pojok kanan atas dan pilih `Public User` untuk melihat peta dan peringatan resmi, atau `Disaster Analyst` untuk melihat parameter teknis lengkap.

---

## 7. Panduan Integrasi REST API bagi Pengembang

Aplikasi lain (Mobile App BPBD, IoT Sirene Desa, Bot Telegram SAR) dapat mengakses data melalui REST API:

### Contoh 1: Mengambil Peringatan Dini Aktif (cURL)
```bash
curl -X GET "http://localhost:8000/api/v1/alerts?is_official=true" -H "accept: application/json"
```

### Contoh 2: Meminta Jawaban RAG Copilot (Python)
```python
import requests

payload = {"question": "Bagaimana risiko banjir di Bekasi?"}
response = requests.post("http://localhost:8000/api/v1/copilot/chat", json=payload)
data = response.json()
print("Jawaban AI:", data["answer"])
print("Sitasi Sumber:", data["citations"])
```

### Contoh 3: Mengambil GeoJSON Layer Risiko untuk GIS Map (JavaScript)
```javascript
fetch("http://localhost:8000/api/v1/risk-map?hazard=flood")
  .then(res => res.json())
  .then(geojson => {
    L.geoJSON(geojson).addTo(myMap);
  });
```
