# 🎮 Cara Pakai Login System - Updated Version

## ✅ Perubahan Utama

### SEBELUM (❌ Salah):
- Python melakukan face detection
- Python menghitung progress login
- Login selesai di Python → langsung stop
- Godot hanya menampilkan video

### SEKARANG (✅ Benar):
- **Python**: Hanya streaming video terus-menerus (tidak stop)
- **Godot**: Melakukan semua face detection dan login logic
- **Godot**: Setelah login berhasil, tampilkan "Login Berhasil!" 
- **Godot**: User harus klik tombol "LANJUT" untuk ke scene berikutnya

---

## 🚀 Cara Menjalankan

### Step 1: Jalankan Python (Video Streamer)

```bash
cd "/Users/samudera/Bagja/Kuliah/Luar Mata Kuliah/Pipeline/mediapipe_app"
source ../mediapipe_env/bin/activate
python login.py
```

**Output yang diharapkan:**
```
==================================================
   VIDEO STREAMING TO GODOT
==================================================
Mode: UDP Video Streamer (No Login Logic)
📡 UDP Target: 127.0.0.1:5000
Login akan dihandle oleh Godot
Tekan Ctrl+C untuk keluar
==================================================

✅ UDP socket created: 127.0.0.1:5000
📦 Max packet size: 60000 bytes
🎨 JPEG quality: 80%

🎥 Camera aktif - Streaming ke Godot...
📡 Menunggu koneksi dari Godot...
Tekan Ctrl+C untuk keluar

💡 Instruksi:
   1. Buka Godot dan jalankan Login.tscn
   2. Klik tombol 'CONNECT CAMERA' di Godot
   3. Video akan muncul di Godot
   4. Godot akan mendeteksi wajah dan handle login

📡 Streaming... (frame: 60)
📡 Streaming... (frame: 120)
📡 Streaming... (frame: 180)
...
```

**✅ Python TIDAK STOP** - terus streaming sampai Ctrl+C!

---

### Step 2: Jalankan Godot (Login UI)

1. **Buka Godot Engine**
2. **Load project** di `/Users/samudera/Bagja/Kuliah/Luar Mata Kuliah/Pipeline/Godot_Project`
3. **Open Scene**: `Scene/Login.tscn`
4. **Play Scene** (F5 atau tombol Play)

---

### Step 3: Connect Camera di Godot

1. Window Godot Login muncul
2. **Klik tombol "📹 CONNECT CAMERA"**
3. Status berubah: "📡 Waiting for video from login.py..."

---

### Step 4: Video Streaming & Face Detection

**Setelah klik CONNECT CAMERA:**

1. ✅ Video muncul di window Godot (16:9 aspect ratio)
2. ✅ Status menunjukkan "Video: Active"
3. ✅ **Godot mulai deteksi wajah otomatis!**
4. ✅ Progress muncul: "👤 Wajah Terdeteksi: 0%"

**Progress face detection:**
```
👤 Wajah Terdeteksi: 10%
👤 Wajah Terdeteksi: 25%
👤 Wajah Terdeteksi: 50% - Hampir selesai!
👤 Wajah Terdeteksi: 75%
👤 Wajah Terdeteksi: 100%
✅ Login Berhasil! Klik LOGIN untuk lanjut.
```

---

### Step 5: Login Berhasil - Klik Tombol untuk Lanjut

**Setelah face detection selesai (100%):**

1. ✅ Status: "✅ Login Berhasil! Klik LOGIN untuk lanjut."
2. ✅ Tombol "LOGIN" berubah jadi "🚀 LANJUT"
3. ✅ Tombol "🚀 LANJUT" menjadi **ENABLED** (bisa diklik)
4. ✅ Tombol akan beranimasi (pulsing) untuk menarik perhatian

**User harus:**
- **Klik tombol "🚀 LANJUT"** untuk pindah ke scene berikutnya
- **TIDAK otomatis** pindah scene!

---

### Step 6: Transisi ke Scene Berikutnya

**Setelah klik "🚀 LANJUT":**

1. Status: "🚀 Loading..."
2. Fade out animation
3. Pindah ke `Scene/Main_UI.tscn` atau `Scene/WorldEnv.tscn`

---

## 🎯 Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│  Python (login.py)                                      │
├─────────────────────────────────────────────────────────┤
│  1. Buka camera                                         │
│  2. Loop forever:                                       │
│     - Capture frame                                     │
│     - Encode JPEG                                       │
│     - Fragment into UDP packets                         │
│     - Send to Godot (127.0.0.1:5000)                   │
│     - Print status every 60 frames                      │
│  3. TIDAK ADA LOGIC LOGIN!                              │
│  4. Streaming terus sampai Ctrl+C                       │
└─────────────────────────────────────────────────────────┘
                        │
                        │ UDP packets
                        ▼
┌─────────────────────────────────────────────────────────┐
│  Godot (login.gd)                                       │
├─────────────────────────────────────────────────────────┤
│  1. User klik "CONNECT CAMERA"                          │
│     └─> Bind UDP port 5000                             │
│  2. Receive UDP packets                                 │
│     └─> Reassemble fragments                           │
│     └─> Display video (16:9)                           │
│  3. ✅ FACE DETECTION DI GODOT:                         │
│     - Analyze each frame                                │
│     - Check center region for face                      │
│     - Count frames: face_detected_frames++             │
│     - Progress: (frames / 60) * 100%                   │
│  4. When face_detected_frames >= 60:                   │
│     └─> Login success!                                 │
│     └─> Status: "Login Berhasil! Klik LOGIN"          │
│     └─> Enable "🚀 LANJUT" button                      │
│  5. User MUST click "🚀 LANJUT":                        │
│     └─> Transition animation                           │
│     └─> Change scene to Main_UI.tscn                   │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 Troubleshooting

