# 🎮 Integrasi Hand Gesture Control dengan Godot

## 📋 Deskripsi
Sistem ini menghubungkan deteksi gesture tangan dari MediaPipe (Python) dengan Godot Engine melalui UDP untuk mengontrol objek 3D secara real-time.

## 🔧 Cara Kerja

### Python (MediaPipe)
- Mendeteksi posisi tangan menggunakan MediaPipe
- Menentukan arah gesture (UP, DOWN, LEFT, RIGHT, CENTER)
- Mengirim gesture ke Godot via UDP (port 9999)

### Godot Engine
- Menerima gesture dari Python via UDP
- Menggerakkan objek 3D (drone) sesuai gesture yang diterima
- Smooth movement dengan delta time

## 🚀 Cara Setup

### 1. Setup Python Environment

```bash
# Aktivasi virtual environment
source mediapipe_env/bin/activate

# Pastikan semua dependencies terinstall
pip install -r mediapipe_app/requirements.txt
```

### 2. Setup Godot Project

1. Buka Godot Engine
2. Import/Load project dari folder `Godot_Project/`
3. Buka scene `GestureControl.tscn`
4. Pastikan script `gesture_receiver.gd` sudah ter-attach ke node `GestureReceiver`

### 3. Konfigurasi (Opsional)

#### Python - Environment Variables
```bash
# Default: 127.0.0.1:9999
export GESTURE_UDP_HOST=127.0.0.1
export GESTURE_UDP_PORT=9999
```

#### Godot - Inspector Properties
- **controlled_object**: Node3D yang akan digerakkan (default: auto-detect Sketchfab_Scene)
- **move_speed**: Kecepatan gerakan (default: 5.0)
- **smooth_movement**: Smooth atau step movement (default: true)
- **movement_scale**: Skala pergerakan (default: 1.0)
- **show_debug**: Tampilkan debug log (default: true)

## 🎯 Cara Menggunakan

### Step 1: Jalankan Godot
1. Buka Godot Project
2. Buka scene `GestureControl.tscn`
3. Klik tombol **Play** (F5)
4. Scene akan mulai listening pada UDP port 9999

### Step 2: Jalankan Python MediaPipe

#### Opsi A: GUI Version (Recommended)
```bash
# Dari root folder Pipeline
./run_gui.sh

# Atau manual
source mediapipe_env/bin/activate
cd mediapipe_app
python gui_app.py
```

Kemudian:
1. Login dengan Face Detection (opsional)
2. Klik **"👋 Hand Gesture Control"**
3. Klik **"▶️ Mulai Tracking"**
4. Gerakkan tangan Anda!

#### Opsi B: Terminal Version
```bash
# Dari root folder Pipeline
./run_app.sh

# Atau manual
source mediapipe_env/bin/activate
cd mediapipe_app
python main.py
```

Kemudian pilih menu **"2. Hand Gesture Control"**

### Step 3: Kontrol Objek dengan Tangan
- **Gerakkan tangan ke ATAS** → Drone bergerak forward
- **Gerakkan tangan ke BAWAH** → Drone bergerak backward
- **Gerakkan tangan ke KIRI** → Drone bergerak ke kiri
- **Gerakkan tangan ke KANAN** → Drone bergerak ke kanan
- **Tangan di CENTER** → Drone berhenti

## 📡 Protokol UDP

### Format Message (JSON)
```json
{
  "type": "gesture",
  "gesture": "UP",
  "timestamp": 1234567890.123
}
```

### Gesture Values
- `UP` - Tangan di area atas
- `DOWN` - Tangan di area bawah
- `LEFT` - Tangan di area kiri
- `RIGHT` - Tangan di area kanan
- `CENTER` - Tangan di tengah
- `NO_HAND` - Tidak ada tangan terdeteksi

## 🐛 Troubleshooting

### Python tidak mengirim gesture
1. **Check console output** - Harus ada pesan "✅ UDP gesture sender initialized"
2. **Check firewall** - Pastikan port 9999 tidak diblokir
3. **Test dengan netcat**:
   ```bash
   # Terminal 1
   nc -ul 9999
   
   # Terminal 2 - jalankan Python app
   # Jika berhasil, netcat akan menerima JSON messages
   ```

### Godot tidak menerima gesture
1. **Check console** - Harus ada pesan "✅ Listening for gestures on UDP port: 9999"
2. **Check controlled_object** - Pastikan ada node yang di-assign
3. **Check port conflict** - Pastikan port 9999 tidak dipakai aplikasi lain:
   ```bash
   # macOS/Linux
   lsof -i :9999
   
   # Kill process jika ada
   kill -9 <PID>
   ```

