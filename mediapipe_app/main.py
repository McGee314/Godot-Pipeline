import cv2
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.hand_tracking import HandTracker

class MediaPipeApp:
    def __init__(self):
        """Initialize MediaPipe Application"""
        self.hand_tracker = HandTracker()
        
    def run(self):
        """Run the main application - directly start hand gesture control"""
        try:
            print("=" * 50)
            print("   HAND GESTURE CONTROL")
            print("=" * 50)
            print("🎥 Membuka kamera...")
            print("✋ Gerakkan tangan Anda untuk melihat deteksi arah:")
            print("   - ATAS: Gerakkan tangan ke atas layar")
            print("   - BAWAH: Gerakkan tangan ke bawah layar")
            print("   - KIRI: Gerakkan tangan ke kiri layar")
            print("   - KANAN: Gerakkan tangan ke kanan layar")
            print("Tekan 'q' untuk keluar")
            print("=" * 50)
            print()
            
            # Langsung jalankan gesture control
            self.hand_tracker.gesture_control_system()
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Aplikasi dihentikan oleh user.")
        except Exception as e:
            print(f"❌ Error tidak terduga: {e}")

# Main entry point
if __name__ == "__main__":
    app = MediaPipeApp()
    app.run()