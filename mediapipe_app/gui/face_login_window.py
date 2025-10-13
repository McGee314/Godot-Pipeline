import tkinter as tk
from tkinter import ttk, messagebox
import cv2
import threading
import time
from PIL import Image, ImageTk
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))
from face_detection import FaceDetector

class FaceLoginWindow:
    def __init__(self, parent_app):
        """Initialize face login window"""
        self.parent_app = parent_app
        self.face_detector = FaceDetector()
        
        # Create window
        self.window = tk.Toplevel(self.parent_app.root)
        self.window.title("Face Detection Login")
        self.window.geometry("800x700")
        self.window.configure(bg='#2c3e50')
        self.window.resizable(False, False)
        
        # Center window
        self.center_window()
        
        # Camera variables
        self.cap = None
        self.is_running = False
        self.face_detected_time = 0
        self.required_detection_time = 60  # 2 seconds at 30 FPS
        
        # Create interface
        self.create_interface()
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_interface(self):
        """Create the login interface"""
        # Header
        header_frame = tk.Frame(self.window, bg='#34495e', height=80)
        header_frame.pack(fill='x', padx=20, pady=20)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🔐 Face Detection Login",
            font=('Arial', 20, 'bold'),
            bg='#34495e',
            fg='#ecf0f1'
        )
        title_label.pack(pady=20)
        
        # Status frame
        status_frame = tk.Frame(self.window, bg='#2c3e50', height=60)
        status_frame.pack(fill='x', padx=20)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="📷 Tekan tombol 'Mulai Login' untuk memulai",
            font=('Arial', 12),
            bg='#2c3e50',
            fg='#f39c12'
        )
        self.status_label.pack(pady=15)
        
        # Camera frame
        camera_frame = tk.Frame(self.window, bg='#34495e', width=640, height=480)
        camera_frame.pack(padx=20, pady=10)
        camera_frame.pack_propagate(False)
        
        # Camera label
        self.camera_label = tk.Label(
            camera_frame,
            text="🎥 Kamera akan ditampilkan di sini",
            font=('Arial', 16),
            bg='#34495e',
            fg='#bdc3c7',
            width=80,
            height=30
        )
        self.camera_label.pack(fill='both', expand=True)
        
        # Progress frame
        progress_frame = tk.Frame(self.window, bg='#2c3e50', height=50)
        progress_frame.pack(fill='x', padx=20, pady=10)
        progress_frame.pack_propagate(False)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            length=500
        )
        self.progress_bar.pack(pady=15)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.window, bg='#2c3e50')
        buttons_frame.pack(fill='x', padx=20, pady=20)
        
        # Start button
        self.start_btn = tk.Button(
            buttons_frame,
            text="📹 Mulai Login",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            activebackground='#229954',
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            command=self.start_login
        )
        self.start_btn.pack(side='left', padx=(0, 10))
        
        # Stop button
        self.stop_btn = tk.Button(
            buttons_frame,
            text="⏹️ Berhenti",
            font=('Arial', 12, 'bold'),
            bg='#e74c3c',
            fg='white',
            activebackground='#c0392b',
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            command=self.stop_login,
            state='disabled'
        )
        self.stop_btn.pack(side='left', padx=(0, 10))
        
        # Close button
        close_btn = tk.Button(
            buttons_frame,
            text="❌ Tutup",
            font=('Arial', 12, 'bold'),
            bg='#95a5a6',
            fg='white',
            activebackground='#7f8c8d',
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            command=self.on_closing
        )
        close_btn.pack(side='right')
        
        # Instructions
        instructions_text = """📝 Instruksi Login:
1. Klik tombol 'Mulai Login' untuk mengaktifkan kamera
2. Posisikan wajah Anda di tengah layar
3. Pastikan pencahayaan cukup dan wajah terlihat jelas
4. Tunggu hingga deteksi wajah mencapai 100%
5. Login berhasil jika progress bar penuh"""
        
        instructions_label = tk.Label(
            self.window,
            text=instructions_text,
            font=('Arial', 10),
            bg='#2c3e50',
            fg='#bdc3c7',
            justify='left'
        )
        instructions_label.pack(padx=20, pady=(0, 20))
    
    def start_login(self):
        """Start face detection login process"""
        try:
            # Try multiple camera indices
            camera_indices = [0, 1, -1]  # Try default, secondary, and any available
            self.cap = None
            
            for index in camera_indices:
                print(f"Trying camera index {index}...")
                test_cap = cv2.VideoCapture(index)
                if test_cap.isOpened():
                    # Test if we can actually read a frame
                    ret, frame = test_cap.read()
                    if ret:
                        self.cap = test_cap
                        print(f"✅ Camera {index} working!")
                        break
                    else:
                        test_cap.release()
                else:
                    test_cap.release()
            
            if self.cap is None or not self.cap.isOpened():
                error_msg = """Tidak dapat mengakses kamera!

Kemungkinan penyebab:
• Kamera sedang digunakan aplikasi lain
• Driver kamera bermasalah  
• Permission kamera ditolak
• Kamera tidak terpasang

Solusi:
1. Tutup aplikasi lain yang menggunakan kamera
2. Restart aplikasi
3. Periksa pengaturan privacy kamera di System Preferences"""
                messagebox.showerror("Error Kamera", error_msg)
                return
            
            # Test camera frame capture
            ret, test_frame = self.cap.read()
            if not ret:
                self.cap.release()
                messagebox.showerror("Error", "Kamera dapat dibuka tapi tidak dapat membaca frame!")
                return
            
            self.is_running = True
            self.face_detected_time = 0
            
            # Update UI
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.status_label.config(
                text="📷 Kamera aktif - Posisikan wajah Anda",
                fg='#3498db'
            )
            
            # Start camera thread
            self.camera_thread = threading.Thread(target=self.camera_loop)
            self.camera_thread.daemon = True
            self.camera_thread.start()
            
        except Exception as e:
            error_msg = f"""Gagal memulai login: {str(e)}

Tips troubleshooting:
1. Restart aplikasi
2. Periksa permission kamera
3. Tutup aplikasi lain yang menggunakan kamera
4. Coba kembali dalam beberapa detik"""
            messagebox.showerror("Error", error_msg)
            print(f"Camera error: {e}")
    
    def stop_login(self):
        """Stop face detection login process"""
        self.is_running = False
        
        # Wait for camera thread to finish
        if hasattr(self, 'camera_thread') and self.camera_thread.is_alive():
            try:
                self.camera_thread.join(timeout=1.0)
            except:
                pass
        
        # Release camera
        if self.cap:
            try:
                self.cap.release()
                self.cap = None
            except Exception as e:
                print(f"Error releasing camera: {e}")
            
        # Reset UI
        if hasattr(self, 'start_btn'):
            self.start_btn.config(state='normal')
        if hasattr(self, 'stop_btn'):
            self.stop_btn.config(state='disabled')
        if hasattr(self, 'status_label'):
            self.status_label.config(
                text="📷 Login dihentikan",
                fg='#e74c3c'
            )
        if hasattr(self, 'progress_var'):
            self.progress_var.set(0)
        if hasattr(self, 'camera_label'):
            self.camera_label.config(
                image='',
                text="🎥 Kamera tidak aktif"
            )
    
    def camera_loop(self):
        """Main camera processing loop"""
        frame_count = 0
        consecutive_failures = 0
        max_failures = 10
        
        try:
            while self.is_running and self.cap and self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    consecutive_failures += 1
                    print(f"Failed to read frame {consecutive_failures}/{max_failures}")
                    
                    if consecutive_failures >= max_failures:
                        print("Too many consecutive frame read failures")
                        self.window.after(0, self.camera_error_callback, "Kehilangan koneksi kamera")
                        break
                    
                    time.sleep(0.1)  # Wait a bit before retrying
                    continue
                
                consecutive_failures = 0  # Reset failure counter
                frame_count += 1
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Detect face
                try:
                    has_face, processed_frame = self.face_detector.detect_face(frame)
                except Exception as e:
                    print(f"Face detection error: {e}")
                    # Continue with original frame if face detection fails
                    has_face = False
                    processed_frame = frame
                
                # Update login progress
                if has_face:
                    self.face_detected_time += 1
                    progress = (self.face_detected_time / self.required_detection_time) * 100
                    
                    # Update UI in main thread
                    self.window.after(0, self.update_progress, progress, "🟢 Wajah terdeteksi!")
                    
                    # Check if login successful
                    if self.face_detected_time >= self.required_detection_time:
                        self.window.after(0, self.login_successful)
                        break
                else:
                    self.face_detected_time = max(0, self.face_detected_time - 2)  # Decrease slower
                    progress = (self.face_detected_time / self.required_detection_time) * 100
                    self.window.after(0, self.update_progress, progress, "🔴 Wajah tidak terdeteksi")
                
                # Convert frame for tkinter
                try:
                    frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                    frame_resized = cv2.resize(frame_rgb, (640, 480))
                    image = Image.fromarray(frame_resized)
                    photo = ImageTk.PhotoImage(image=image)
                    
                    # Update camera display in main thread
                    self.window.after(0, self.update_camera_display, photo)
                except Exception as e:
                    print(f"Frame processing error: {e}")
                    # Continue without updating display if frame processing fails
                
                time.sleep(0.033)  # ~30 FPS
                
        except Exception as e:
            print(f"Camera loop error: {e}")
            self.window.after(0, self.camera_error_callback, f"Error kamera: {str(e)}")
        
        finally:
            # Cleanup
            if self.cap:
                try:
                    self.cap.release()
                except:
                    pass
    
    def update_camera_display(self, photo):
        """Update camera display in main thread"""
        if self.camera_label.winfo_exists():
            self.camera_label.config(image=photo, text='')
            self.camera_label.image = photo  # Keep reference
    
    def update_progress(self, progress, status_text):
        """Update progress bar and status in main thread"""
        if self.window.winfo_exists():
            self.progress_var.set(min(progress, 100))
            self.status_label.config(text=status_text)
    
    def camera_error_callback(self, error_message):
        """Handle camera errors in main thread"""
        self.stop_login()
        self.status_label.config(
            text="❌ Error kamera",
            fg='#e74c3c'
        )
        messagebox.showerror("Error Kamera", f"{error_message}\n\nSilakan coba lagi atau restart aplikasi.")

    def login_successful(self):
        """Handle successful login"""
        self.stop_login()
        
        # Show success message
        self.status_label.config(
            text="✅ LOGIN BERHASIL!",
            fg='#27ae60'
        )
        self.progress_var.set(100)
        
        # Update parent app status
        self.parent_app.update_login_status(True)
        
        # Show success dialog
        messagebox.showinfo("Login Berhasil!", "Face detection login berhasil!\n\nAnda sekarang dapat menggunakan fitur Hand Gesture Control.")
        
        # Close window after 2 seconds
        self.window.after(2000, self.on_closing)
    
    def on_closing(self):
        """Handle window closing"""
        self.stop_login()
        if hasattr(self, 'window') and self.window.winfo_exists():
            self.window.destroy()

if __name__ == "__main__":
    # Test window independently
    root = tk.Tk()
    root.withdraw()  # Hide root window
    
    class MockParent:
        def __init__(self):
            self.root = root
        def update_login_status(self, status):
            print(f"Login status: {status}")
    
    app = FaceLoginWindow(MockParent())
    root.mainloop()