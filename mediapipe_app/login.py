import cv2
import sys
import os
import socket
import struct
import time
import mediapipe as mp

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

class FaceLoginSystem:
    def __init__(self, send_udp=True, udp_host='127.0.0.1', udp_port=5000):
        """
        Initialize Face Login System
        
        Args:
            send_udp: If True, send video frames via UDP to Godot
            udp_host: UDP destination host
            udp_port: UDP destination port
        """
        # MediaPipe Face Detection
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=0, min_detection_confidence=0.7)  # Increased from 0.5 to 0.7 for stricter detection
        
        self.is_logged_in = False
        self.send_udp = send_udp
        self.udp_host = udp_host
        self.udp_port = udp_port
        self.udp_socket = None
        
        # UDP streaming settings (matching godot_udp_server.py)
        self.sequence_number = 0
        self.max_packet_size = 60000  # 60KB per packet (safe for UDP)
        self.jpeg_quality = 80  # JPEG quality (0-100)
        
        if self.send_udp:
            self.setup_udp()
    
    def setup_udp(self):
        """Setup UDP socket for sending video frames to Godot"""
        try:
            self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Set larger send buffer to handle fragmented packets
            self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)  # 64KB send buffer
            print(f"✅ UDP socket created: {self.udp_host}:{self.udp_port}")
            print(f"📦 Max packet size: {self.max_packet_size} bytes")
            print(f"🎨 JPEG quality: {self.jpeg_quality}%")
        except Exception as e:
            print(f"❌ Error creating UDP socket: {e}")
            self.send_udp = False
    
    def send_frame_udp(self, frame):
        """
        Send frame via UDP to Godot with packet fragmentation.
        Uses same protocol as godot_udp_server.py:
        
        Packet Format:
        [sequence_number:4][total_packets:4][packet_index:4][JPEG_data_chunk...]
        
        Args:
            frame: OpenCV frame to send
        """
        if not self.send_udp or self.udp_socket is None:
            return
        
        try:
            # Encode frame as JPEG
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), self.jpeg_quality]
            _, jpeg_buffer = cv2.imencode('.jpg', frame, encode_param)
            jpeg_bytes = jpeg_buffer.tobytes()
            
            frame_size = len(jpeg_bytes)
            
            # Calculate number of packets needed
            total_packets = (frame_size + self.max_packet_size - 1) // self.max_packet_size
            
            # Send each fragment
            for packet_index in range(total_packets):
                # Calculate chunk boundaries
                start = packet_index * self.max_packet_size
                end = min(start + self.max_packet_size, frame_size)
                chunk = jpeg_bytes[start:end]
                
                # Build packet: [seq_num:4][total_packets:4][packet_index:4][data...]
                header = struct.pack('>III', self.sequence_number, total_packets, packet_index)
                packet = header + chunk
                
                # Send packet
                self.udp_socket.sendto(packet, (self.udp_host, self.udp_port))
                
                # Add minimal delay between packets to prevent UDP buffer overflow
                if packet_index < total_packets - 1:
                    time.sleep(0.0005)  # 0.5ms delay
            
            # Increment sequence number
            self.sequence_number = (self.sequence_number + 1) % 65536
            
        except Exception as e:
            print(f"❌ Error sending frame via UDP: {e}")
    
    def send_gesture_udp(self, gesture_message):
        """Send gesture/status message via UDP to Godot"""
        if not self.send_udp or self.udp_socket is None:
            return
        
        try:
            message = f"gesture:{gesture_message}"
            self.udp_socket.sendto(message.encode('utf-8'), (self.udp_host, self.udp_port))
        except Exception as e:
            print(f"Error sending gesture via UDP: {e}")
    
    def detect_face(self, frame):
        """
        Detect face in frame using MediaPipe with strict validation
        Returns: (has_face, processed_frame, face_count)
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.face_detection.process(rgb_frame)
        
        has_face = False
        face_count = 0
        
        if results.detections:
            # Validate each detection
            for detection in results.detections:
                # Get detection score (confidence)
                score = detection.score[0]
                
                # Only count if confidence is high enough
                if score >= 0.7:  # Strict threshold
                    face_count += 1
                    has_face = True
                    
                    # Draw detection annotations on the image
                    self.mp_drawing.draw_detection(frame, detection)
                    
                    # Add confidence text
                    bbox = detection.location_data.relative_bounding_box
                    h, w, _ = frame.shape
                    x = int(bbox.xmin * w)
                    y = int(bbox.ymin * h)
                    
                    # Display confidence percentage
                    cv2.putText(frame, f"{int(score * 100)}%", 
                               (x, max(y - 10, 20)), 
                               cv2.FONT_HERSHEY_SIMPLEX, 
                               0.6, (0, 255, 0), 2)
        
        # Add status text on frame
        if has_face:
            cv2.putText(frame, f"FACE_DETECTED:{face_count}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                       1, (0, 255, 0), 3)
        else:
            cv2.putText(frame, "NO_FACE_DETECTED", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                       1, (0, 0, 255), 3)
                
        return has_face, frame, face_count
    
    def welcome_screen(self):
        """Display welcome message"""
        print("=" * 50)
        print("   VIDEO STREAMING TO GODOT")
        print("=" * 50)
        print("Mode: UDP Video Streamer WITH Face Detection")
        if self.send_udp:
            print(f"📡 UDP Target: {self.udp_host}:{self.udp_port}")
        print("✅ MediaPipe Face Detection: AKTIF")
        print("Login akan dihandle oleh Godot")
        print("Tekan Ctrl+C untuk keluar")
        print("=" * 50)
    
    def stream_video(self):
        """Stream video continuously to Godot WITH face detection visualization"""
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Error: Tidak dapat mengakses kamera")
            return False
            
        print("\n🎥 Camera aktif - Streaming ke Godot...")
        print("📡 Menunggu koneksi dari Godot...")
        print("👤 Face detection AKTIF - wajah akan ditandai dengan kotak hijau")
        print("Tekan Ctrl+C untuk keluar")
        print("\n💡 Instruksi:")
        print("   1. Buka Godot dan jalankan Login.tscn")
        print("   2. Klik tombol 'CONNECT CAMERA' di Godot")
        print("   3. Video dengan face detection akan muncul di Godot")
        print("   4. Godot akan menghitung deteksi wajah untuk login")
        print("")
        
        frame_count = 0
        faces_detected = 0
        total_faces_count = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("❌ Error: Tidak dapat membaca frame dari kamera")
                    break
                
                frame_count += 1
                
                # Detect face and draw annotations
                has_face, processed_frame, face_count = self.detect_face(frame)
                
                # Count faces for statistics
                if has_face:
                    faces_detected += 1
                    total_faces_count += face_count
                
                # Stream the processed frame (with face detection boxes)
                if self.send_udp:
                    self.send_frame_udp(processed_frame)
                
                # Print status every 60 frames (~2 seconds)
                if frame_count % 60 == 0:
                    face_percentage = (faces_detected / frame_count) * 100
                    avg_faces = total_faces_count / max(faces_detected, 1)
                    print(f"📡 Streaming... (frames: {frame_count}, face detected: {face_percentage:.1f}%, avg faces: {avg_faces:.1f})")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Streaming dihentikan oleh user")
        except Exception as e:
            print(f"❌ Error saat streaming: {e}")
        finally:
            cap.release()
            if self.udp_socket:
                self.udp_socket.close()
            print("🔌 Camera dan UDP socket closed")
        
        return True
    
    def run(self):
        """Run the video streaming system - just stream, don't handle login"""
        try:
            self.welcome_screen()
            print()
            self.stream_video()
                    
        except KeyboardInterrupt:
            print("\n\n⚠️  Aplikasi dihentikan oleh user.")
        except Exception as e:
            print(f"❌ Error tidak terduga: {e}")
        finally:
            if self.udp_socket:
                self.udp_socket.close()
                print("🔌 UDP socket closed")

# Main entry point
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Face Detection Login System with UDP')
    parser.add_argument('--no-udp', action='store_true', help='Disable UDP streaming')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='UDP host (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5000, help='UDP port (default: 5000)')
    
    args = parser.parse_args()
    
    login_system = FaceLoginSystem(
        send_udp=not args.no_udp,
        udp_host=args.host,
        udp_port=args.port
    )
    login_system.run()
