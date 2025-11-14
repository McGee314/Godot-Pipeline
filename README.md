# MediaPipe Face Detection & Hand Gesture Control

Aplikasi Python untuk Face Detection Login dan Hand Gesture Control menggunakan MediaPipe, dengan integrasi Godot Engine untuk kontrol drone/game real-time via UDP.

## 🎯 Fitur Utama

1. **Face Detection Login** 
   - Login sistem menggunakan deteksi wajah MediaPipe
   - Streaming video via UDP ke Godot
   - Deteksi wajah dengan confidence threshold 70%
   
2. **Hand Gesture Control** 
   - Kontrol 2 tangan simultan (kiri & kanan)
   - 8 gesture berbeda untuk kontrol lengkap
   - Real-time gesture recognition
   - UDP communication dengan Godot (port 9999)
   
3. **🎮 Integrasi Godot Engine**
   - Kontrol drone 3D di Godot dengan gesture tangan
   - Face detection login di Godot
   - Real-time UDP communication
   - Scene flow: Main_UI → Login → WorldEnv (game)

## 📁 Struktur Project

```
Pipeline/
├── mediapipe_env/           # Virtual environment Python
├── mediapipe_app/           # Aplikasi Python utama
│   ├── src/                 # Core functionality
│   │   ├── face_detection.py    # MediaPipe face detection
│   │   └── hand_tracking.py     # MediaPipe hand tracking & gesture
│   ├── main.py              # Entry point - Hand Gesture Control
│   ├── login.py             # Face detection video streamer (UDP)
│   ├── requirements.txt     # Python dependencies
│   └── README.md
├── Godot_Project/          # Godot 4.x integration
│   ├── Scene/
│   │   ├── Main_UI.tscn         # Main menu
│   │   ├── Login.tscn           # Face detection login UI
│   │   ├── WorldEnv.tscn        # Game scene with drone
│   │   └── GestureControl.tscn  # Gesture control scene
│   ├── Scripts/
│   │   ├── main_ui.gd           # Main menu controller
│   │   ├── login.gd             # Login + UDP video receiver
│   │   ├── drone.gd             # Drone flight controls
│   │   └── gesture_receiver.gd  # Gesture UDP receiver
│   └── Models/                  # 3D models
├── Keperluan Dokumentasi/   # Gesture images untuk dokumentasi
│   ├── FORWARD.png
│   ├── BACKWARD.png
│   ├── LEFT.png
│   ├── RIGHT.png
│   ├── UP.png
│   ├── DOWN.png
│   ├── ROTATE_LEFT.png
│   └── ROTATE_RIGHT.png
├── GESTURE_CONTROL_GUIDE.md # 📖 Panduan lengkap gesture control
├── CARA_PAKAI_BARU.md       # Panduan login system baru
└── README.md                # Dokumentasi utama (file ini)
```

## 🚀 Quick Start

### 1. Setup Virtual Environment

```bash
# Buat virtual environment (jika belum ada)
python3 -m venv mediapipe_env

# Aktivasi virtual environment
source mediapipe_env/bin/activate  # macOS/Linux
# atau
mediapipe_env\Scripts\activate     # Windows
```

### 2. Install Dependencies

```bash
cd mediapipe_app
pip install -r requirements.txt
```

### 3. Jalankan Aplikasi

#### A. Hand Gesture Control (Direct)
```bash
cd mediapipe_app
python main.py
```
**Kegunaan:** Langsung buka kamera untuk gesture control tanpa login

#### B. Face Detection Login (UDP Streaming ke Godot)
```bash
cd mediapipe_app
python login.py
```
**Kegunaan:** Stream video dengan face detection ke Godot untuk login system

---

## 🎮 Hand Gesture Control - Panduan Lengkap

### Kontrol 2 Tangan Simultan

Sistem menggunakan **2 tangan** untuk kontrol penuh:
- **👈 Tangan Kiri**: Movement (WASD - maju, mundur, kiri, kanan)
- **👉 Tangan Kanan**: Vertical + Rotation (naik, turun, rotasi)

---

### 👈 Tangan Kiri - Movement (WASD)

| Gesture | Gambar | Jari | Aksi | Kegunaan |
|---------|--------|------|------|----------|
| **✊ KEPAL** | ![FORWARD](Keperluan%20Dokumentasi/FORWARD.png) | 0 jari | FORWARD (W) | Drone maju |
| **🖐️ TERBUKA** | ![BACKWARD](Keperluan%20Dokumentasi/BACKWARD.png) | 5 jari | BACKWARD (S) | Drone mundur |
| **👍 Telunjuk+Jempol** | ![RIGHT](Keperluan%20Dokumentasi/RIGHT.png) | 2 jari | RIGHT (D) | Drone ke kanan |
| **✌️ Telunjuk+Tengah** | ![LEFT](Keperluan%20Dokumentasi/LEFT.png) | 2 jari | LEFT (A) | Drone ke kiri |

