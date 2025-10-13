#!/bin/bash

# MediaPipe GUI Application Launcher
# Script untuk menjalankan aplikasi GUI MediaPipe

echo "🎯 MediaPipe Face & Hand Tracking GUI"
echo "======================================"

# Check if we're in the right directory
if [ ! -d "mediapipe_env" ]; then
    echo "❌ Error: Virtual environment 'mediapipe_env' tidak ditemukan!"
    echo "Pastikan Anda menjalankan script ini dari direktori project utama."
    exit 1
fi

echo "🔄 Mengaktifkan virtual environment..."
source mediapipe_env/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Error: Gagal mengaktifkan virtual environment!"
    exit 1
fi

echo "✅ Virtual environment aktif"
echo "🚀 Meluncurkan GUI application..."

cd mediapipe_app
python gui_app.py

echo "👋 GUI application ditutup"