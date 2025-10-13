# 📹 Troubleshooting Kamera - MediaPipe App

## Masalah Umum dan Solusi

### 🔴 Error: "Tidak dapat mengakses kamera"

#### Kemungkinan Penyebab:
1. **Kamera sedang digunakan aplikasi lain**
   - Zoom, Skype, Teams, atau video call apps lainnya
   - Browser dengan tab yang menggunakan kamera
   - Aplikasi streaming atau recording

2. **Permission kamera ditolak**
   - macOS: System Preferences > Security & Privacy > Camera
   - Windows: Settings > Privacy > Camera
   - Linux: Check camera permissions

3. **Driver kamera bermasalah**
   - Kamera tidak terdeteksi sistem
   - Driver outdated atau corrupt

#### Solusi:

##### 🔧 Langkah Cepat:
```bash
# 1. Test kamera dengan script khusus
cd "/path/to/Pipeline"
source mediapipe_env/bin/activate
python test_camera.py

# 2. Restart aplikasi
./run_gui.sh

# 3. Jika masih error, restart sistem
```

##### 🛠️ Troubleshooting Mendalam:

**macOS:**
1. Buka **System Preferences** > **Security & Privacy** > **Camera**
2. Pastikan **Terminal** atau **Python** memiliki akses kamera
3. Restart aplikasi setelah memberikan permission

**Windows:**
1. Buka **Settings** > **Privacy** > **Camera**
2. Pastikan "Allow apps to access your camera" aktif
3. Pastikan Python/Command Prompt memiliki akses

**Linux (Ubuntu/Debian):**
```bash
# Check camera devices
ls /dev/video*

# Check camera permissions
sudo usermod -a -G video $USER

# Test camera with v4l2
v4l2-ctl --list-devices
```

##### 📱 Check Aplikasi Lain:
```bash
# macOS - Lihat proses yang menggunakan kamera
sudo lsof | grep -i camera

# Kill aplikasi yang menggunakan kamera (ganti PID)
kill -9 [PID]
```

### 🟡 Kamera Terbuka tapi Tidak Ada Gambar

#### Penyebab dan Solusi:
1. **Kamera tertutup/blocked**
   - Buka penutup kamera laptop
   - Periksa fisik kamera

2. **Pencahayaan terlalu gelap**
   - Tambah pencahayaan ruangan
   - Posisikan dekat jendela/lampu

3. **Resolusi tidak supported**
   - Aplikasi otomatis mencari resolusi yang cocok

### 🟢 Tips Optimal Camera Performance

#### 🎯 Positioning:
- Jarak ideal: **30-60 cm** dari kamera
- Pencahayaan: **Cukup terang**, hindari backlight
- Background: **Kontras** dengan wajah/tangan

#### ⚙️ Performance:
- Tutup aplikasi lain yang berat
- Gunakan resolusi moderate (640x480 - 1280x720)
- Pastikan laptop tidak overheating

#### 🔍 Debug Mode:
Untuk debugging lebih lanjut, buka terminal dan jalankan:
```bash
cd "/path/to/Pipeline"
source mediapipe_env/bin/activate
cd mediapipe_app
python -c "
import cv2
cap = cv2.VideoCapture(0)
print('Camera opened:', cap.isOpened())
if cap.isOpened():
    ret, frame = cap.read()
    print('Frame captured:', ret)
    if ret:
        print('Frame shape:', frame.shape)
cap.release()
"
```

## 🚨 Error Codes dan Artinya

| Error | Arti | Solusi |
|-------|------|--------|
| `Camera not accessible` | Kamera tidak bisa dibuka | Check permissions & close other apps |
| `Cannot capture frames` | Kamera buka tapi tidak bisa baca frame | Restart camera/system |
| `Consecutive frame failures` | Koneksi kamera hilang saat berjalan | Reconnect camera, restart app |
| `Face detection error` | MediaPipe face detection gagal | Check pencahayaan, posisi wajah |
| `Hand tracking error` | MediaPipe hand tracking gagal | Check pencahayaan, posisi tangan |

## 📞 Bantuan Lebih Lanjut

Jika masalah masih berlanjut:

1. **Jalankan diagnostic:**
   ```bash
   python test_camera.py
   ```

2. **Check system info:**
   - OS version
   - Camera model
   - Python version
   - OpenCV version

3. **Coba alternative:**
   - Gunakan external USB camera
   - Test dengan aplikasi kamera lain
   - Update driver kamera

4. **Reset environment:**
   ```bash
   # Hapus dan buat ulang virtual environment
   rm -rf mediapipe_env
   python3 -m venv mediapipe_env
   source mediapipe_env/bin/activate
   pip install -r mediapipe_app/requirements.txt
   ```

---
*Dokumen ini akan terus diupdate sesuai dengan isu yang ditemukan users.*