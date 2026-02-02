import sys
print(f"Python Version: {sys.version}")

try:
    import mediapipe as mp
    print(f"MediaPipe Path: {mp.__file__}")
    print(f"MediaPipe Dir: {dir(mp)}")
except ImportError as e:
    print(f"Error importing mediapipe: {e}")

try:
    import mediapipe.solutions as solutions
    print("SUCCESS: import mediapipe.solutions works")
except ImportError as e:
    print(f"FAIL: import mediapipe.solutions failed: {e}")

try:
    from mediapipe.python.solutions import pose
    print("SUCCESS: from mediapipe.python.solutions import pose works")
except ImportError as e:
    print(f"FAIL: from mediapipe.python.solutions import pose failed: {e}")

try:
    import mediapipe.python.solutions as solutions_direct
    print("SUCCESS: import mediapipe.python.solutions works")
except ImportError as e:
    print(f"FAIL: import mediapipe.python.solutions failed: {e}")
