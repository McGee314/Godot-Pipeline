# 🎮 Cara Cepat: Webcam + Gesture ke Godot

## ✅ Sistem Sudah Siap!

Server Python **webcam_server_udp.py** sudah jalan di background! ✅

Output server:
```
🚀 UDP Server dimulai di localhost:8888
📺 Server berjalan! Client dapat bergabung dengan mengirim 'REGISTER'
```

---

## 🚀 Langkah Selanjutnya

### Sekarang buka GODOT:

1. **Buka Godot Engine**
2. **Load Project**: `Godot_Project/`
3. **Buka Scene**: `webcam_client_udp.tscn`
4. **Klik Play** (F5)
5. **Klik "Connect to Server"** di window Godot

### Yang Harus Muncul di Godot Console:
```
🎮 Godot UDP client initialized
📺 Webcam server: 127.0.0.1:8888
✅ Listening for gestures on UDP port: 9999
🔄 Starting UDP connection...
📤 Registration sent to server
📥 Received: REGISTERED
✅ Registration confirmed!
🎥 Ready to receive video streams!
```

### Di Python Console (terminal):
```
✅ Client terdaftar: ('127.0.0.1', xxxxx)
📊 Total clients: 1
📤 Sent frame 1: 15234 bytes in 2 packets to 1 clients
```

---

## 🖐️ Untuk Hand Gesture Control

Buka **Terminal Baru** dan jalankan:

```bash
cd mediapipe_app
source ../mediapipe_env/bin/activate
python hand_gesture_only.py
```

Gerakkan tangan di kamera:
- **Atas** → Drone maju
- **Bawah** → Drone mundur
- **Kiri** → Drone ke kiri
- **Kanan** → Drone ke kanan

---

## ❌ Jika Ada Masalah

### "Registration timeout"
- Pastikan server Python sudah jalan (sudah ✅)
- Cek console Python ada tulisan "Client terdaftar"

### Video tidak muncul
- Pastikan kamera tidak dipakai aplikasi lain
- Test dengan: `python test_camera.py`

### Gesture tidak jalan
- Jalankan `hand_gesture_only.py` di terminal terpisah
- Pastikan Godot console ada: "👋 Gesture received: UP"

---

## 📖 Dokumentasi Lengkap

Baca file `COMPLETE_SETUP_GUIDE.md` untuk troubleshooting detail!

---

## 🎯 Current Status

✅ **Webcam Server**: RUNNING (port 8888)  
⏳ **Godot Client**: Belum dijalankan  
⏳ **Hand Gesture**: Belum dijalankan  

**Next Step**: Buka Godot dan klik "Connect to Server"! 🚀
