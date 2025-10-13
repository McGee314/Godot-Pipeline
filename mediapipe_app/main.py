import cv2
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.face_detection import FaceDetector
from src.hand_tracking import HandTracker

class MediaPipeApp:
    def __init__(self):
        """Initialize MediaPipe Application"""
        self.face_detector = FaceDetector()
        self.hand_tracker = HandTracker()
        self.is_logged_in = False
        
    def welcome_screen(self):
        """Display welcome message"""
        print("=" * 50)
        print("   MEDIAPIPE FACE & HAND TRACKING APP")
        print("=" * 50)
        print("Aplikasi ini memiliki 2 mode:")
        print("1. Face Detection Login - Login menggunakan deteksi wajah")
        print("2. Hand Gesture Control - Kontrol gesture menggunakan tangan")
        print("=" * 50)
        
    def main_menu(self):
        """Display main menu and handle user choice"""
        while True:
            print("\n=== MENU UTAMA ===")
            print("1. Login dengan Face Detection")
            print("2. Hand Gesture Control (Harus login dulu)")
            print("3. Keluar")
            
            try:
                choice = input("Pilih menu (1-3): ").strip()
                
                if choice == "1":
                    self.login_process()
                elif choice == "2":
                    if self.is_logged_in:
                        self.gesture_control_process()
                    else:
                        print("❌ Anda harus login terlebih dahulu!")
                        input("Tekan Enter untuk melanjutkan...")
                elif choice == "3":
                    print("Terima kasih telah menggunakan aplikasi!")
                    break
                else:
                    print("Pilihan tidak valid. Silakan pilih 1-3.")
                    input("Tekan Enter untuk melanjutkan...")
                    
            except KeyboardInterrupt:
                print("\nAplikasi dihentikan.")
                break
            except Exception as e:
                print(f"Error: {e}")
                input("Tekan Enter untuk melanjutkan...")
    
    def login_process(self):
        """Handle face detection login process"""
        print("\n=== PROSES LOGIN ===")
        print("Memulai sistem face detection login...")
        print("Pastikan wajah Anda terlihat jelas di kamera.")
        input("Tekan Enter untuk memulai login...")
        
        try:
            login_success = self.face_detector.login_system()
            
            if login_success:
                self.is_logged_in = True
                print("✅ LOGIN BERHASIL!")
                print("Sekarang Anda dapat menggunakan fitur Hand Gesture Control.")
            else:
                print("❌ Login gagal atau dibatalkan.")
                
        except Exception as e:
            print(f"Error saat login: {e}")
        
        input("Tekan Enter untuk kembali ke menu...")
    
    def gesture_control_process(self):
        """Handle hand gesture control process"""
        print("\n=== HAND GESTURE CONTROL ===")
        print("Memulai sistem kontrol gesture tangan...")
        print("Gerakkan tangan Anda untuk melihat deteksi arah:")
        print("- ATAS: Gerakkan tangan ke atas layar")
        print("- BAWAH: Gerakkan tangan ke bawah layar") 
        print("- KIRI: Gerakkan tangan ke kiri layar")
        print("- KANAN: Gerakkan tangan ke kanan layar")
        input("Tekan Enter untuk memulai...")
        
        try:
            self.hand_tracker.gesture_control_system()
        except Exception as e:
            print(f"Error saat gesture control: {e}")
        
        input("Tekan Enter untuk kembali ke menu...")
    
    def run(self):
        """Run the main application"""
        try:
            self.welcome_screen()
            self.main_menu()
        except KeyboardInterrupt:
            print("\nAplikasi dihentikan oleh user.")
        except Exception as e:
            print(f"Error tidak terduga: {e}")

# Main entry point
if __name__ == "__main__":
    app = MediaPipeApp()
    app.run()