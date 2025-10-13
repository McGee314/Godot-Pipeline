import cv2
import mediapipe as mp
import time

class FaceDetector:
    def __init__(self):
        """Initialize MediaPipe Face Detection"""
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=0, min_detection_confidence=0.5)
        
    def detect_face(self, frame):
        """
        Detect face in frame
        Returns: (has_face, processed_frame)
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.face_detection.process(rgb_frame)
        
        has_face = False
        if results.detections:
            has_face = True
            # Draw detection annotations on the image
            for detection in results.detections:
                self.mp_drawing.draw_detection(frame, detection)
                
        return has_face, frame
    
    def login_system(self):
        """
        Face detection login system
        Returns True if login successful, False otherwise
        """
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Tidak dapat mengakses kamera")
            return False
            
        print("=== SISTEM LOGIN FACE DETECTION ===")
        print("Posisikan wajah Anda di depan kamera...")
        print("Tekan 'q' untuk keluar")
        
        login_success = False
        face_detected_time = 0
        required_detection_time = 2  # 2 detik deteksi wajah untuk login sukses
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Tidak dapat membaca frame dari kamera")
                break
                
            # Detect face
            has_face, processed_frame = self.detect_face(frame)
            
            # Login logic
            if has_face:
                face_detected_time += 1
                cv2.putText(processed_frame, f"Wajah Terdeteksi! {face_detected_time}/60", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # Login berhasil setelah 2 detik (60 frames pada 30 FPS)
                if face_detected_time >= 60:
                    cv2.putText(processed_frame, "LOGIN SUCCESS!", 
                               (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.imshow('Face Detection Login', processed_frame)
                    cv2.waitKey(2000)  # Tampilkan pesan sukses selama 2 detik
                    login_success = True
                    break
            else:
                face_detected_time = 0
                cv2.putText(processed_frame, "Wajah tidak terdeteksi", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            cv2.imshow('Face Detection Login', processed_frame)
            
            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        return login_success

# Test function
if __name__ == "__main__":
    detector = FaceDetector()
    result = detector.login_system()
    if result:
        print("✅ Login berhasil!")
    else:
        print("❌ Login gagal!")