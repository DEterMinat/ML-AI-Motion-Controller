import mediapipe
import cv2

print(f"MediaPipe Version: {mediapipe.__version__}")
try:
    mp_pose = mediapipe.solutions.pose
    print("SUCCESS: mediapipe.solutions.pose is available")
    
    # Check if we can initialize it (requires binary components)
    pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)
    print("SUCCESS: MediaPipe Pose model initialized")
    pose.close()
    
except AttributeError:
    print("FAILURE: mediapipe.solutions has no pose attribute")
except Exception as e:
    print(f"FAILURE: Exception accessing mediapipe.solutions: {e}")

print(f"OpenCV Version: {cv2.__version__}")