---

### 👉 Tangan Kanan - Vertical + Rotation

| Gesture | Gambar | Jari | Aksi | Kegunaan |
|---------|--------|------|------|----------|
| **✊ KEPAL** | ![UP](Keperluan%20Dokumentasi/UP.png) | 0 jari | UP | Drone naik |
| **🖐️ TERBUKA** | ![DOWN](Keperluan%20Dokumentasi/DOWN.png) | 5 jari | DOWN | Drone turun |
| **✌️ Telunjuk+Tengah** | ![ROTATE_RIGHT](Keperluan%20Dokumentasi/ROTATE_RIGHT.png) | 2 jari | ROTATE_RIGHT | Putar kanan (yaw) |
| **👍 Telunjuk+Jempol** | ![ROTATE_LEFT](Keperluan%20Dokumentasi/ROTATE_LEFT.png) | 2 jari | ROTATE_LEFT | Putar kiri (yaw) |

---

### 💡 Tips Penggunaan Gesture

#### 1. **Posisi Optimal**
- **Jarak kamera**: 30-50 cm dari wajah
- Pastikan kedua tangan dalam frame
- Latar belakang kontras membantu deteksi

#### 2. **Pencahayaan**
- Gunakan pencahayaan **terang dan merata**
- Hindari backlight (cahaya dari belakang)
- Pencahayaan dari depan/samping lebih baik

#### 3. **Gesture yang Jelas**
- Buat gesture dengan **tegas dan jelas**
- Tahan gesture 0.5-1 detik agar terdeteksi
- Jangan terlalu cepat berganti gesture

#### 4. **Kombinasi Tangan**
Anda bisa gunakan **kedua tangan sekaligus**:
```
Contoh 1: Tangan kiri KEPAL (maju) + Tangan kanan KEPAL (naik)
         = Drone maju sambil naik

Contoh 2: Tangan kiri Telunjuk+Tengah (kiri) + Tangan kanan Telunjuk+Jempol (rotasi kiri)
         = Strafe kiri sambil putar kiri
```

#### 5. **Debug Info**
Di layar akan muncul:
- Label tangan (Left/Right)
- Jumlah jari terdeteksi
- Nama jari yang terangkat (Thumb, Index, Middle, Ring, Pinky)
- Gesture yang terdeteksi (FORWARD, LEFT, UP, dll)

---

### 📊 Ringkasan Kontrol

| Tangan | Gesture | Jari | Command | Game Action |
|--------|---------|------|---------|-------------|
| Kiri | ✊ Kepal | 0 | FORWARD | Maju (W) |
| Kiri | 🖐️ Terbuka | 5 | BACKWARD | Mundur (S) |
| Kiri | 👍 Tel+Jempol | 2 | RIGHT | Kanan (D) |
| Kiri | ✌️ Tel+Tengah | 2 | LEFT | Kiri (A) |
| Kanan | ✊ Kepal | 0 | UP | Naik |
| Kanan | 🖐️ Terbuka | 5 | DOWN | Turun |
| Kanan | ✌️ Tel+Tengah | 2 | ROTATE_RIGHT | Rotasi Kanan |
| Kanan | 👍 Tel+Jempol | 2 | ROTATE_LEFT | Rotasi Kiri |

---

## 🔐 Face Detection Login System

### Arsitektur Baru (Python UDP Streaming + Godot Login Logic)

```
┌─────────────┐         UDP Video Stream          ┌──────────────┐
│  login.py   │  ─────────────────────────────>  │  login.gd    │
│  (Python)   │     (JPEG fragmented packets)     │  (Godot)     │
│             │                                    │              │
│ - Stream    │                                    │ - Receive    │
│ - MediaPipe │                                    │ - Detect     │
│ - Detect    │                                    │ - Login      │
│ - Annotate  │                                    │ - Manual OK  │
└─────────────┘                                    └──────────────┘
```

### Cara Kerja:

#### Python Side (`login.py`):
1. Buka kamera dengan OpenCV
2. Deteksi wajah dengan MediaPipe (confidence ≥70%)
3. Gambar kotak hijau di wajah yang terdeteksi
4. Tambahkan text: "FACE_DETECTED:1" (hijau) atau "NO_FACE_DETECTED" (merah)
5. Encode frame ke JPEG (quality 80%)
6. Fragment JPEG ke paket 60KB (UDP safe)
7. Kirim via UDP ke Godot (port 5000)

