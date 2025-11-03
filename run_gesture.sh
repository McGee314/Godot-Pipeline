#!/bin/bash

# Activate virtual environment
source mediapipe_env/bin/activate

# Run simple hand gesture tracker (NO GUI)
cd mediapipe_app
python hand_gesture_only.py
