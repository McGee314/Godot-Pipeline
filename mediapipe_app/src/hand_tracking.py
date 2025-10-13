import cv2
import mediapipe as mp
import numpy as np

class HandTracker:
    def __init__(self):
        """Initialize MediaPipe Hand Tracking"""
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
    def detect_hands(self, frame):
        """
        Detect hands in frame
        Returns: (hand_landmarks, processed_frame)
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.hands.process(rgb_frame)
        
        hand_landmarks = None
        if results.multi_hand_landmarks:
            # Draw hand landmarks
            for hand_landmark in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmark, self.mp_hands.HAND_CONNECTIONS)
                hand_landmarks = hand_landmark
                
        return hand_landmarks, frame
    
    def get_gesture_direction(self, landmarks, frame_width, frame_height):
        """
        Determine gesture direction based on hand position
        Returns: direction string (UP, DOWN, LEFT, RIGHT, CENTER)
        """
        if landmarks is None:
            return "NO_HAND"
        
        # Get wrist position (landmark 0)
        wrist = landmarks.landmark[0]
        wrist_x = int(wrist.x * frame_width)
        wrist_y = int(wrist.y * frame_height)
        
        # Define screen regions
        center_x = frame_width // 2
        center_y = frame_height // 2
        threshold = 100  # Pixel threshold for gesture detection
        
        # Determine direction based on wrist position relative to center
        if wrist_y < center_y - threshold:
            return "UP"
        elif wrist_y > center_y + threshold:
            return "DOWN"
        elif wrist_x < center_x - threshold:
            return "LEFT"
        elif wrist_x > center_x + threshold:
            return "RIGHT"
        else:
            return "CENTER"
    
    def gesture_control_system(self):
        """
        Hand tracking gesture control system
        """
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Tidak dapat mengakses kamera")
            return
            
        print("=== SISTEM GESTURE CONTROL ===")
        print("Gunakan tangan Anda untuk kontrol:")
        print("- Gerakkan tangan ke ATAS, BAWAH, KIRI, atau KANAN")
        print("- Tekan 'q' untuk keluar")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Tidak dapat membaca frame dari kamera")
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            frame_height, frame_width = frame.shape[:2]
            
            # Detect hands
            landmarks, processed_frame = self.detect_hands(frame)
            
            # Get gesture direction
            direction = self.get_gesture_direction(landmarks, frame_width, frame_height)
            
            # Draw direction on screen
            if direction != "NO_HAND":
                color = (0, 255, 0) if direction != "CENTER" else (255, 255, 0)
                cv2.putText(processed_frame, f"ARAH: {direction}", 
                           (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                print(f"Gesture detected: {direction}")
            else:
                cv2.putText(processed_frame, "Tidak ada tangan terdeteksi", 
                           (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            # Draw center lines for reference
            cv2.line(processed_frame, (frame_width//2, 0), 
                    (frame_width//2, frame_height), (255, 255, 255), 1)
            cv2.line(processed_frame, (0, frame_height//2), 
                    (frame_width, frame_height//2), (255, 255, 255), 1)
            
            # Draw zones
            cv2.putText(processed_frame, "UP", (frame_width//2-20, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(processed_frame, "DOWN", (frame_width//2-30, frame_height-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(processed_frame, "LEFT", (10, frame_height//2), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(processed_frame, "RIGHT", (frame_width-80, frame_height//2), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow('Hand Gesture Control', processed_frame)
            
            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

# Test function
if __name__ == "__main__":
    tracker = HandTracker()
    tracker.gesture_control_system()