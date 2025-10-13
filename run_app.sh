#!/bin/bash

# Script untuk menjalankan MediaPipe Application
# Pastikan script ini dijalankan dari folder project utama

echo "=== MediaPipe Face & Hand Tracking App Setup ==="
echo "Mempersiapkan environment..."

# Aktivasi virtual environment
if [ -d "mediapipe_env" ]; then
    echo "Mengaktifkan virtual environment..."
    source mediapipe_env/bin/activate
    
    # Masuk ke folder aplikasi dan jalankan
    cd mediapipe_app
    echo "Menjalankan aplikasi..."
    python main.py
else
    echo "Error: Virtual environment 'mediapipe_env' tidak ditemukan!"
    echo "Pastikan Anda sudah membuat virtual environment dan install dependencies."
    echo "Jalankan setup manual berikut:"
    echo "1. python3 -m venv mediapipe_env"
    echo "2. source mediapipe_env/bin/activate"
    echo "3. pip install -r mediapipe_app/requirements.txt"
    echo "4. python mediapipe_app/main.py"
fi