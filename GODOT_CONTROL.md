# Hand Gesture Control untuk Godot (Tanpa GUI)

## 🎮 Cara Pakai

### 1. Jalankan Python Hand Tracking
```bash
# Di terminal:
cd mediapipe_app
python hand_gesture_only.py
```

Atau gunakan script shortcut:
```bash
./run_gesture.sh
```

### 2. Jalankan Godot
- Buka project Godot
- Jalankan scene dengan `webcam_client_udp.tscn`
- Objek 3D akan bergerak sesuai gesture tangan

## 🖐️ Gesture yang Didukung

| Gesture | Arah Gerakan | Kontrol di Godot |
|---------|--------------|------------------|
| **UP** | Tangan ke atas layar | Objek maju (forward) |
| **DOWN** | Tangan ke bawah layar | Objek mundur (backward) |
| **LEFT** | Tangan ke kiri layar | Objek ke kiri |
| **RIGHT** | Tangan ke kanan layar | Objek ke kanan |
| **CENTER** | Tangan di tengah | Objek berhenti |

## 📡 Komunikasi

- Python mengirim gesture via UDP ke port **9999**
- Godot menerima gesture dan menggerakkan objek 3D
- Format pesan: JSON `{"type":"gesture","gesture":"UP","timestamp":...}`

## ⚙️ Pengaturan di Godot

Di Inspector, atur:
- **Controlled Object**: Node3D yang ingin dikontrol (auto-detect `Sketchfab_Scene`)
- **Move Speed**: Kecepatan gerakan (default: 5.0)
- **Smooth Movement**: Aktifkan untuk gerakan halus
- **Movement Scale**: Skala gerakan (default: 1.0)

## 🔧 Troubleshooting

### Camera tidak terbuka
```bash
# Test camera:
python test_camera.py
```

### Gesture tidak terkirim
```bash
# Test UDP connection:
cd mediapipe_app
python ../test_gesture_udp.py sender
```

### Godot tidak menerima
Cek console Godot, harus muncul:
```
✅ Gesture UDP bound to port 9999
👋 Gesture received: UP
```

## ⌨️ Keyboard Shortcuts

- **Q**: Quit aplikasi Python
- **ESC**: Stop di Godot

## 📝 Catatan

- **TIDAK ADA GUI** - Fokus langsung ke Godot
- Hanya menampilkan window kamera dengan overlay gesture
- Otomatis kirim gesture ke Godot real-time
- Minimal delay, responsif untuk game control
