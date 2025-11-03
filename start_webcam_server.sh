#!/bin/bash

echo "🚀 Starting Webcam UDP Server"
echo "=============================="

# Activate virtual environment if exists
if [ -d "mediapipe_env" ]; then
    source mediapipe_env/bin/activate
    echo "✅ Virtual environment activated"
fi

# Run webcam server
python webcam_server_udp.py
