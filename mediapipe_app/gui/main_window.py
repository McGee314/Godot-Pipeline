import tkinter as tk
from tkinter import ttk, messagebox
import threading
import cv2
from PIL import Image, ImageTk
import sys
import os

class MainWindow:
    def __init__(self):
        """Initialize main window application"""
        self.root = tk.Tk()
        self.root.title("MediaPipe Face & Hand Tracking App")
        self.root.geometry("600x500")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(False, False)
        
        # Center window on screen
        self.center_window()
        
        # Application state
        self.is_logged_in = False
        
        # Create main interface
        self.create_main_interface()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_main_interface(self):
        """Create the main application interface"""
        # Header frame
        header_frame = tk.Frame(self.root, bg='#34495e', height=100)
        header_frame.pack(fill='x', padx=20, pady=20)
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="🎯 MediaPipe App",
            font=('Arial', 24, 'bold'),
            bg='#34495e',
            fg='#ecf0f1'
        )
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Face Detection & Hand Tracking Application",
            font=('Arial', 12),
            bg='#34495e',
            fg='#bdc3c7'
        )
        subtitle_label.pack()
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg='#2c3e50')
        content_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Status frame
        status_frame = tk.Frame(content_frame, bg='#34495e', height=60)
        status_frame.pack(fill='x', pady=(0, 20))
        status_frame.pack_propagate(False)
        
        # Status indicator
        self.status_label = tk.Label(
            status_frame,
            text="🔴 Belum Login",
            font=('Arial', 14, 'bold'),
            bg='#34495e',
            fg='#e74c3c'
        )
        self.status_label.pack(pady=15)
        
        # Buttons frame
        buttons_frame = tk.Frame(content_frame, bg='#2c3e50')
        buttons_frame.pack(fill='both', expand=True)
        
        # Login button
        self.login_btn = tk.Button(
            buttons_frame,
            text="🔐 Login dengan Face Detection",
            font=('Arial', 14, 'bold'),
            bg='#3498db',
            fg='white',
            activebackground='#2980b9',
            activeforeground='white',
            relief='flat',
            height=3,
            cursor='hand2',
            command=self.open_face_login
        )
        self.login_btn.pack(fill='x', pady=10)
        
        # Hand gesture button
        self.gesture_btn = tk.Button(
            buttons_frame,
            text="👋 Hand Gesture Control",
            font=('Arial', 14, 'bold'),
            bg='#95a5a6',
            fg='white',
            activebackground='#7f8c8d',
            activeforeground='white',
            relief='flat',
            height=3,
            cursor='hand2',
            command=self.open_hand_gesture,
            state='disabled'
        )
        self.gesture_btn.pack(fill='x', pady=10)
        
        # Info frame
        info_frame = tk.Frame(content_frame, bg='#34495e', height=80)
        info_frame.pack(fill='x', pady=20)
        info_frame.pack_propagate(False)
        
        info_text = """💡 Cara Penggunaan:
1. Klik "Login dengan Face Detection" untuk masuk
2. Setelah login berhasil, gunakan "Hand Gesture Control" """
        
        info_label = tk.Label(
            info_frame,
            text=info_text,
            font=('Arial', 10),
            bg='#34495e',
            fg='#bdc3c7',
            justify='left'
        )
        info_label.pack(pady=10, padx=20)
        
        # Footer
        footer_frame = tk.Frame(self.root, bg='#2c3e50', height=50)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)
        
        # Exit button
        exit_btn = tk.Button(
            footer_frame,
            text="❌ Keluar",
            font=('Arial', 12),
            bg='#e74c3c',
            fg='white',
            activebackground='#c0392b',
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            command=self.exit_app
        )
        exit_btn.pack(side='right', padx=20, pady=10)
        
        # About button
        about_btn = tk.Button(
            footer_frame,
            text="ℹ️ Tentang",
            font=('Arial', 12),
            bg='#34495e',
            fg='white',
            activebackground='#2c3e50',
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            command=self.show_about
        )
        about_btn.pack(side='left', padx=20, pady=10)
    
    def update_login_status(self, logged_in=True):
        """Update login status and enable/disable buttons"""
        self.is_logged_in = logged_in
        if logged_in:
            self.status_label.config(
                text="🟢 Login Berhasil",
                fg='#27ae60'
            )
            self.gesture_btn.config(
                state='normal',
                bg='#27ae60',
                activebackground='#229954'
            )
            self.login_btn.config(text="✅ Sudah Login")
        else:
            self.status_label.config(
                text="🔴 Belum Login",
                fg='#e74c3c'
            )
            self.gesture_btn.config(
                state='disabled',
                bg='#95a5a6'
            )
            self.login_btn.config(text="🔐 Login dengan Face Detection")
    
    def open_face_login(self):
        """Open face detection login window"""
        if not self.is_logged_in:
            from .face_login_window import FaceLoginWindow
            login_window = FaceLoginWindow(self)
        else:
            messagebox.showinfo("Info", "Anda sudah login!")
    
    def open_hand_gesture(self):
        """Open hand gesture control window"""
        if self.is_logged_in:
            from .hand_gesture_window import HandGestureWindow
            gesture_window = HandGestureWindow(self)
        else:
            messagebox.showwarning("Peringatan", "Silakan login terlebih dahulu!")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """MediaPipe Face & Hand Tracking App
        
Versi: 1.0.0
Dibuat dengan: Python, MediaPipe, OpenCV, Tkinter

Fitur:
• Face Detection untuk Login
• Hand Gesture Control
• User Interface yang mudah digunakan

Dependencies:
• mediapipe==0.10.21
• opencv-python==4.8.1.78
• numpy==1.24.3
• PIL (Pillow)

© 2024 MediaPipe App Developer"""
        
        messagebox.showinfo("Tentang Aplikasi", about_text)
    
    def exit_app(self):
        """Exit application with confirmation"""
        result = messagebox.askyesno(
            "Konfirmasi Keluar", 
            "Apakah Anda yakin ingin keluar dari aplikasi?"
        )
        if result:
            self.root.quit()
            self.root.destroy()
    
    def run(self):
        """Run the main application"""
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)
        
        # Start the main loop
        self.root.mainloop()

if __name__ == "__main__":
    app = MainWindow()
    app.run()