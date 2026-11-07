@echo off
title NaturalGuard AI - Multi-Hazard Early Warning & Natural Disaster Platform
color 0B
echo ===================================================================
echo   NATURALGUARD AI - MULTI-HAZARD EARLY WARNING & DISASTER PLATFORM
echo   Official Data First * Multi-Source Fusion * AI Geospatial Intel
echo ===================================================================
echo.
echo [1/2] Menyiapkan server backend NaturalGuard AI...
cd /d "%~dp0backend"
pip install -r requirements.txt >nul 2>&1
echo.
echo [2/2] Membuka NaturalGuard AI Command Center di browser...
start "" "http://localhost:8000"
echo.
echo ===================================================================
echo Web Dashboard / Command Center: http://localhost:8000
echo Dokumentasi REST API (OpenAPI): http://localhost:8000/docs
echo ===================================================================
echo.
echo Server sedang berjalan... Tekan Ctrl+C untuk menutup.
python run.py
pause
