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
from hand_tracking import HandTracker

class HandGestureWindow:
    def __init__(self, parent_app):
        """Initialize hand gesture window"""
        self.parent_app = parent_app
        self.hand_tracker = HandTracker()
        
        # Create window
        self.window = tk.Toplevel(self.parent_app.root)
        self.window.title("Hand Gesture Control")
        self.window.geometry("900x750")
        self.window.configure(bg='#2c3e50')
        self.window.resizable(False, False)
        
        # Center window
        self.center_window()
        
        # Camera variables
        self.cap = None
        self.is_running = False
        self.current_gesture = "NO_HAND"
        self.gesture_history = []
        
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
        """Create the hand gesture interface"""
        # Header
        header_frame = tk.Frame(self.window, bg='#34495e', height=80)
        header_frame.pack(fill='x', padx=20, pady=20)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="👋 Hand Gesture Control",
            font=('Arial', 20, 'bold'),
            bg='#34495e',
            fg='#ecf0f1'
        )
        title_label.pack(pady=20)
        
        # Main content frame
        content_frame = tk.Frame(self.window, bg='#2c3e50')
        content_frame.pack(fill='both', expand=True, padx=20)
        
        # Left panel (Camera + Controls)
        left_panel = tk.Frame(content_frame, bg='#2c3e50')
        left_panel.pack(side='left', fill='both', expand=True)
        
        # Camera frame
        camera_frame = tk.Frame(left_panel, bg='#34495e', width=640, height=480)
        camera_frame.pack(pady=10)
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
        
        # Controls frame
        controls_frame = tk.Frame(left_panel, bg='#2c3e50')
        controls_frame.pack(fill='x', pady=10)
        
        # Start button
        self.start_btn = tk.Button(
            controls_frame,
            text="▶️ Mulai Tracking",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            activebackground='#229954',
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            command=self.start_tracking
        )
        self.start_btn.pack(side='left', padx=(0, 10))
        
        # Stop button
        self.stop_btn = tk.Button(
            controls_frame,
            text="⏹️ Berhenti",
            font=('Arial', 12, 'bold'),
            bg='#e74c3c',
            fg='white',
            activebackground='#c0392b',
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            command=self.stop_tracking,
            state='disabled'
        )
        self.stop_btn.pack(side='left', padx=(0, 10))
        
        # Close button
        close_btn = tk.Button(
            controls_frame,
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
        
        # Right panel (Gesture Info)
        right_panel = tk.Frame(content_frame, bg='#34495e', width=220)
        right_panel.pack(side='right', fill='y', padx=(20, 0))
        right_panel.pack_propagate(False)
        
        # Current gesture frame
        gesture_frame = tk.Frame(right_panel, bg='#34495e')
        gesture_frame.pack(fill='x', padx=10, pady=10)
        
        gesture_title = tk.Label(
            gesture_frame,
            text="🎯 Gesture Saat Ini",
            font=('Arial', 14, 'bold'),
            bg='#34495e',
            fg='#ecf0f1'
        )
        gesture_title.pack(pady=(0, 10))
        
        self.gesture_label = tk.Label(
            gesture_frame,
            text="NO_HAND",
            font=('Arial', 18, 'bold'),
            bg='#2c3e50',
            fg='#f39c12',
            relief='raised',
            pady=10
        )
        self.gesture_label.pack(fill='x')
        
        # Gesture indicators
        indicators_frame = tk.Frame(right_panel, bg='#34495e')
        indicators_frame.pack(fill='x', padx=10, pady=10)
        
        indicators_title = tk.Label(
            indicators_frame,
            text="📍 Arah Gerakan",
            font=('Arial', 14, 'bold'),
            bg='#34495e',
            fg='#ecf0f1'
        )
        indicators_title.pack(pady=(0, 10))
        
        # Direction indicators
        self.direction_indicators = {}
        directions = [
            ("UP", "⬆️", "#3498db"),
            ("DOWN", "⬇️", "#e74c3c"),
            ("LEFT", "⬅️", "#f39c12"),
            ("RIGHT", "➡️", "#27ae60")
        ]
        
        for direction, emoji, color in directions:
            indicator_frame = tk.Frame(indicators_frame, bg='#34495e')
            indicator_frame.pack(fill='x', pady=2)
            
            indicator = tk.Label(
                indicator_frame,
                text=f"{emoji} {direction}",
                font=('Arial', 12),
                bg='#2c3e50',
                fg='#7f8c8d',
                relief='raised',
                pady=5
            )
            indicator.pack(fill='x')
            self.direction_indicators[direction] = (indicator, color)
        
        # Statistics frame
        stats_frame = tk.Frame(right_panel, bg='#34495e')
        stats_frame.pack(fill='x', padx=10, pady=10)
        
        stats_title = tk.Label(
            stats_frame,
            text="📊 Statistik",
            font=('Arial', 14, 'bold'),
            bg='#34495e',
            fg='#ecf0f1'
        )
        stats_title.pack(pady=(0, 10))
        
        self.stats_label = tk.Label(
            stats_frame,
            text="Gesture Count: 0",
            font=('Arial', 10),
            bg='#2c3e50',
            fg='#bdc3c7',
            justify='left',
            pady=10
        )
        self.stats_label.pack(fill='x')
        
        # Instructions frame
        instructions_frame = tk.Frame(right_panel, bg='#34495e')
        instructions_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        instructions_title = tk.Label(
            instructions_frame,
            text="📝 Instruksi",
            font=('Arial', 14, 'bold'),
            bg='#34495e',
            fg='#ecf0f1'
        )
        instructions_title.pack(pady=(0, 10))
        
        instructions_text = """🖐️ Cara Penggunaan:

1. Klik 'Mulai Tracking'
2. Posisikan tangan di depan kamera
3. Gerakkan tangan ke arah:
   • ATAS untuk UP
   • BAWAH untuk DOWN
   • KIRI untuk LEFT
   • KANAN untuk RIGHT

💡 Tips:
• Gunakan pencahayaan cukup
• Jarak 30-60 cm dari kamera
• Gerakkan tangan perlahan"""
        
        instructions_label = tk.Label(
            instructions_frame,
            text=instructions_text,
            font=('Arial', 9),
            bg='#34495e',
            fg='#bdc3c7',
            justify='left',
            anchor='n'
        )
        instructions_label.pack(fill='both', expand=True)
    
    def start_tracking(self):
        """Start hand gesture tracking"""
        try:
            # Try multiple camera indices
            camera_indices = [0, 1, -1]
            self.cap = None
            
            for index in camera_indices:
                print(f"Trying camera index {index}...")
                test_cap = cv2.VideoCapture(index)
                if test_cap.isOpened():
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

Solusi:
1. Tutup aplikasi lain yang menggunakan kamera
2. Restart aplikasi
3. Periksa pengaturan privacy kamera"""
                messagebox.showerror("Error Kamera", error_msg)
                return
            
            self.is_running = True
            self.gesture_history = []
            
            # Update UI
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            
            # Start camera thread
            self.camera_thread = threading.Thread(target=self.camera_loop)
            self.camera_thread.daemon = True
            self.camera_thread.start()
            
        except Exception as e:
            error_msg = f"""Gagal memulai tracking: {str(e)}

Tips troubleshooting:
1. Restart aplikasi
2. Periksa permission kamera
3. Tutup aplikasi lain yang menggunakan kamera"""
            messagebox.showerror("Error", error_msg)
            print(f"Camera error: {e}")
    
    def camera_error_callback(self, error_message):
        """Handle camera errors in main thread"""
        self.stop_tracking()
        messagebox.showerror("Error Kamera", f"{error_message}\n\nSilakan coba lagi atau restart aplikasi.")
    
    def stop_tracking(self):
        """Stop hand gesture tracking"""
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
        if hasattr(self, 'camera_label'):
            self.camera_label.config(
                image='',
                text="🎥 Tracking dihentikan"
            )
        self.update_gesture_display("NO_HAND")
    
    def camera_loop(self):
        """Main camera processing loop"""
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
                    
                    time.sleep(0.1)
                    continue
                
                consecutive_failures = 0
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                frame_height, frame_width = frame.shape[:2]
                
                # Detect hands and get gesture
                try:
                    landmarks, processed_frame = self.hand_tracker.detect_hands(frame)
                    direction = self.hand_tracker.get_gesture_direction(landmarks, frame_width, frame_height)
                except Exception as e:
                    print(f"Hand tracking error: {e}")
                    # Continue with original frame if hand tracking fails
                    direction = "NO_HAND"
                    processed_frame = frame
                
                # Update gesture in main thread
                if direction != self.current_gesture:
                    self.current_gesture = direction
                    self.gesture_history.append(direction)
                    # Send gesture to Godot
                    try:
                        self.hand_tracker.send_gesture_to_godot(direction)
                    except Exception as e:
                        print(f"Warning: failed to send gesture to Godot: {e}")
                    self.window.after(0, self.update_gesture_display, direction)
                
                # Draw direction on frame
                if direction != "NO_HAND":
                    color = (0, 255, 0) if direction != "CENTER" else (255, 255, 0)
                    cv2.putText(processed_frame, f"ARAH: {direction}", 
                               (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                else:
                    cv2.putText(processed_frame, "Tidak ada tangan terdeteksi", 
                               (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                # Draw reference lines
                cv2.line(processed_frame, (frame_width//2, 0), 
                        (frame_width//2, frame_height), (255, 255, 255), 1)
                cv2.line(processed_frame, (0, frame_height//2), 
                        (frame_width, frame_height//2), (255, 255, 255), 1)
                
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
    
    def update_gesture_display(self, gesture):
        """Update gesture display and indicators"""
        if not self.window.winfo_exists():
            return
            
        # Update main gesture label
        colors = {
            "UP": "#3498db",
            "DOWN": "#e74c3c", 
            "LEFT": "#f39c12",
            "RIGHT": "#27ae60",
            "CENTER": "#9b59b6",
            "NO_HAND": "#7f8c8d"
        }
        
        self.gesture_label.config(
            text=gesture,
            fg=colors.get(gesture, "#7f8c8d")
        )
        
        # Update direction indicators
        for direction, (indicator, color) in self.direction_indicators.items():
            if direction == gesture:
                indicator.config(bg=color, fg='white')
            else:
                indicator.config(bg='#2c3e50', fg='#7f8c8d')
        
        # Update statistics
        gesture_count = len([g for g in self.gesture_history if g != "NO_HAND"])
        up_count = self.gesture_history.count("UP")
        down_count = self.gesture_history.count("DOWN")
        left_count = self.gesture_history.count("LEFT")
        right_count = self.gesture_history.count("RIGHT")
        
        stats_text = f"""Total Gestures: {gesture_count}
UP: {up_count}
DOWN: {down_count}
LEFT: {left_count}
RIGHT: {right_count}"""
        
        self.stats_label.config(text=stats_text)
        
        # Print to console for debugging
        if gesture != "NO_HAND":
            print(f"Gesture detected: {gesture}")
    
    def on_closing(self):
        """Handle window closing"""
        self.stop_tracking()
        if hasattr(self, 'window') and self.window.winfo_exists():
            self.window.destroy()

if __name__ == "__main__":
    # Test window independently
    root = tk.Tk()
    root.withdraw()  # Hide root window
    
    class MockParent:
        def __init__(self):
            self.root = root
    
    app = HandGestureWindow(MockParent())
    root.mainloop()