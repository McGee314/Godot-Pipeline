#!/usr/bin/env python3
"""
Test script untuk mengecek kamera dan MediaPipe
"""

import cv2
import mediapipe as mp
import sys
import os

def test_camera_access():
    """Test akses kamera"""
    print("🔍 Testing Camera Access...")
    
    # Test multiple camera indices
    camera_indices = [0, 1, -1]
    working_cameras = []
    
    for index in camera_indices:
        print(f"   Testing camera index {index}...")
        try:
            cap = cv2.VideoCapture(index)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    print(f"   ✅ Camera {index}: Working (Resolution: {frame.shape})")
                    working_cameras.append(index)
                else:
                    print(f"   ❌ Camera {index}: Cannot read frames")
                cap.release()
            else:
                print(f"   ❌ Camera {index}: Cannot open")
        except Exception as e:
            print(f"   ❌ Camera {index}: Error - {e}")
    
    if working_cameras:
        print(f"✅ Found {len(working_cameras)} working camera(s): {working_cameras}")
        return working_cameras[0]
    else:
        print("❌ No working cameras found!")
        return None

def test_mediapipe():
    """Test MediaPipe face detection"""
    print("\n🔍 Testing MediaPipe Face Detection...")
    
    try:
        mp_face_detection = mp.solutions.face_detection
        face_detection = mp_face_detection.FaceDetection(
            model_selection=0, min_detection_confidence=0.5)
        print("✅ MediaPipe Face Detection initialized successfully")
        return True
    except Exception as e:
        print(f"❌ MediaPipe Face Detection error: {e}")
        return False

def test_mediapipe_hands():
    """Test MediaPipe hand tracking"""
    print("\n🔍 Testing MediaPipe Hand Tracking...")
    
    try:
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        print("✅ MediaPipe Hand Tracking initialized successfully")
        return True
    except Exception as e:
        print(f"❌ MediaPipe Hand Tracking error: {e}")
        return False

def test_gui_dependencies():
    """Test GUI dependencies"""
    print("\n🔍 Testing GUI Dependencies...")
    
    missing_deps = []
    
    try:
        import tkinter
        print("✅ tkinter: Available")
    except ImportError:
        print("❌ tkinter: Missing")
        missing_deps.append("tkinter")
    
    try:
        from PIL import Image, ImageTk
        print("✅ PIL (Pillow): Available")
    except ImportError:
        print("❌ PIL (Pillow): Missing")
        missing_deps.append("pillow")
    
    try:
        import numpy
        print(f"✅ numpy: Available (version {numpy.__version__})")
    except ImportError:
        print("❌ numpy: Missing")
        missing_deps.append("numpy")
    
    return len(missing_deps) == 0

def main():
    """Main test function"""
    print("🎯 MediaPipe Application Camera Test")
    print("=" * 50)
    
    # Test camera access
    camera_index = test_camera_access()
    
    # Test MediaPipe
    mp_face_ok = test_mediapipe()
    mp_hands_ok = test_mediapipe_hands()
    
    # Test GUI dependencies
    gui_deps_ok = test_gui_dependencies()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    if camera_index is not None:
        print("✅ Camera: Ready")
    else:
        print("❌ Camera: Not available")
    
    if mp_face_ok:
        print("✅ Face Detection: Ready")
    else:
        print("❌ Face Detection: Not working")
    
    if mp_hands_ok:
        print("✅ Hand Tracking: Ready")
    else:
        print("❌ Hand Tracking: Not working")
    
    if gui_deps_ok:
        print("✅ GUI Dependencies: Ready")
    else:
        print("❌ GUI Dependencies: Missing")
    
    # Overall status
    all_ok = camera_index is not None and mp_face_ok and mp_hands_ok and gui_deps_ok
    
    if all_ok:
        print("\n🎉 ALL TESTS PASSED - Application should work properly!")
    else:
        print("\n⚠️  SOME TESTS FAILED - Please fix the issues above")
        
        if camera_index is None:
            print("\n💡 Camera Tips:")
            print("   • Close other applications using the camera")
            print("   • Check camera permissions in System Preferences")
            print("   • Try restarting the computer")
            print("   • Make sure camera is properly connected")
    
    return all_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)