# MediaPipe Face Detection & Hand Tracking Application

Aplikasi Python sederhana menggunakan MediaPipe untuk Face Detection dan Hand Tracking.

## Fitur

1. **Face Detection Login** - Login menggunakan deteksi wajah
2. **Hand Gesture Control** - Kontrol gesture menggunakan tracking tangan (UP, DOWN, LEFT, RIGHT)

## Struktur Project

```
Pipeline/
├── mediapipe_env/           # Virtual environment
├── mediapipe_app/           # Folder aplikasi utama
│   ├── src/                 # Core functionality
│   │   ├── __init__.py
│   │   ├── face_detection.py    # Face detection engine
│   │   └── hand_tracking.py     # Hand tracking engine
│   ├── gui/                 # GUI components
│   │   ├── __init__.py
│   │   ├── main_window.py       # Main GUI window
│   │   ├── face_login_window.py # Face detection GUI
│   │   └── hand_gesture_window.py # Hand tracking GUI
│   ├── utils/               # Utility functions
│   ├── main.py              # Terminal version
│   ├── gui_app.py           # GUI version entry point
│   ├── requirements.txt     # Dependencies
│   └── README.md            # Documentation
├── run_gui.sh              # GUI launcher (macOS/Linux)
├── run_gui.bat             # GUI launcher (Windows)
└── run_app.sh              # Terminal launcher
```

## Cara Setup dan Menjalankan

### 1. Persiapan Virtual Environment

```bash
# Buat virtual environment
python3 -m venv mediapipe_env

# Aktivasi virtual environment (macOS/Linux)
source mediapipe_env/bin/activate

# Aktivasi virtual environment (Windows)
mediapipe_env\Scripts\activate
```

### 2. Install Dependencies

```bash
# Install dari requirements.txt
pip install -r mediapipe_app/requirements.txt

# Atau install manual satu per satu
pip install mediapipe==0.10.21
pip install opencv-python==4.8.1.78
pip install numpy==1.24.3
pip install pillow
```

### 3. Jalankan Aplikasi

#### GUI Version (Direkomendasikan) 🎨
```bash
# Jalankan menggunakan script otomatis
./run_gui.sh          # macOS/Linux
# atau
run_gui.bat           # Windows

# Atau jalankan manual
cd mediapipe_app
python gui_app.py
```

#### Terminal Version 💻
```bash
# Masuk ke folder aplikasi
cd mediapipe_app

# Jalankan aplikasi terminal
python main.py
```

## Cara Menggunakan

### GUI Version (User-Friendly) 🎨

#### 1. Aplikasi Utama
- Aplikasi akan membuka dengan window GUI yang menarik
- Anda akan melihat status login dan tombol-tombol utama
- Interface sudah sangat intuitif dan mudah dipahami

#### 2. Face Detection Login
1. Klik tombol "🔐 Login dengan Face Detection"
2. Window kamera akan terbuka dengan preview real-time
3. Posisikan wajah di tengah layar
4. Progress bar akan menunjukkan tingkat deteksi
5. Login berhasil ketika progress bar mencapai 100%
6. Window akan menutup otomatis setelah login berhasil

#### 3. Hand Gesture Control  
1. Setelah login berhasil, klik "👋 Hand Gesture Control"
2. Window tracking akan terbuka dengan panel kontrol
3. Klik "▶️ Mulai Tracking" untuk mengaktifkan kamera
4. Gerakkan tangan untuk melihat deteksi real-time:
   - **ATAS** - untuk arah UP (biru)
   - **BAWAH** - untuk arah DOWN (merah)  
   - **KIRI** - untuk arah LEFT (kuning)
   - **KANAN** - untuk arah RIGHT (hijau)
5. Panel kanan menunjukkan statistik dan indikator arah
6. Klik "⏹️ Berhenti" untuk menghentikan tracking

### Terminal Version (Advanced) 💻

#### 1. Menu Utama
Setelah aplikasi dijalankan, Anda akan melihat menu:
- **1. Login dengan Face Detection** - Untuk login menggunakan wajah
- **2. Hand Gesture Control** - Untuk kontrol gesture (harus login dulu)
- **3. Keluar** - Untuk keluar dari aplikasi

