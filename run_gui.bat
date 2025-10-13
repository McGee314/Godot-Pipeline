@echo off
REM MediaPipe GUI Application Launcher for Windows
REM Script untuk menjalankan aplikasi GUI MediaPipe di Windows

echo 🎯 MediaPipe Face ^& Hand Tracking GUI
echo ======================================

REM Check if we're in the right directory
if not exist "mediapipe_env" (
    echo ❌ Error: Virtual environment 'mediapipe_env' tidak ditemukan!
    echo Pastikan Anda menjalankan script ini dari direktori project utama.
    pause
    exit /b 1
)

echo 🔄 Mengaktifkan virtual environment...
call mediapipe_env\Scripts\activate.bat

if errorlevel 1 (
    echo ❌ Error: Gagal mengaktifkan virtual environment!
    pause
    exit /b 1
)

echo ✅ Virtual environment aktif
echo 🚀 Meluncurkan GUI application...

cd mediapipe_app
python gui_app.py

echo 👋 GUI application ditutup
pause