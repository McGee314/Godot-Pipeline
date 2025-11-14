import cv2
import mediapipe as mp
import numpy as np
import socket
import json
import time
import os

class HandTracker:
    def __init__(self):
        """Initialize MediaPipe Hand Tracking"""
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,  # Detect 2 hands (left and right)
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        
        # UDP Configuration for Godot communication
        self.udp_host = os.getenv('GESTURE_UDP_HOST', '127.0.0.1')
        self.udp_port = int(os.getenv('GESTURE_UDP_PORT', '9999'))
        self.udp_socket = None
        self.last_sent_gesture = None
        self.last_sent_time = 0.0
        
        # Initialize UDP socket
        try:
            self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.udp_socket.settimeout(0.1)
            print(f"✅ UDP gesture sender initialized: {self.udp_host}:{self.udp_port}")
        except Exception as e:
            print(f"⚠️ Failed to initialize UDP socket: {e}")
            self.udp_socket = None
        
    def detect_hands(self, frame):
        """
        Detect hands in frame
        Returns: (results, processed_frame) - results contains multi_hand_landmarks and multi_handedness
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            # Draw hand landmarks for all detected hands
            for hand_landmark in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmark, self.mp_hands.HAND_CONNECTIONS)
                
        return results, frame
    
    def count_fingers(self, landmarks):
        """
        Count number of extended fingers
        Returns: number of fingers up (0-5)
        """
        # Finger tip and PIP landmark indices
        finger_tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
        finger_pips = [3, 6, 10, 14, 18]  # PIP joints
        
        fingers_up = 0
        
        # Thumb (special case - check horizontal distance)
        if landmarks[finger_tips[0]].x < landmarks[finger_pips[0]].x:
            fingers_up += 1
        
        # Other 4 fingers (check if tip is above PIP)
        for i in range(1, 5):
            if landmarks[finger_tips[i]].y < landmarks[finger_pips[i]].y:
                fingers_up += 1
        
        return fingers_up
    
    def get_hand_tilt(self, landmarks):
        """
        Detect if hand is tilted left or right based on wrist and middle finger base
        Returns: "LEFT", "RIGHT", or "STRAIGHT"
        """
        wrist = landmarks[0]
        middle_base = landmarks[9]
        
        # Calculate horizontal distance
        x_diff = middle_base.x - wrist.x
        
        # Threshold for tilt detection
        tilt_threshold = 0.05
        
        if x_diff > tilt_threshold:
            return "RIGHT"
        elif x_diff < -tilt_threshold:
            return "LEFT"
        else:
            return "STRAIGHT"
    
    def detect_gesture(self, landmarks, hand_label):
        """
        Detect gesture based on finger count and hand tilt
        
        Left hand gestures (WASD movement):
        - 1 finger straight: FORWARD (W)
        - 1 finger tilted right: RIGHT (D)
        - 1 finger tilted left: LEFT (A)
        - 2 fingers: BACKWARD (S)
        
        Right hand gestures (Vertical + Rotation):
        - 1 finger straight: UP
        - 2 fingers: DOWN
        - 1 finger tilted right: ROTATE_RIGHT
        - 1 finger tilted left: ROTATE_LEFT
        
        Returns: gesture command string
        """
        finger_count = self.count_fingers(landmarks)
        hand_tilt = self.get_hand_tilt(landmarks)
        
        if hand_label == "Left":  # Left hand = WASD
            if finger_count == 1:
                if hand_tilt == "RIGHT":
                    return "RIGHT"  # D
                elif hand_tilt == "LEFT":
                    return "LEFT"  # A
                else:
                    return "FORWARD"  # W
            elif finger_count == 2:
                return "BACKWARD"  # S
        
        elif hand_label == "Right":  # Right hand = Up/Down + Rotation
            if finger_count == 1:
                if hand_tilt == "RIGHT":
                    return "ROTATE_RIGHT"
                elif hand_tilt == "LEFT":
                    return "ROTATE_LEFT"
                else:
                    return "UP"  # Straight up
            elif finger_count == 2:
                return "DOWN"
        
        return None
    
    def gesture_control_system(self):
        """
        Hand tracking gesture control system with 2 hands
        """
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Tidak dapat mengakses kamera")
            return
            
        print("=== SISTEM GESTURE CONTROL ===")
        print("Kontrol dengan 2 tangan:")
        print("\n👈 TANGAN KIRI (Movement - WASD):")
        print("   - 1 jari lurus: MAJU (W)")
        print("   - 1 jari miring kanan: KANAN (D)")
        print("   - 1 jari miring kiri: KIRI (A)")
        print("   - 2 jari: MUNDUR (S)")
        print("\n👉 TANGAN KANAN (Vertical + Rotation):")
        print("   - 1 jari lurus: NAIK (UP)")
        print("   - 2 jari: TURUN (DOWN)")
        print("   - 1 jari miring kanan: ROTASI KANAN")
        print("   - 1 jari miring kiri: ROTASI KIRI")
        print("\nTekan 'q' untuk keluar")
        print("=" * 50)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Tidak dapat membaca frame dari kamera")
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            frame_height, frame_width = frame.shape[:2]
            
            # Detect hands
            results, processed_frame = self.detect_hands(frame)
            
            # Process each detected hand
            left_gesture = None
            right_gesture = None
            
            if results.multi_hand_landmarks and results.multi_handedness:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    # Get hand label (Left or Right)
                    hand_label = handedness.classification[0].label
                    
                    # Detect gesture for this hand
                    gesture = self.detect_gesture(hand_landmarks.landmark, hand_label)
                    
                    if hand_label == "Left":
                        left_gesture = gesture
                    else:
                        right_gesture = gesture
                    
                    # Draw hand label on screen
                    wrist = hand_landmarks.landmark[0]
                    x = int(wrist.x * frame_width)
                    y = int(wrist.y * frame_height)
                    
                    # Draw finger count for debugging
                    finger_count = self.count_fingers(hand_landmarks.landmark)
                    tilt = self.get_hand_tilt(hand_landmarks.landmark)
                    
                    cv2.putText(processed_frame, f"{hand_label}: {finger_count} fingers", 
                               (x - 50, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                    cv2.putText(processed_frame, f"Tilt: {tilt}", 
                               (x - 50, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
            
            # Display detected gestures
            y_offset = 30
            if left_gesture:
                cv2.putText(processed_frame, f"LEFT HAND: {left_gesture}", 
                           (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                self.send_gesture_to_godot(left_gesture)
                y_offset += 35
            
            if right_gesture:
                cv2.putText(processed_frame, f"RIGHT HAND: {right_gesture}", 
                           (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                self.send_gesture_to_godot(right_gesture)
                y_offset += 35
            
            if not left_gesture and not right_gesture:
                cv2.putText(processed_frame, "Tunjukkan tangan Anda", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
            # Draw instruction overlay
            cv2.putText(processed_frame, "L: WASD | R: UP/DOWN/Rotation", 
                       (10, frame_height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            cv2.imshow('Hand Gesture Control', processed_frame)
            
            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
    
    def send_gesture_to_godot(self, gesture):
        """Send gesture command to Godot via UDP"""
        if not self.udp_socket:
            return
        
        # Rate limiting: only send if gesture changed or 100ms passed
        current_time = time.time()
        if gesture == self.last_sent_gesture and (current_time - self.last_sent_time) < 0.1:
            return
        
        try:
            # Create JSON message
            message = {
                "type": "gesture",
                "gesture": gesture,
                "timestamp": current_time
            }
            
            # Send to Godot
            data = json.dumps(message).encode('utf-8')
            self.udp_socket.sendto(data, (self.udp_host, self.udp_port))
            
            self.last_sent_gesture = gesture
            self.last_sent_time = current_time
            
            # Debug output
            if gesture != "CENTER":
                print(f"📤 Sent to Godot: {gesture}")
                
        except Exception as e:
            print(f"⚠️ Failed to send gesture: {e}")

# Test function
if __name__ == "__main__":
    tracker = HandTracker()
    tracker.gesture_control_system()