#### 2. Face Detection Login
1. Pilih menu "1" untuk login
2. Posisikan wajah di depan kamera
3. Pastikan pencahayaan cukup dan wajah terlihat jelas
4. Sistem akan mendeteksi wajah selama 2 detik
5. Jika berhasil, akan muncul "LOGIN SUCCESS!"
6. Tekan 'q' untuk keluar dari mode kamera

#### 3. Hand Gesture Control
1. Setelah login berhasil, pilih menu "2"
2. Posisikan tangan di depan kamera
3. Gerakkan tangan ke arah yang diinginkan
4. Arah akan ditampilkan di layar dan terminal
5. Tekan 'q' untuk keluar dari mode gesture

## Troubleshooting

### 🔧 Test Kamera dan Dependencies
```bash
# Jalankan test diagnostik
python ../test_camera.py

# Atau test manual
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK:', cap.isOpened()); cap.release()"
```

### Error: Tidak dapat mengakses kamera
**Penyebab umum:**
- Kamera sedang digunakan aplikasi lain (Zoom, Teams, browser, dll)
- Permission kamera ditolak sistem operasi
- Driver kamera bermasalah

**Solusi:**
1. **Tutup aplikasi lain** yang menggunakan kamera
2. **Check permission:**
   - **macOS**: System Preferences > Security & Privacy > Camera
   - **Windows**: Settings > Privacy > Camera  
   - **Linux**: `sudo usermod -a -G video $USER`
3. **Restart aplikasi** atau komputer
4. **Coba kamera external** jika built-in camera bermasalah

### Error: ModuleNotFoundError
- Pastikan virtual environment sudah diaktifkan
- Install ulang dependencies: `pip install -r requirements.txt`

### Error: ImportError atau dependency conflicts
- Hapus virtual environment dan buat ulang:
  ```bash
  rm -rf mediapipe_env
  python3 -m venv mediapipe_env
  source mediapipe_env/bin/activate
  pip install -r mediapipe_app/requirements.txt
  ```

### Deteksi wajah/tangan tidak akurat
- **Pencahayaan**: Pastikan ruangan cukup terang, hindari backlight
- **Jarak**: Posisikan 30-60 cm dari kamera  
- **Background**: Gunakan background kontras dengan wajah/tangan
- **Stabilitas**: Gerakkan wajah/tangan secara perlahan

### GUI tidak muncul / Error tkinter
- **macOS**: Install Python dengan tkinter: `brew install python-tk`
- **Linux**: Install tkinter: `sudo apt-get install python3-tk`
- **Windows**: Tkinter biasanya sudah included

### 📋 Quick Diagnostics
Jika masalah berlanjut, lihat file `../CAMERA_TROUBLESHOOTING.md` untuk panduan lengkap.

## Persyaratan Sistem

- **Python**: 3.8 atau lebih tinggi
- **Kamera**: Webcam atau kamera laptop yang berfungsi
- **RAM**: Minimal 4GB (recommended 8GB)
- **OS**: Windows 10+, macOS 10.15+, atau Linux Ubuntu 18.04+

## Dependencies

- `mediapipe==0.10.21` - Library untuk face detection dan hand tracking
- `opencv-python==4.12.0.88` - Library untuk computer vision
- `numpy>=1.21.0,<2.0.0` - Library untuk operasi array

## Perintah Lengkap dari Awal

```bash
# 1. Buat dan masuk ke direktori project
mkdir mediapipe_project
cd mediapipe_project

# 2. Buat virtual environment
python3 -m venv mediapipe_env

# 3. Aktivasi virtual environment
source mediapipe_env/bin/activate  # macOS/Linux
# atau
mediapipe_env\Scripts\activate     # Windows

# 4. Install dependencies
pip install mediapipe opencv-python "numpy<2"

# 5. Buat struktur folder dan file (jika belum ada)
mkdir -p mediapipe_app/src

# 6. Jalankan aplikasi
cd mediapipe_app
python main.py
```

## Tips Penggunaan

1. **Pencahayaan**: Gunakan pencahayaan yang cukup untuk hasil deteksi terbaik
2. **Jarak**: Posisikan wajah/tangan 30-60 cm dari kamera
3. **Background**: Gunakan background yang kontras dengan kulit
4. **Stabilitas**: Gerakkan tangan secara perlahan untuk gesture yang stabil
5. **Performance**: Tutup aplikasi lain yang menggunakan kamera untuk performa optimal