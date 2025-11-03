#!/usr/bin/env python3
"""
Test script untuk memverifikasi UDP gesture sender
Jalankan script ini untuk test apakah gesture UDP bekerja
"""

import socket
import json
import time
import sys

def test_udp_gesture_sender():
    """Test mengirim gesture ke Godot via UDP"""
    
    host = '127.0.0.1'
    port = 9999
    
    print("🧪 UDP Gesture Sender Test")
    print("=" * 50)
    print(f"Target: {host}:{port}")
    print()
    
    try:
        # Create UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1.0)
        print("✅ UDP socket created")
        
        # Test gestures
        test_gestures = ["UP", "DOWN", "LEFT", "RIGHT", "CENTER"]
        
        print("\n📤 Sending test gestures...")
        print("Pastikan Godot sudah running dan listening di port 9999\n")
        
        for i, gesture in enumerate(test_gestures, 1):
            # Create message
            message = {
                "type": "gesture",
                "gesture": gesture,
                "timestamp": time.time()
            }
            
            # Send message
            data = json.dumps(message).encode('utf-8')
            sock.sendto(data, (host, port))
            
            print(f"{i}. Sent: {gesture}")
            time.sleep(1)  # Wait 1 second between gestures
        
        print("\n✅ Test selesai!")
        print("\nJika Godot berjalan, objek seharusnya bergerak:")
        print("  • UP → Forward")
        print("  • DOWN → Backward")
        print("  • LEFT → Ke kiri")
        print("  • RIGHT → Ke kanan")
        print("  • CENTER → Berhenti")
        
        sock.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Pastikan Godot sudah running")
        print("2. Pastikan port 9999 tidak dipakai aplikasi lain")
        print("3. Check firewall settings")
        return False

def test_udp_receiver():
    """Test menerima gesture (untuk debug)"""
    
    port = 9999
    
    print("🧪 UDP Gesture Receiver Test")
    print("=" * 50)
    print(f"Listening on port: {port}")
    print("Jalankan MediaPipe app dan gerakkan tangan...")
    print("Press Ctrl+C to stop\n")
    
    try:
        # Create UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', port))
        sock.settimeout(1.0)
        print("✅ Listening for gestures...")
        
        gesture_count = {}
        
        while True:
            try:
                data, addr = sock.recvfrom(1024)
                message = data.decode('utf-8')
                
                # Parse JSON
                try:
                    obj = json.loads(message)
                    if obj.get("type") == "gesture":
                        gesture = obj.get("gesture")
                        
                        # Count gestures
                        gesture_count[gesture] = gesture_count.get(gesture, 0) + 1
                        
                        print(f"📥 Received: {gesture} (count: {gesture_count[gesture]})")
                        
                except json.JSONDecodeError:
                    print(f"⚠️ Invalid JSON: {message}")
                    
            except socket.timeout:
                continue
                
    except KeyboardInterrupt:
        print("\n\n📊 Gesture Statistics:")
        for gesture, count in sorted(gesture_count.items()):
            print(f"  {gesture}: {count}")
        print("\n✅ Test stopped")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        
    finally:
        sock.close()

if __name__ == "__main__":
    print("=" * 50)
    print("  UDP Gesture Communication Test")
    print("=" * 50)
    print()
    print("Pilih test mode:")
    print("1. Sender Test (kirim gesture ke Godot)")
    print("2. Receiver Test (terima gesture dari Python)")
    print()
    
    try:
        choice = input("Pilih (1/2): ").strip()
        
        if choice == "1":
            test_udp_gesture_sender()
        elif choice == "2":
            test_udp_receiver()
        else:
            print("❌ Pilihan tidak valid")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n👋 Test dibatalkan")
        sys.exit(0)
