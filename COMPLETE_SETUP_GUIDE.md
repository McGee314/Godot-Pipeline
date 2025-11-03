# 📺 Webcam Streaming + Hand Gesture Control - Godot

## 🎯 Cara Menggunakan Sistem Lengkap

Sistem ini terdiri dari **2 komponen utama**:
1. **Webcam Streaming** (Python → Godot) di port **8888**
2. **Hand Gesture Control** (Python → Godot) di port **9999**

---

## 🚀 Quick Start

### Terminal 1️⃣: Jalankan Webcam Server
```bash
cd /path/to/Pipeline
./start_webcam_server.sh
```

**Atau manual:**
```bash
python webcam_server_udp.py
```

**Output yang benar:**
```
🚀 UDP Server dimulai di localhost:8888
📺 Server berjalan! Client dapat bergabung dengan mengirim 'REGISTER'
⌨️  Tekan Ctrl+C untuk menghentikan server
```

---

### Terminal 2️⃣: Jalankan Hand Gesture Tracker
```bash
cd mediapipe_app
python hand_gesture_only.py
```

**Output yang benar:**
```
🚀 Hand Gesture Tracker Started
📡 Sending to Godot: 127.0.0.1:9999
❌ Press 'q' to quit
```

---

### Godot 3️⃣: Jalankan Scene
1. Buka **Godot Engine**
2. Load project `Godot_Project/`
3. Buka scene **`webcam_client_udp.tscn`**
4. Klik **Play** (F5)
5. Klik tombol **"Connect to Server"**

**Console output yang benar:**
```
🎮 Godot UDP client initialized
📺 Webcam server: 127.0.0.1:8888
👋 Gesture port: 9999
✅ Listening for gestures on UDP port: 9999
🔄 Starting UDP connection...
✅ UDP client ready to communicate with 127.0.0.1:8888
📤 Registration sent to server, waiting for confirmation...
📥 Received: REGISTERED
✅ Registration confirmed!
🎥 Ready to receive video streams!
```

Di Python server akan muncul:
```
✅ Client terdaftar: ('127.0.0.1', 54321)
📊 Total clients: 1
```

---

## 🎮 Kontrol Gesture Tangan

Ketika hand gesture tracker jalan, gerakkan tangan Anda:

| Posisi Tangan | Gesture | Efek di Godot |
|--------------|---------|---------------|
| 🖐️ Atas layar | `UP` | Drone maju (forward -Z) |
| 🖐️ Bawah layar | `DOWN` | Drone mundur (+Z) |
| 🖐️ Kiri layar | `LEFT` | Drone ke kiri (-X) |
| 🖐️ Kanan layar | `RIGHT` | Drone ke kanan (+X) |
| 🖐️ Tengah | `CENTER` | Drone berhenti |

---

## 🔧 Troubleshooting

### ❌ Problem: "Registration timeout" di Godot

**Penyebab:**
- Python server belum jalan
- Port 8888 sudah dipakai aplikasi lain

**Solusi:**
```bash
# 1. Cek apakah server jalan
ps aux | grep webcam_server_udp

# 2. Cek port 8888
lsof -i :8888

# 3. Kill proses yang pakai port 8888
kill -9 <PID>

# 4. Restart server
python webcam_server_udp.py
```

---

### ❌ Problem: Video tidak muncul di Godot

**Penyebab:**
- Kamera tidak terbuka
- Tidak ada client registration

**Solusi:**
```bash
# 1. Test kamera dulu
python test_camera.py

# 2. Pastikan di console server muncul:
✅ Client terdaftar: ('127.0.0.1', xxxx)

# 3. Di Godot console harus ada:
✅ Registration confirmed!
📊 Frame 1 completed
```

---

### ❌ Problem: Gesture tidak menggerakkan drone

**Penyebab:**
- Hand gesture tracker belum jalan
- Port 9999 blocked
- `controlled_object` tidak ditemukan

**Solusi di Godot Console:**
```
✅ Listening for gestures on UDP port: 9999
✅ Auto-detected controlled object: Sketchfab_Scene
👋 Gesture received: UP
```

**Jika tidak ada object:**
1. Buka scene `WorldEnv.tscn`
2. Pastikan ada node `Sketchfab_Scene` (drone)
3. Atau manual assign di Inspector: `WebcamClient` → `Controlled Object`

---

## 📊 Monitoring

### Python Server Console:
```
📤 Sent frame 30: 12534 bytes in 2 packets to 1 clients
```

### Godot Console:
```
📊 Frame 30 completed. Drop rate: 0.5%
FPS: 29.8
Rate: 156.3 KB/s
👋 Gesture received: UP
```

---

## ⚙️ Konfigurasi Advanced

### Python - Ubah Port/Host
Edit `webcam_server_udp.py`:
```python
server = WebcamServerUDP(host='0.0.0.0', port=8888)  # Listen semua interface
```

### Godot - Ubah Settings
Di Inspector → `WebcamClient`:
- **Server Host**: `127.0.0.1` (localhost) atau IP remote
- **Server Port**: `8888`
- **Gesture Port**: `9999`
- **Move Speed**: `5.0` (kecepatan drone)
- **Smooth Movement**: `true` (gerakan halus)

---

## 🎬 Urutan Start yang Benar

1. ✅ **Start Python Webcam Server** (`webcam_server_udp.py`)
2. ✅ **Start Python Hand Gesture** (`hand_gesture_only.py`)
3. ✅ **Start Godot Scene** (F5)
4. ✅ **Klik "Connect to Server"** di Godot
5. ✅ **Gerakkan tangan** untuk kontrol drone! 🚁

---

## 🛑 Cara Stop

1. **Godot**: Klik "Disconnect" atau close window
2. **Hand Gesture**: Press `Q` di window OpenCV
3. **Webcam Server**: Press `Ctrl+C` di terminal

---

## 📝 Port Summary

| Port | Protokol | Fungsi | Arah Data |
|------|----------|--------|-----------|
| 8888 | UDP | Webcam streaming | Python → Godot |
| 9999 | UDP | Hand gesture | Python → Godot |

---

## 💡 Tips

- **Pencahayaan**: Pastikan ruangan cukup terang untuk hand tracking
- **Jarak kamera**: 30-60cm dari kamera untuk tracking optimal
- **Network**: Untuk remote testing, ganti `127.0.0.1` dengan IP address
- **Performance**: Close aplikasi lain yang pakai kamera (Zoom, Teams, dll)

---

## ✅ Checklist Debugging

- [ ] Python server running di port 8888
- [ ] Hand gesture tracker running di port 9999
- [ ] Godot scene loaded (webcam_client_udp.tscn)
- [ ] Godot console show "Registration confirmed"
- [ ] Video muncul di Godot window
- [ ] Gesture detected di Python console
- [ ] Drone bergerak sesuai gesture

Jika semua ✅, sistem berjalan sempurna! 🎉
