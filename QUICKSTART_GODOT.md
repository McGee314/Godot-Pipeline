# 🚀 Quick Start - Hand Gesture Control dengan Godot

## Step-by-Step Setup

### 1️⃣ Setup Python MediaPipe

```bash
# Dari folder Pipeline
source mediapipe_env/bin/activate
pip install -r mediapipe_app/requirements.txt
```

### 2️⃣ Jalankan Godot

1. Buka **Godot Engine**
2. Klik **Import** → Pilih folder `Godot_Project/`
3. Buka scene **`GestureControl.tscn`**
4. Klik **Play** (F5) atau tombol ▶️

Godot sekarang listening di port **9999** untuk gesture!

### 3️⃣ Jalankan Hand Tracking

**Option A: GUI (Recommended)**
```bash
./run_gui.sh
```
- Login (opsional)
- Klik **"👋 Hand Gesture Control"**
- Klik **"▶️ Mulai Tracking"**
- Gerakkan tangan! 🖐️

**Option B: Terminal**
```bash
./run_app.sh
```
- Pilih menu **2**
- Gerakkan tangan! 🖐️

### 4️⃣ Kontrol Objek!

| Gesture | Action |
|---------|--------|
| 👆 ATAS | Maju (Forward) |
| 👇 BAWAH | Mundur (Backward) |
| 👈 KIRI | Ke Kiri |
| 👉 KANAN | Ke Kanan |
| 🖐️ CENTER | Berhenti |

## 🧪 Test Koneksi

Sebelum mulai, test dulu koneksinya:

```bash
python test_gesture_udp.py
```

Pilih **1** untuk test sender (Python → Godot)

## ⚙️ Konfigurasi

### Python - Environment Variables
```bash
export GESTURE_UDP_HOST=127.0.0.1  # Default
export GESTURE_UDP_PORT=9999        # Default
```

### Godot - Inspector Settings
Pilih node **GestureReceiver** di Inspector:
- `move_speed`: 5.0 (kecepatan)
- `smooth_movement`: true (smooth vs step)
- `movement_scale`: 1.0 (scale gerakan)
- `show_debug`: true (debug console)

## 🐛 Troubleshooting

### Python tidak kirim gesture
```bash
# Check output console
# Harus ada: "✅ UDP gesture sender initialized"
```

### Godot tidak terima gesture
```bash
# Check Godot console
# Harus ada: "✅ Listening for gestures on UDP port: 9999"

# Check port
lsof -i :9999  # macOS/Linux
```

### Objek tidak bergerak
1. Check **Inspector** → GestureReceiver → controlled_object
2. Pastikan ada node assigned (biasanya Sketchfab_Scene)
3. Check move_speed > 0

### Gerakan terlalu cepat/lambat
- Turun/naikkan `move_speed` di Inspector
- Toggle `smooth_movement` on/off

## 📺 Demo Flow

```
[Python Camera] → [MediaPipe] → [Gesture Detection]
                                        ↓
                                   UDP :9999
                                        ↓
[Godot Receiver] → [3D Object Movement] → [Visual Feedback]
```

## 🎯 Tips

✅ **Pencahayaan bagus** - Ruangan terang  
✅ **Jarak optimal** - 30-60cm dari kamera  
✅ **Background kontras** - Tangan vs background  
✅ **Gerakan smooth** - Jangan terlalu cepat  

## 📚 Dokumentasi Lengkap

👉 `Godot_Project/GESTURE_INTEGRATION.md`

---

**Happy Coding! 🎮✨**
