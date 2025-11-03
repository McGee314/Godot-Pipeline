#!/usr/bin/env python3
"""
Simple Hand Gesture Tracking for Godot
Langsung kirim gesture ke Godot tanpa GUI
"""

import cv2
import mediapipe as mp
import socket
import json
import time

class SimpleHandGesture:
    def __init__(self):
        """Initialize hand tracking and UDP sender"""
        # MediaPipe setup
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # UDP setup for Godot
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_host = '127.0.0.1'
        self.udp_port = 9999
        
        # Rate limiting
        self.last_gesture = None
        self.last_time = 0.0
        
        print("🚀 Hand Gesture Tracker Started")
        print(f"📡 Sending to Godot: {self.udp_host}:{self.udp_port}")
        print("❌ Press 'q' to quit")
        print("=" * 50)
    
    def get_gesture(self, landmarks, width, height):
        """Detect gesture direction from hand landmarks"""
        if not landmarks:
            return "NO_HAND"
        
        # Get wrist position
        wrist = landmarks.landmark[0]
        x = int(wrist.x * width)
        y = int(wrist.y * height)
        
        # Calculate center and threshold
        cx, cy = width // 2, height // 2
        threshold = 100
        
        # Determine direction
        if y < cy - threshold:
            return "UP"
        elif y > cy + threshold:
            return "DOWN"
        elif x < cx - threshold:
            return "LEFT"
        elif x > cx + threshold:
            return "RIGHT"
        else:
            return "CENTER"
    
    def send_to_godot(self, gesture):
        """Send gesture via UDP to Godot"""
        current_time = time.time()
        
        # Rate limiting: send only if changed or 100ms passed
        if gesture == self.last_gesture and (current_time - self.last_time) < 0.1:
            return
        
        try:
            message = {
                "type": "gesture",
                "gesture": gesture,
                "timestamp": current_time
            }
            
            data = json.dumps(message).encode('utf-8')
            self.udp_socket.sendto(data, (self.udp_host, self.udp_port))
            
            self.last_gesture = gesture
            self.last_time = current_time
            
            # Print only active gestures
            if gesture not in ["CENTER", "NO_HAND"]:
                print(f"👋 {gesture}")
                
        except Exception as e:
            print(f"⚠️ UDP Error: {e}")
    
    def run(self):
        """Main loop"""
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Cannot access camera")
            return
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Mirror effect
            frame = cv2.flip(frame, 1)
            h, w = frame.shape[:2]
            
            # Process frame
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb)
            
            # Detect gesture
            landmarks = None
            if results.multi_hand_landmarks:
                landmarks = results.multi_hand_landmarks[0]
                self.mp_drawing.draw_landmarks(
                    frame, landmarks, self.mp_hands.HAND_CONNECTIONS
                )
            
            gesture = self.get_gesture(landmarks, w, h)
            
            # Send to Godot
            self.send_to_godot(gesture)
            
            # Display
            color = (0, 255, 0) if gesture not in ["NO_HAND", "CENTER"] else (128, 128, 128)
            cv2.putText(frame, f"GESTURE: {gesture}", 
                       (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            
            # Draw reference lines
            cv2.line(frame, (w//2, 0), (w//2, h), (200, 200, 200), 1)
            cv2.line(frame, (0, h//2), (w, h//2), (200, 200, 200), 1)
            
            cv2.imshow('Hand Gesture -> Godot', frame)
            
            # Quit on 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        self.udp_socket.close()
        print("\n✅ Stopped")

if __name__ == "__main__":
    tracker = SimpleHandGesture()
    tracker.run()