### Objek tidak bergerak
1. **Check Inspector** - Pastikan `GestureReceiver` punya reference ke objek
2. **Check move_speed** - Pastikan tidak 0
3. **Check console** - Lihat apakah gesture diterima ("👋 Gesture received: ...")

### Gerakan terlalu cepat/lambat
- Adjust `move_speed` di Inspector (default: 5.0)
- Adjust `movement_scale` untuk fine-tuning
- Toggle `smooth_movement` untuk step-based movement

## 📊 Architecture

```
┌─────────────────────────┐
│   Python MediaPipe      │
│   ┌─────────────────┐   │
│   │  Hand Tracking  │   │
│   └────────┬────────┘   │
│            │             │
│   ┌────────▼────────┐   │
│   │ Gesture Detect  │   │
│   └────────┬────────┘   │
│            │             │
│   ┌────────▼────────┐   │
│   │  UDP Sender     │   │
│   │  Port: 9999     │   │
│   └────────┬────────┘   │
└────────────┼────────────┘
             │ JSON
             │ {"type":"gesture",
             │  "gesture":"UP"}
             ▼
┌────────────┴────────────┐
│   Godot Engine          │
│   ┌─────────────────┐   │
│   │  UDP Receiver   │   │
│   │  Port: 9999     │   │
│   └────────┬────────┘   │
│            │             │
│   ┌────────▼────────┐   │
│   │ Gesture Handler │   │
│   └────────┬────────┘   │
│            │             │
│   ┌────────▼────────┐   │
│   │  Move Object    │   │
│   │  (Drone/3D)     │   │
│   └─────────────────┘   │
└─────────────────────────┘
```

## 🎨 Customization

### Mengubah Mapping Gesture

Edit file `gesture_receiver.gd`:

```gdscript
match gesture:
    "UP":
        movement = Vector3(0, 1, 0) * move_speed  # Gerak ke atas
    "DOWN":
        movement = Vector3(0, -1, 0) * move_speed  # Gerak ke bawah
    # dst...
```

### Menambah Gesture Baru

1. **Python** - Edit `hand_tracking.py`:
   ```python
   def get_gesture_direction(self, landmarks, frame_width, frame_height):
       # Tambah logic gesture baru
       if condition:
           return "NEW_GESTURE"
   ```

2. **Godot** - Edit `gesture_receiver.gd`:
   ```gdscript
   match gesture:
       "NEW_GESTURE":
           movement = Vector3(x, y, z) * move_speed
   ```

## 📚 Files Yang Dimodifikasi/Dibuat

### Python
- ✏️ `mediapipe_app/src/hand_tracking.py` - Ditambah UDP sender
- ✏️ `mediapipe_app/gui/hand_gesture_window.py` - Ditambah UDP call

### Godot
- ✨ `Godot_Project/gesture_receiver.gd` - Script penerima gesture (BARU)
- ✨ `Godot_Project/GestureControl.tscn` - Scene dengan gesture control (BARU)
- ✨ `Godot_Project/GESTURE_INTEGRATION.md` - Dokumentasi ini (BARU)

## 💡 Tips

1. **Pencahayaan**: Pastikan ruangan cukup terang untuk deteksi tangan
2. **Jarak**: Posisi tangan 30-60 cm dari kamera
3. **Background**: Gunakan background yang kontras dengan warna tangan
4. **Smooth vs Step**: 
   - `smooth_movement = true` → Gerakan smooth (recommended)
   - `smooth_movement = false` → Gerakan step-by-step
5. **Network**: Untuk test remote, ubah `GESTURE_UDP_HOST` ke IP komputer yang menjalankan Godot

## 🔮 Future Enhancements

- [ ] Gesture untuk rotasi objek
- [ ] Multi-hand control
- [ ] Hand pose recognition (fist, peace sign, etc.)
- [ ] Bidirectional communication (Godot → Python feedback)
- [ ] Recording & replay gesture sequences
- [ ] Multiple object control
- [ ] Gesture speed affects object speed

## 📞 Support

Jika ada masalah:
1. Check console output (Python & Godot)
2. Verify UDP port tidak dipakai aplikasi lain
3. Test dengan tool seperti netcat atau Wireshark
4. Check firewall settings

---

**Selamat mencoba! 🚀**
