#!/usr/bin/env python3
"""
MediaPipe Face Detection & Hand Tracking GUI Application

This is the main entry point for the GUI version of the application.
Run this script to start the application with a user-friendly interface.
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    from gui.main_window import MainWindow
except ImportError as e:
    # Fallback error handling
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(
        "Import Error",
        f"Gagal mengimpor modul GUI:\n{str(e)}\n\nPastikan semua dependencies telah terinstall:\n• mediapipe\n• opencv-python\n• pillow\n• numpy"
    )
    sys.exit(1)

def check_dependencies():
    """Check if all required dependencies are installed"""
    missing_deps = []
    
    try:
        import cv2
    except ImportError:
        missing_deps.append("opencv-python")
    
    try:
        import mediapipe
    except ImportError:
        missing_deps.append("mediapipe")
    
    try:
        import PIL
    except ImportError:
        missing_deps.append("pillow")
    
    try:
        import numpy
    except ImportError:
        missing_deps.append("numpy")
    
    return missing_deps

def main():
    """Main application entry point"""
    print("🚀 Starting MediaPipe GUI Application...")
    
    # Check dependencies
    missing_deps = check_dependencies()
    if missing_deps:
        root = tk.Tk()
        root.withdraw()
        
        deps_text = "\n• ".join(missing_deps)
        error_msg = f"""Beberapa dependencies belum terinstall:

• {deps_text}

Silakan install dependencies dengan perintah:
pip install {' '.join(missing_deps)}

Atau gunakan:
pip install -r requirements.txt"""
        
        messagebox.showerror("Dependencies Missing", error_msg)
        print(f"❌ Missing dependencies: {', '.join(missing_deps)}")
        return 1
    
    try:
        # Create and run GUI application
        print("✅ All dependencies found")
        print("🎨 Launching GUI interface...")
        
        app = MainWindow()
        app.run()
        
        print("👋 Application closed successfully")
        return 0
        
    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        
        error_msg = f"""Terjadi error saat menjalankan aplikasi:

{str(e)}

Tips troubleshooting:
1. Pastikan kamera tidak digunakan aplikasi lain
2. Restart aplikasi
3. Periksa permission kamera
4. Reinstall dependencies jika perlu"""
        
        messagebox.showerror("Application Error", error_msg)
        print(f"❌ Application error: {str(e)}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)