#### Godot Side (`login.gd`):
1. Listen UDP port 5000
2. Reassemble fragmented packets
3. Display video di TextureRect (16:9)
4. Detect wajah dengan pixel color sampling:
   - Cari pixel hijau dari kotak MediaPipe
   - Cari text hijau "FACE_DETECTED"
   - Cari text merah "NO_FACE_DETECTED"
5. Hitung frame dengan wajah terdeteksi (butuh 60 frames)
6. Tampilkan progress: "👤 Wajah Terdeteksi: X%"
7. Setelah 100%, enable button "🚀 LANJUT"
8. User klik button → pindah ke WorldEnv.tscn (game)

### Menjalankan Login System:

**Terminal 1 - Python Streamer:**
```bash
cd mediapipe_app
python login.py
```

**Terminal 2 - Godot:**
```bash
# Buka Godot Engine
# Load project: Godot_Project/
# Jalankan Main_UI.tscn (F5)
# Klik tombol "Login"
# Klik "CONNECT CAMERA"
# Tunjukkan wajah ke kamera
# Tunggu progress 100%
# Klik "🚀 LANJUT"
```

---

## 🎮 Integrasi dengan Godot Engine

### Scene Flow

```
Main_UI.tscn (Main Menu)
    ↓ (klik tombol Login)
Login.tscn (Face Detection)
    ↓ (login berhasil + klik LANJUT)
WorldEnv.tscn (Game dengan Drone)
```

### Setup Godot Project

1. **Buka Godot Engine 4.x**
2. **Load Project**: `Godot_Project/`
3. **Test Scene Flow**:
   - Run `Main_UI.tscn` (F5)
   - Klik "Login"
   - Test login (tanpa Python → akan timeout)
   - Quit button → kembali ke Main_UI

### Drone Controls di Godot

Drone di `WorldEnv.tscn` sudah dilengkapi dengan:

#### Keyboard Controls (untuk testing):
- **W/Arrow Up**: Maju / Naik vertical
- **S/Arrow Down**: Mundur / Turun
- **A**: Geser kiri
- **D**: Geser kanan
- **Arrow Left**: Rotasi kiri
- **Arrow Right**: Rotasi kanan
- **Left Shift**: Speed boost (8.0 → 16.0)
- **Spasi**: Naik (khusus vertical, butuh height ≥1.0)

#### Gesture Controls (via UDP port 9999):
Sama dengan gesture table di atas, diterima via `gesture_receiver.gd`

### Test Gesture Integration

**Terminal 1 - Hand Gesture:**
```bash
cd mediapipe_app
python main.py
```

**Terminal 2 - Godot:**
```bash
# Buka Godot
# Run GestureControl.tscn atau WorldEnv.tscn
# Drone akan merespons gesture tangan
```

---

## 🔧 Troubleshooting

### Gesture Tidak Terdeteksi

**Gejala:** Gesture tangan tidak terdeteksi atau salah deteksi

**Solusi:**
1. **Cek pencahayaan** - Pastikan ruangan cukup terang
2. **Cek jarak** - Posisi 30-50cm dari kamera
3. **Lihat debug info** - Di layar muncul jumlah jari terdeteksi
4. **Test satu tangan** - Test tangan kiri dulu, lalu kanan
5. **Cek background** - Gunakan background kontras

**Debug info yang ditampilkan:**
```
Left: 2 fingers
Thumb, Index
LEFT HAND: RIGHT
```

### Kamera Tidak Bisa Dibuka

**Penyebab:**
- Aplikasi lain menggunakan kamera (Zoom, Teams, browser)
- Permission ditolak sistem operasi
- Driver kamera bermasalah

**Solusi:**
```bash
# Test kamera
python test_camera.py

# macOS: Check permission
# System Preferences > Security & Privacy > Camera

# Windows: Check permission  
# Settings > Privacy > Camera

# Linux: Add user to video group
sudo usermod -a -G video $USER
```

### Face Detection Salah/False Positive

**Gejala:** Login terdeteksi tanpa wajah

**Solusi:**
- Sudah diperbaiki dengan pixel color detection
- Confidence threshold ditingkatkan ke 70%
- Deteksi text hijau "FACE_DETECTED" dari Python
- Deteksi kotak hijau MediaPipe bounding box

### UDP Tidak Terkirim

**Gejala:** Gesture tidak sampai ke Godot

**Solusi:**
1. Pastikan Godot running dan listening
2. Check port tidak dipakai aplikasi lain
3. Firewall allow port 9999 (gesture) dan 5000 (video)
4. Test dengan netcat:
   ```bash
   echo "test" | nc -u 127.0.0.1 9999
   ```

