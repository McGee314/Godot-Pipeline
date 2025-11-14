# 🎮 Panduan Kontrol Gesture Tangan

Dokumentasi lengkap untuk menggunakan sistem kontrol gesture tangan dengan MediaPipe dan Godot.

---

## 📋 Daftar Isi

1. [Persyaratan Sistem](#persyaratan-sistem)
2. [Instalasi](#instalasi)
3. [Cara Menjalankan](#cara-menjalankan)
4. [Kontrol Gesture - Tangan Kiri](#kontrol-gesture---tangan-kiri)
5. [Kontrol Gesture - Tangan Kanan](#kontrol-gesture---tangan-kanan)
6. [Tips Penggunaan](#tips-penggunaan)
7. [Troubleshooting](#troubleshooting)

---

## 🖥️ Persyaratan Sistem

### Hardware
- **Kamera webcam** yang berfungsi
- **RAM minimum**: 4GB
- **Processor**: Intel Core i5 atau setara

### Software
- **Python 3.10+**
- **OpenCV** (`cv2`)
- **MediaPipe**
- **Godot 4.x** (opsional, untuk integrasi game)

---

## 📦 Instalasi

### 1. Activate Virtual Environment
```bash
cd mediapipe_app
source ../mediapipe_env/bin/activate  # macOS/Linux
# atau
../mediapipe_env/Scripts/activate     # Windows
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Test Kamera
```bash
python test_camera.py
```

---

## 🚀 Cara Menjalankan

### Menjalankan Hand Gesture Control

```bash
cd mediapipe_app
python main.py
```

**Instruksi:**
1. Aplikasi akan membuka window kamera
2. Tunjukkan tangan Anda ke kamera
3. Lakukan gesture sesuai panduan di bawah
4. Tekan **'q'** untuk keluar

---

## 👈 Kontrol Gesture - Tangan Kiri

Tangan kiri digunakan untuk **Movement (WASD)** - kontrol horizontal dan maju/mundur.

### ✊ FORWARD (Maju - W)
**Gesture:** Kepal tangan (0 jari terangkat)

![FORWARD](Keperluan%20Dokumentasi/FORWARD.png)

**Kegunaan:**
- Drone bergerak maju
- Karakter berjalan ke depan

---

### 🖐️ BACKWARD (Mundur - S)
**Gesture:** Semua 5 jari terangkat

![BACKWARD](Keperluan%20Dokumentasi/BACKWARD.png)

**Kegunaan:**
- Drone bergerak mundur
- Karakter berjalan ke belakang

---

### 👍 RIGHT (Kanan - D)
**Gesture:** Jari telunjuk + jempol terangkat (2 jari)

![RIGHT](Keperluan%20Dokumentasi/RIGHT.png)

**Kegunaan:**
- Drone bergerak ke kanan
- Karakter bergerak ke kanan (strafe right)

---

### ✌️ LEFT (Kiri - A)
**Gesture:** Jari telunjuk + jari tengah terangkat (2 jari)

![LEFT](Keperluan%20Dokumentasi/LEFT.png)

**Kegunaan:**
- Drone bergerak ke kiri
- Karakter bergerak ke kiri (strafe left)

---

## 👉 Kontrol Gesture - Tangan Kanan

Tangan kanan digunakan untuk **Vertical Movement + Rotation** - kontrol naik/turun dan rotasi.

### ✊ UP (Naik)
**Gesture:** Kepal tangan (0 jari terangkat)

![UP](Keperluan%20Dokumentasi/UP.png)

**Kegunaan:**
- Drone naik ke atas
- Karakter melompat / terbang ke atas

---

### 🖐️ DOWN (Turun)
**Gesture:** Semua 5 jari terangkat

![DOWN](Keperluan%20Dokumentasi/DOWN.png)

**Kegunaan:**
- Drone turun ke bawah
- Karakter jongkok / terbang ke bawah

---

### ✌️ ROTATE_RIGHT (Rotasi Kanan)
**Gesture:** Jari telunjuk + jari tengah terangkat (2 jari)

![ROTATE_RIGHT](Keperluan%20Dokumentasi/ROTATE_RIGHT.png)

**Kegunaan:**
- Drone berputar ke kanan (yaw right)
- Kamera/karakter memutar pandangan ke kanan

---

### 👍 ROTATE_LEFT (Rotasi Kiri)
**Gesture:** Jari telunjuk + jempol terangkat (2 jari)

![ROTATE_LEFT](Keperluan%20Dokumentasi/ROTATE_LEFT.png)

**Kegunaan:**
- Drone berputar ke kiri (yaw left)
- Kamera/karakter memutar pandangan ke kiri

---

## 💡 Tips Penggunaan

### 1. **Posisi Tangan yang Optimal**
- Jarak kamera: **30-50 cm** dari wajah
- Pastikan tangan Anda berada dalam frame kamera
- Latar belakang yang kontras membantu deteksi

### 2. **Pencahayaan**
- Gunakan pencahayaan yang **cukup terang**
- Hindari backlight (cahaya dari belakang)
- Pencahayaan merata dari depan/samping lebih baik

### 3. **Gesture yang Jelas**
- Buat gesture dengan **jelas dan tegas**
- Tahan gesture selama **0.5-1 detik** agar terdeteksi
- Jangan terlalu cepat berganti gesture

### 4. **Mirror Effect**
- Video kamera di-flip horizontal (mirror mode)
- Tangan kiri di layar = tangan kiri fisik Anda
- Tangan kanan di layar = tangan kanan fisik Anda

### 5. **Kombinasi Tangan**
Anda bisa menggunakan **kedua tangan sekaligus**:
- Tangan kiri: FORWARD (maju)
- Tangan kanan: UP (naik)
- Hasil: Drone maju sambil naik

---

## 🔧 Troubleshooting

### ❌ Kamera Tidak Terdeteksi
**Solusi:**
```bash
# Test kamera terlebih dahulu
python test_camera.py

# Pastikan tidak ada aplikasi lain yang menggunakan kamera
# Restart aplikasi jika perlu
```

### ❌ Gesture Tidak Terdeteksi
**Kemungkinan penyebab:**
1. **Pencahayaan kurang** - Tambah sumber cahaya
2. **Tangan terlalu jauh/dekat** - Sesuaikan jarak
3. **Gesture tidak jelas** - Pastikan jari yang benar terangkat
4. **Confidence threshold terlalu tinggi** - Lihat debug info di layar

**Cek debug info:**
- Di layar akan muncul: `Left: 2 fingers` dan `Thumb, Index`
- Pastikan jumlah jari dan nama jari sesuai gesture yang Anda buat

### ❌ Tangan Kiri/Kanan Tertukar
**Solusi:**
- Sistem menggunakan mirror mode (normal untuk webcam)
- Pastikan Anda melihat label "Left" atau "Right" di layar
- Jika tertukar, coba posisikan tangan lebih jelas di frame

### ❌ Deteksi Lambat/Lag
**Solusi:**
1. Close aplikasi lain yang berat
2. Turunkan resolution kamera (edit di `hand_tracking.py`)
3. Pastikan lighting optimal untuk mengurangi processing

### ❌ UDP Tidak Terkirim ke Godot
**Solusi:**
```bash
# Cek apakah Godot sudah running dan listening di port 9999
# Di Godot, pastikan GestureControl.tscn sudah aktif

# Test manual dengan netcat:
echo "test" | nc -u 127.0.0.1 9999
```

---

## 📊 Ringkasan Kontrol

| Tangan | Gesture | Jari | Aksi | Kegunaan |
|--------|---------|------|------|----------|
| **Kiri** | ✊ Kepal | 0 | FORWARD | Maju (W) |
| **Kiri** | 🖐️ Terbuka | 5 | BACKWARD | Mundur (S) |
| **Kiri** | 👍 Telunjuk+Jempol | 2 | RIGHT | Kanan (D) |
| **Kiri** | ✌️ Telunjuk+Tengah | 2 | LEFT | Kiri (A) |
| **Kanan** | ✊ Kepal | 0 | UP | Naik |
| **Kanan** | 🖐️ Terbuka | 5 | DOWN | Turun |
| **Kanan** | ✌️ Telunjuk+Tengah | 2 | ROTATE_RIGHT | Putar Kanan |
| **Kanan** | 👍 Telunjuk+Jempol | 2 | ROTATE_LEFT | Putar Kiri |

---

## 🎯 Contoh Penggunaan dalam Game

### Skenario 1: Terbang Drone
```
1. Tangan kiri kepal (FORWARD) → Drone maju
2. Tangan kanan kepal (UP) → Drone naik
3. Hasil: Drone maju sambil naik
```

### Skenario 2: Eksplorasi
```
1. Tangan kiri telunjuk+tengah (LEFT) → Gerak ke kiri
2. Tangan kanan telunjuk+jempol (ROTATE_LEFT) → Putar kiri
3. Hasil: Strafe kiri sambil memutar pandangan
```

### Skenario 3: Hover di Tempat
```
1. Tidak ada gesture → Drone hover (diam di tempat)
2. Atau semua jari diturunkan (selain gesture valid)
```

---

## 📞 Support

Jika mengalami masalah:
1. Periksa section **Troubleshooting** di atas
2. Pastikan semua dependencies terinstall dengan benar
3. Cek debug info yang muncul di layar
4. Test gesture satu per satu untuk isolasi masalah

---

## 📝 Catatan Teknis

### Teknologi yang Digunakan
- **MediaPipe Hands**: Hand landmark detection (21 points per hand)
- **OpenCV**: Video capture dan image processing
- **UDP Socket**: Communication dengan Godot (port 9999)
- **Python 3.10+**: Backend processing

### Algoritma Deteksi
1. **Finger Counting**: Menghitung jari yang terangkat berdasarkan landmark position
2. **Hand Orientation**: Deteksi tangan kiri/kanan berdasarkan handedness
3. **Gesture Recognition**: Kombinasi finger count + specific fingers
4. **Rate Limiting**: 100ms cooldown untuk menghindari spam

### Performance
- **FPS target**: 30 FPS
- **Latency**: < 100ms dari gesture ke deteksi
- **Confidence threshold**: 0.7 (70%)
- **Max hands**: 2 (left + right)

---

**Happy Gesturing! 🎮✋**