### Python tidak streaming

**Problem:**
```
❌ Error: Tidak dapat mengakses kamera
```

**Solution:**
1. Tutup aplikasi lain yang pakai camera (Zoom, Teams, Skype)
2. Check permission camera di System Preferences
3. Test: `python test_camera.py`

---

### Godot: Video tidak muncul

**Problem:**
- Placeholder "Waiting for camera..." masih muncul
- Video tidak muncul

**Solution:**
1. ✅ Check Python sudah jalan dulu sebelum Godot
2. ✅ Pastikan klik "CONNECT CAMERA" di Godot
3. ✅ Check Godot console untuk error messages
4. ✅ Check firewall: allow port 5000
5. ✅ Test: `python test_udp_fragmentation.py`

---

### Face detection tidak jalan

**Problem:**
- Video muncul tapi tidak ada "Wajah Terdeteksi"
- Progress tetap 0%

**Kemungkinan:**
1. **Wajah tidak di tengah frame** → posisikan wajah di tengah
2. **Pencahayaan terlalu gelap/terang** → atur pencahayaan
3. **Background terlalu kompleks** → gunakan background simple
4. **Jarak terlalu dekat/jauh** → jarak ideal 30-60cm

**Debug:**
- Lihat Godot console untuk debug messages
- Check apakah `_detect_face_in_frame()` dipanggil

---

### Login button tidak enabled

**Problem:**
- Progress sudah 100% tapi button masih disabled

**Solution:**
- Ini **NORMAL** di design baru!
- Setelah 100%, button otomatis enabled dan jadi "🚀 LANJUT"
- Jika tidak: check Godot console untuk errors

---

## 📊 Technical Details

### Python (login.py)

**Fungsi utama:**
```python
def stream_video(self):
    """Stream video continuously - NO login logic!"""
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        
        # Just stream - NO face detection!
        self.send_frame_udp(frame)
```

**Tidak ada:**
- ❌ Face detection
- ❌ Progress tracking
- ❌ Login logic
- ❌ Gesture messages
- ❌ Auto-stop setelah login

**Yang ada:**
- ✅ Video capture
- ✅ JPEG encoding
- ✅ UDP fragmentation
- ✅ Continuous streaming
- ✅ Status print setiap 60 frames

---

### Godot (login.gd)

**Fungsi utama:**
```gdscript
func _detect_face_in_frame(image: Image):
    """Face detection - ALL LOGIN LOGIC HERE!"""
    
    # Sample center region pixels
    # Check for face presence
    # Update counter: face_detected_frames++
    
    if face_detected_frames >= required_frames:
        _on_login_success()
```

**Yang ada:**
- ✅ UDP packet reception
- ✅ Frame reassembly
- ✅ Video display (16:9)
- ✅ Face detection (heuristic)
- ✅ Progress tracking
- ✅ Login logic
- ✅ Button enable/disable
- ✅ Scene transition

---

## 🎨 UI Flow

### Status Messages

| Progress | Status Message | Color | Button State |
|----------|---------------|-------|--------------|
| 0% | "❌ Wajah tidak terdeteksi" | RED | Disabled |
| 1-49% | "👤 Wajah Terdeteksi: X%" | YELLOW | Disabled |
| 50-99% | "👤 Wajah Terdeteksi: X% - Hampir selesai!" | CYAN | Disabled |
| 100% | "✅ Login Berhasil! Klik LOGIN untuk lanjut." | GREEN | **ENABLED** |
| Click | "🚀 Loading..." | CYAN | Transitioning |

### Button States

| State | Text | Enabled | Action |
|-------|------|---------|--------|
| Initial | "🔐 LOGIN" | ❌ Disabled | None |
| Login Success | "🚀 LANJUT" | ✅ **ENABLED** | Pulsing animation |
| Clicked | "🚀 LANJUT" | ✅ Enabled | Proceed to next scene |

---

## 🔄 Comparison: Old vs New

| Aspect | Old (❌) | New (✅) |
|--------|---------|----------|
| **Face Detection** | Python | Godot |
| **Progress Tracking** | Python | Godot |
| **Login Logic** | Python | Godot |
| **Streaming** | Stops after login | Continuous |
| **Scene Transition** | Automatic | Manual (click button) |
| **User Control** | None | User decides when to proceed |
| **Architecture** | Mixed logic | Clean separation |

---

## ✅ Checklist Testing

- [ ] Python jalan tanpa error
- [ ] Python print "Streaming... (frame: X)" setiap 60 frames
- [ ] Godot bisa connect dengan button "CONNECT CAMERA"
- [ ] Video muncul di Godot dalam 16:9 aspect ratio
- [ ] Status update "Wajah Terdeteksi: X%" saat wajah di tengah
- [ ] Progress mencapai 100%
- [ ] Status berubah "Login Berhasil! Klik LOGIN untuk lanjut"
- [ ] Button "LOGIN" berubah jadi "🚀 LANJUT"
- [ ] Button "🚀 LANJUT" enabled dan pulsing
- [ ] Klik button → transisi → scene berikutnya
- [ ] Python masih streaming (tidak stop)

---

## 🎉 Summary

**Yang Berubah:**
1. ✅ Python = Pure video streamer (no login logic)
2. ✅ Godot = All login logic (face detection + progress + button)
3. ✅ User control = Manual click to proceed
4. ✅ Better UX = User tahu kapan login berhasil dan kapan lanjut

**Keuntungan:**
- 🎯 Separation of concerns (Python = streaming, Godot = UI logic)
- 🔄 Python bisa digunakan untuk scene lain juga
- 👤 User punya kontrol penuh
- 🎨 Better user experience
- 🐛 Easier debugging (logic terpisah)

---

**Happy Testing! 🚀**
