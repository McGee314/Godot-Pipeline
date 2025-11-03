# 🎮 Testing Gesture Control - Checklist

## ✅ Status Saat Ini

✅ **Webcam Server**: RUNNING (port 8888)  
✅ **Hand Gesture Tracker**: RUNNING (port 9999)  
✅ **Video Feed**: Sudah masuk ke Godot  
⏳ **Gesture Control**: Testing...

---

## 🖐️ Cara Test Gesture

### 1. Cek Python Console (hand_gesture_only.py)
Harus ada output seperti:
```
👋 DOWN
👋 UP
👋 LEFT
👋 RIGHT
```

**Jika TIDAK ADA gesture terdeteksi:**
- Gerakkan tangan lebih jelas ke atas/bawah/kiri/kanan
- Pastikan tangan terlihat jelas di kamera
- Jarak ideal: 30-60cm dari kamera

---

### 2. Cek Godot Console
Harus ada output:
```
✅ Listening for gestures on UDP port: 9999
✅ Auto-detected controlled object: Sketchfab_Scene
👋 Gesture received: DOWN
👋 Gesture received: UP
```

**Jika TIDAK ADA "Gesture received":**
- Restart Godot scene (tekan F5 lagi)
- Pastikan port 9999 tidak blocked firewall

**Jika "No 3D object found":**
- Buka scene `WorldEnv.tscn` yang punya drone
- Atau manual assign di Inspector: `Controlled Object` → pilih Sketchfab_Scene

---

### 3. Test Gerakan Drone

| Posisi Tangan | Python Output | Godot Output | Gerakan Drone |
|--------------|---------------|--------------|---------------|
| 🖐️ Atas layar | `👋 UP` | `👋 Gesture received: UP` | Maju ke depan |
| 🖐️ Bawah layar | `👋 DOWN` | `👋 Gesture received: DOWN` | Mundur |
| 🖐️ Kiri layar | `👋 LEFT` | `👋 Gesture received: LEFT` | Geser kiri |
| 🖐️ Kanan layar | `👋 RIGHT` | `👋 Gesture received: RIGHT` | Geser kanan |
| 🖐️ Tengah | `CENTER` | - | Berhenti |

---

## 🐛 Troubleshooting

### Drone TIDAK bergerak padahal gesture terdeteksi

**Check 1: Controlled Object**
```
# Di Godot Console, harus ada:
✅ Auto-detected controlled object: Sketchfab_Scene

# Jika TIDAK ada, berarti drone tidak terdeteksi
```

**Solusi:**
1. Di Godot, pilih node `WebcamClient` di Scene Tree
2. Di Inspector, cari property `Controlled Object`
3. Drag node `Sketchfab_Scene` dari scene tree ke property tersebut
4. Restart scene (F5)

**Check 2: Move Speed terlalu kecil**
```
# Di Inspector, cek:
Move Speed: 5.0  (jika terlalu kecil, naikkan jadi 10.0 atau 20.0)
```

**Check 3: Smooth Movement**
```
# Di Inspector:
Smooth Movement: true (coba ganti jadi false untuk step movement)
```

---

### Gesture terdeteksi tapi responsnya lambat

**Solusi:**
1. Turunkan JPEG quality di `webcam_server_udp.py`:
   ```python
   encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 30]  # Turunkan dari 40 ke 30
   ```

2. Naikkan `Movement Scale` di Godot Inspector:
   ```
   Movement Scale: 2.0  (untuk gerakan lebih cepat)
   ```

---

### Window OpenCV tidak muncul

**Solusi:**
```bash
# Check apakah proses running:
ps aux | grep hand_gesture_only

# Jika tidak ada, restart:
cd mediapipe_app
source ../mediapipe_env/bin/activate
python hand_gesture_only.py
```

---

## 📊 Expected Performance

- **FPS**: 25-30 FPS (video streaming)
- **Gesture Latency**: <100ms (sangat responsif)
- **Drop Rate**: <5% (frame drops)
- **Data Rate**: 100-200 KB/s

---

## 🎯 Final Check

Centang semua ini:

- [ ] Python server running (webcam_server_udp.py)
- [ ] Hand gesture tracker running (hand_gesture_only.py)
- [ ] Godot scene loaded dan connected
- [ ] Video feed terlihat di Godot
- [ ] Gesture terdeteksi di Python console (`👋 UP`, `👋 DOWN`, etc)
- [ ] Gesture diterima di Godot console (`👋 Gesture received: UP`)
- [ ] Drone bergerak sesuai gesture
- [ ] Status bar Godot menampilkan gesture aktif (`🖐️ UP`)

**Jika semua ✅, SISTEM SUKSES!** 🎉

---

## 🎮 Tips Kontrol

1. **Gerakan pelan**: Smooth movement, bagus untuk navigasi presisi
2. **Gerakan cepat**: Gerakkan tangan lebih jauh dari tengah untuk speed boost
3. **Berhenti**: Kembalikan tangan ke tengah layar
4. **Reset posisi**: Tekan F5 di Godot untuk reset drone ke posisi awal

---

## 📝 Next Steps

Setelah berhasil, Anda bisa:
- Tambah gesture baru (contoh: tangan tertutup = stop)
- Tambah rotasi drone dengan gesture lain
- Buat obstacle course di Godot world
- Tambah multiple objects yang bisa dikontrol
- Record gameplay dengan gesture control

Dokumentasi lengkap: `COMPLETE_SETUP_GUIDE.md`
