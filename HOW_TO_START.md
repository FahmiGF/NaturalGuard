# 🚀 PANDUAN MEMULAI CEPAT (QUICK START GUIDE)
## NATURALGUARD AI — Multi-Hazard Early Warning & Natural Disaster Platform

Panduan ini berisi langkah-langkah praktis untuk mengunduh, menginstal, dan menjalankan platform **NATURALGUARD AI** di komputer lokal maupun server produksi.

---

## 📋 Prasyarat Sistem (System Requirements)

* **Sistem Operasi**: Windows 10/11, macOS, atau Linux (Ubuntu 20.04+ direkomendasikan).
* **Python**: Versi `3.10` atau lebih baru (`python --version`).
* **Web Browser**: Google Chrome, Microsoft Edge, Mozilla Firefox, atau Safari versi modern.
* **Node.js** *(Opsional)*: Diperlukan hanya jika ingin mengembangkan antarmuka mandiri via Next.js 15 (`frontend/`). Web Command Center bawaan sudah berjalan langsung tanpa perlu Node.js!
* **Docker** *(Opsional)*: Untuk deployment container.

---

## ⚡ Cara 1: Menjalankan 1-Klik di Windows (Paling Mudah)

Jika Anda menggunakan Windows, platform dapat dijalankan langsung tanpa mengetik perintah terminal apa pun:

1. Buka folder proyek:
   ```
   naturalguard-ai/
   ```
2. **Klik dua kali** file berikut:
   ```cmd
   Buka_NaturalGuard_AI.bat
   ```
3. Skrip otomatis akan:
   * Memeriksa dan menginstal paket dependensi Python.
   * Menjalankan server asinkron FastAPI pada port `8000`.
   * Membuka peramban (*browser*) secara otomatis ke alamat:
     * 🌐 **Dashboard Command Center**: [http://localhost:8000](http://localhost:8000)
     * 📚 **Dokumentasi REST API**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 💻 Cara 2: Menjalankan Manual via Terminal (Windows, macOS, Linux)

### 1. Kloning Repositori dari GitHub
```bash
git clone https://github.com/FahmiGF/NaturalGuard.git
cd NaturalGuard
```

### 2. Pindah ke Direktori Backend & Siapkan Virtual Environment (Disarankan)
```bash
cd backend

# Membuat virtual environment (opsional tapi disarankan)
python -m venv venv

# Aktivasi di Windows:
venv\Scripts\activate

# Atau aktivasi di macOS/Linux:
source venv/bin/activate
```

### 3. Instal Dependensi Python
```bash
pip install -r requirements.txt
```

### 4. Jalankan Server
```bash
python run.py
```

Output terminal akan menampilkan:
```
============================================================
 🛡️  NATURALGUARD AI — Early Warning & Disaster Platform
 🌐 Dashboard: http://localhost:8000
 📚 OpenAPI Docs: http://localhost:8000/docs
============================================================
```

Buka peramban Anda di **`http://localhost:8000`**.

---

## 🐳 Cara 3: Menjalankan via Docker & Docker Compose (Server / DevOps)

Bagi pengembang yang ingin menjalankan platform terisolasi di dalam container:

```bash
# Pastikan berada di root folder NaturalGuard
docker-compose up --build -d
```

Layanan yang aktif:
* **NaturalGuard Backend & Dashboard**: `http://localhost:8000`
* **Redis Caching Engine**: `localhost:6379`

Untuk menghentikan container:
```bash
docker-compose down
```

---

## ⚛️ Cara 4: Menjalankan Frontend Next.js 15 (Khusus Pengembang Web)

Jika Anda ingin memodifikasi atau mengembangkan frontend terpisah menggunakan Next.js 15, React 19, dan TypeScript:

```bash
cd frontend
npm install
npm run dev
```

Buka peramban di **`http://localhost:3000`**.

---

## 🧭 Tur Fitur Utama: Langkah Pertama Penggunaan

Setelah aplikasi terbuka di peramban, Anda dapat langsung mencoba fitur-fitur berikut:

1. **🗺️ Eksplorasi Peta Geospasial Multi-Bencana**:
   * Klik marker lingkaran berwarna di peta untuk melihat detail parameter bencana (TMA sungai, kemiringan lereng, level kawah Semeru, kedalaman gempa, dll).
   * Gunakan dropdown **`Tile: Carto Dark`** untuk berganti ke **`Esri Satelit Asli`**, **`OpenStreetMap`**, atau **`OpenTopoMap Kontur Lereng`**.
   * Klik tombol **`🌧️ Radar Hujan`** untuk menampilkan mosaik awan radar presipitasi *live*.

2. **⚠️ Cermati Dual-Track Peringatan Dini**:
   * Perhatikan banner merah (**🔴 OFFICIAL GOVERNMENT ALERT**) untuk instruksi evakuasi resmi BPBD/BMKG.
   * Perhatikan banner kuning (**🟡 AI RISK ESTIMATE**) untuk peringatan deteksi dini model machine learning.

3. **📢 Uji Siaran Suara Darurat (TTS)**:
   * Klik tombol **`📢 Siarkan Peringatan (TTS)`** di pojok kanan atas.
   * Aplikasi akan membacakan peringatan terkini dengan sintesis suara Bahasa Indonesia.

4. **🤖 Berinteraksi dengan NaturalGuard Copilot (RAG)**:
   * Buka tab **`NaturalGuard Copilot`**.
   * Coba klik salah satu pertanyaan cepat, misalnya:
     * *"Bagaimana kondisi risiko banjir di Bekasi?"*
     * *"Bagaimana status Gunung Semeru saat ini?"*
   * Asisten akan menjawab dengan sitasi sumber resmi (BMKG, PVMBG, BNPB) dan stempel waktu data.

5. **🌐 Akses Portal Resmi Otoritas**:
   * Buka tab **`Portal Referensi Resmi`**.
   * Telusuri 8 portal nasional & global (BMKG InaTEWS, BNPB InaRISK, PVMBG MAGMA, NASA FIRMS, USGS, GDACS, PUPR SITABA).
   * Gunakan fitur *Interactive In-App Viewer* atau buka langsung di tab baru.

---

## 🧪 Menjalankan Pengujian Otomatis & Verifikasi Model

Anda dapat memverifikasi keandalan sistem kapan saja menggunakan rangkaian tes bawaan:

### 1. Uji Konkurensi & Fuzzing (1.000 Requests)
```bash
python tests/stress_test.py
```
*(Menghasilkan metrik throughput requests/sec dan latensi P95).*

### 2. Uji Unit Matematika & Fisika 8 Hazard Engines
```bash
python tests/test_ai_engines.py
```
*(Memvalidasi perhitungan hidrologi SCS-CN, stabilitas lereng FS, atenuasi gempa GMPE, FWI kebakaran hutan, dan formula skoring risiko terkalibrasi).*

---

## 🛠️ Pemecahan Masalah (Troubleshooting)

### Port 8000 Sedang Digunakan Aplikasi Lain?
Server dirancang cerdas dengan mekanisme *fallback port* otomatis: jika port `8000` sedang terpakai, server otomatis beralih ke port `8005`. Periksa tautan yang tercetak di konsol terminal Anda.

### Suara TTS Tidak Terdengar?
Pastikan volume komputer Anda aktif dan peramban telah diberi izin memutar audio (*autoplay permission*). Fitur ini menggunakan Web Speech API standar pada Chrome, Edge, dan Safari.

### Dependensi Python Gagal Diinstal?
Pastikan Anda menggunakan Python versi 3.10 ke atas dan perbarui *pip*:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

*NaturalGuard AI — Official Data First, AI-Assisted Second.*