### ModuleNotFoundError

**Solusi:**
```bash
# Pastikan virtual env aktif
source mediapipe_env/bin/activate

# Install ulang dependencies
cd mediapipe_app
pip install -r requirements.txt
```

---

## 📋 Persyaratan Sistem

### Hardware
- **Kamera**: Webcam built-in atau eksternal
- **RAM**: Minimum 4GB (recommended 8GB)
- **Processor**: Intel Core i5 atau setara
- **Storage**: 500MB untuk dependencies

### Software
- **Python**: 3.10+ (tested on 3.10)
- **Godot**: 4.x (untuk integrasi game)
- **OS**: 
  - macOS 10.15+
  - Windows 10+
  - Linux Ubuntu 18.04+

### Dependencies (Python)
```
mediapipe>=0.10.0
opencv-python>=4.8.0
numpy<2.0.0
```

---

## 📚 Dokumentasi Tambahan

### Dokumentasi Lengkap
- 📖 **[GESTURE_CONTROL_GUIDE.md](GESTURE_CONTROL_GUIDE.md)** - Panduan lengkap gesture control dengan gambar
- 📖 **[CARA_PAKAI_BARU.md](CARA_PAKAI_BARU.md)** - Panduan login system baru
- 📖 **Godot_Project/GESTURE_INTEGRATION.md** - Integrasi Godot

### Quick Reference
```bash
# Hand Gesture Control
cd mediapipe_app && python main.py

# Face Detection Streaming
cd mediapipe_app && python login.py

# Test kamera
python test_camera.py

# Godot
# Buka Godot > Load Godot_Project/ > Run Main_UI.tscn
```

---

## 🎯 Workflow Lengkap

### Skenario 1: Main Tanpa Login (Gesture Only)

```bash
# Terminal
cd mediapipe_app
python main.py
# Tunjukkan gesture tangan
# Tekan 'q' untuk keluar
```

### Skenario 2: Main dengan Login + Game Godot

**Step 1 - Start Python Face Detection:**
```bash
# Terminal 1
cd mediapipe_app
python login.py
# Biarkan running
```

**Step 2 - Start Godot:**
```bash
# Buka Godot Engine
# Load project: Godot_Project/
# Run Main_UI.tscn (F5)
# Klik "Login"
# Klik "CONNECT CAMERA"
# Tunjukkan wajah
# Tunggu progress 100%
# Klik "🚀 LANJUT"
```

**Step 3 - Start Hand Gesture Control:**
```bash
# Terminal 2 (baru)
cd mediapipe_app
python main.py
# Gesture akan mengontrol drone di Godot
```

**Step 4 - Play the Game:**
```
- Gunakan gesture untuk terbangkan drone
- Atau gunakan keyboard (WASD, arrows, shift)
- Explore dungeon dengan drone
```

---

## 🚀 Teknologi yang Digunakan

### Python Stack
- **MediaPipe**: Hand landmarks (21 points/hand) & Face detection
- **OpenCV**: Video capture, image processing, JPEG encoding
- **NumPy**: Array operations
- **Socket**: UDP communication

### Godot Stack
- **GDScript**: Game logic
- **PacketPeerUDP**: UDP networking
- **CharacterBody3D**: Drone physics
- **TextureRect**: Video display

### Protocols
- **UDP Port 5000**: Video streaming (Python → Godot)
- **UDP Port 9999**: Gesture commands (Python → Godot)
- **JPEG Encoding**: 80% quality, fragmented 60KB packets
- **JSON**: Gesture message format

### Algorithms
- **Finger Counting**: Landmark position comparison
- **Hand Orientation**: Left/right detection via handedness
- **Gesture Recognition**: Finger combination detection
- **Face Detection**: Pixel color sampling + MediaPipe confidence
- **Packet Fragmentation**: Frame reassembly with sequence numbers

---

## 👥 Kontribusi

Project ini dibuat untuk keperluan edukasi dan eksplorasi teknologi computer vision + game integration.

**Fitur yang bisa dikembangkan:**
- [ ] Gesture training/customization
- [ ] Multi-player support
- [ ] Voice commands integration
- [ ] Mobile app (Android/iOS)
- [ ] VR/AR integration

---

## 📄 License

MIT License - Feel free to use and modify

---

## 📞 Support

Jika mengalami masalah:
1. Baca section **Troubleshooting** di atas
2. Check dokumentasi lengkap: `GESTURE_CONTROL_GUIDE.md`
3. Test komponen satu per satu (kamera, gesture, UDP)
4. Lihat debug info di console/layar

---

**Happy Coding & Gaming! 🎮✋🚁**
