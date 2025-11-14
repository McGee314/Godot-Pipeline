import cv2
import sys
import os
import socket
import struct

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.face_detection import FaceDetector

class FaceDetectionSystem:
    def __init__(self, send_udp=False, udp_host='127.0.0.1', udp_port=5000):
        """
        Initialize Face Detection System
        
        Args:
            send_udp: If True, send video frames via UDP
            udp_host: UDP destination host
            udp_port: UDP destination port
        """
        self.face_detector = FaceDetector()
        self.send_udp = send_udp
        self.udp_host = udp_host
        self.udp_port = udp_port
        self.udp_socket = None
        
        if self.send_udp:
            self.setup_udp()
        
    def setup_udp(self):
        """Setup UDP socket for sending video frames"""
        try:
            self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print(f"✅ UDP socket created: {self.udp_host}:{self.udp_port}")
        except Exception as e:
            print(f"❌ Error creating UDP socket: {e}")
            self.send_udp = False
    
    def send_frame_udp(self, frame):
        """Send frame via UDP"""
        if not self.send_udp or self.udp_socket is None:
            return
        
        try:
            # Encode frame as JPEG
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            data = buffer.tobytes()
            
            # Send frame data
            self.udp_socket.sendto(data, (self.udp_host, self.udp_port))
        except Exception as e:
            print(f"Error sending frame via UDP: {e}")
    
    def welcome_screen(self):
        """Display welcome message"""
        print("=" * 50)
        print("   FACE DETECTION SYSTEM")
        print("=" * 50)
        print("Sistem deteksi wajah continuous")
        print("Wajah akan dideteksi secara real-time")
        if self.send_udp:
            print(f"📡 Mengirim video ke: {self.udp_host}:{self.udp_port}")
        print("=" * 50)
    
    def detection_process(self):
        """Run continuous face detection"""
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Error: Tidak dapat mengakses kamera")
            return False
            
        print("\n=== DETEKSI WAJAH AKTIF ===")
        print("Tekan 'q' untuk keluar")
        print("Tekan 's' untuk screenshot")
        
        frame_count = 0
        face_count = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Error: Tidak dapat membaca frame dari kamera")
                    break
                    
                frame_count += 1
                
                # Detect face
                has_face, processed_frame = self.face_detector.detect_face(frame)
                
                if has_face:
                    face_count += 1
                
                # Display statistics
                detection_rate = (face_count / frame_count * 100) if frame_count > 0 else 0
                cv2.putText(processed_frame, f"Frames: {frame_count} | Detections: {face_count}", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                cv2.putText(processed_frame, f"Detection Rate: {detection_rate:.1f}%", 
                           (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                if has_face:
                    cv2.putText(processed_frame, "WAJAH TERDETEKSI", 
                               (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                else:
                    cv2.putText(processed_frame, "Tidak ada wajah", 
                               (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                
                # Send frame via UDP if enabled
                if self.send_udp:
                    self.send_frame_udp(processed_frame)
                    cv2.putText(processed_frame, f"UDP: {self.udp_host}:{self.udp_port}", 
                               (10, processed_frame.shape[0] - 10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
                
                cv2.imshow('Face Detection System', processed_frame)
                
                # Handle key press
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    # Save screenshot
                    filename = f"screenshot_{frame_count}.jpg"
                    cv2.imwrite(filename, processed_frame)
                    print(f"📸 Screenshot saved: {filename}")
            
        except KeyboardInterrupt:
            print("\n\nDeteksi dihentikan oleh user.")
        finally:
            cap.release()
            cv2.destroyAllWindows()
            if self.udp_socket:
                self.udp_socket.close()
        
        print(f"\n=== STATISTIK DETEKSI ===")
        print(f"Total Frames: {frame_count}")
        print(f"Total Detections: {face_count}")
        print(f"Detection Rate: {detection_rate:.1f}%")
        
        return True
    
    def run(self):
        """Run the detection system"""
        try:
            self.welcome_screen()
            input("\nTekan Enter untuk memulai deteksi...")
            self.detection_process()
            
        except KeyboardInterrupt:
            print("\n\nAplikasi dihentikan oleh user.")
        except Exception as e:
            print(f"Error tidak terduga: {e}")

# Main entry point
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Face Detection System')
    parser.add_argument('--udp', action='store_true', help='Enable UDP streaming')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='UDP host (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5000, help='UDP port (default: 5000)')
    
    args = parser.parse_args()
    
    detection_system = FaceDetectionSystem(
        send_udp=args.udp,
        udp_host=args.host,
        udp_port=args.port
    )
    detection_system.run()
