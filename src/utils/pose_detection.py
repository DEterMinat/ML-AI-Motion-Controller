"""
Pose Detection Utility
======================
Handles MediaPipe pose detection and landmark extraction
"""

import cv2

# Handle different MediaPipe installation states
try:
    import mediapipe.solutions as mp_solutions
except ImportError:
    try:
        import mediapipe as mp
        mp_solutions = mp.solutions
    except ImportError:
        raise ImportError(
            "MediaPipe not found. Please install with: pip install mediapipe"
        )

class PoseDetector:
    """MediaPipe Pose detection wrapper"""
    
    def __init__(self, 
                 static_image_mode=False,
                 model_complexity=1,
                 smooth_landmarks=True,
                 min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):
        """
        Initialize MediaPipe Pose detector
        """
        self.mp_pose = mp_solutions.pose
        self.mp_drawing = mp_solutions.drawing_utils
        self.mp_drawing_styles = mp_solutions.drawing_styles
        
        self.pose = self.mp_pose.Pose(
            static_image_mode=static_image_mode,
            model_complexity=model_complexity,
            smooth_landmarks=smooth_landmarks,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
    
    def process_frame(self, frame):
        """
        Process a frame and detect pose landmarks
        
        Args:
            frame: BGR image from OpenCV
            
        Returns:
            MediaPipe pose detection results
        """
        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(frame_rgb)
        return results
    
    def extract_landmarks(self, results):
        """
        Extract RAW landmarks from MediaPipe results (33 points)
        Used for Data Collection and intermediate storage.
        
        Args:
            results: MediaPipe Pose detection results
            
        Returns:
            List of 132 floats (33 landmarks * 4 features) or None
        """
        if results.pose_landmarks is None:
            return None
        
        landmarks_data = []
        for landmark in results.pose_landmarks.landmark:
            landmarks_data.extend([landmark.x, landmark.y, landmark.z, landmark.visibility])
        
        return landmarks_data

    def compute_features(self, raw_landmarks, prev_landmarks=None, prev_velocity=None):
        """
        Convert RAW landmarks (132) to PRO features (108) for Model.
        
        Features breakdown:
        - A. Body Coords (14 points * 4) = 56
        - B. Angles (4) = 4
        - C. Velocity (4 points * 3) = 12
        - D. Bone Vectors (6 bones * 3) = 18 [NEW]
        - E. Acceleration (4 points * 3) = 12 [NEW]
        - F. Distance Features (6) = 6 [NEW]
        Total = 108 features
        """
        import numpy as np
        
        if not raw_landmarks or len(raw_landmarks) != 132:
            return None
            
        # Helper to get array [x, y, z]
        def get_coords(data, i):
            idx = i * 4
            return np.array(data[idx:idx+3])
        
        # Helper to get visibility
        def get_vis(data, i):
            return data[i*4 + 3]
            
        # 1. Key Joints
        left_shoulder = get_coords(raw_landmarks, 11)
        right_shoulder = get_coords(raw_landmarks, 12)
        left_hip = get_coords(raw_landmarks, 23)
        right_hip = get_coords(raw_landmarks, 24)
        l_elbow = get_coords(raw_landmarks, 13)
        r_elbow = get_coords(raw_landmarks, 14)
        l_wrist = get_coords(raw_landmarks, 15)
        r_wrist = get_coords(raw_landmarks, 16)
        
        # 2. Normalization
        mid_hip = (left_hip + right_hip) / 2
        mid_shoulder = (left_shoulder + right_shoulder) / 2
        torso_size = np.linalg.norm(left_shoulder - right_shoulder)
        if torso_size < 0.01: torso_size = 1.0
        
        features = []
        
        # ===== A. Body Coords (11-24 ONLY) = 56 features =====
        for i in range(11, 25):
            coords = get_coords(raw_landmarks, i)
            rel_coords = (coords - mid_hip) / torso_size
            features.extend(rel_coords.tolist())
            features.append(get_vis(raw_landmarks, i))
            
        # ===== B. Upper Body Angles = 4 features =====
        def calc_angle(a, b, c):
            ba = a - b; bc = c - b
            cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
            angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
            return np.degrees(angle) / 180.0
        
        features.append(calc_angle(left_shoulder, l_elbow, l_wrist))  # Left elbow angle
        features.append(calc_angle(right_shoulder, r_elbow, r_wrist)) # Right elbow angle
        features.append(calc_angle(left_hip, left_shoulder, l_elbow)) # Left shoulder angle
        features.append(calc_angle(right_hip, right_shoulder, r_elbow)) # Right shoulder angle
        
        # ===== C. Velocity (Delta) = 12 features =====
        velocity_points = [13, 14, 15, 16]  # Elbows, Wrists
        current_velocity = []
        
        if prev_landmarks:
            for i in velocity_points:
                curr = get_coords(raw_landmarks, i)
                prev = get_coords(prev_landmarks, i)
                delta = (curr - prev) * 5.0  # Scale for sensitivity
                current_velocity.extend(delta.tolist())
                features.extend(delta.tolist())
        else:
            current_velocity = [0.0] * 12
            features.extend([0.0] * 12)
        
        # ===== D. Bone Vectors (NEW) = 18 features =====
        # Direction vectors of arm bones (normalized)
        def bone_vector(start, end):
            vec = end - start
            norm = np.linalg.norm(vec)
            if norm < 1e-6: return [0.0, 0.0, 0.0]
            return (vec / norm).tolist()
        
        # Left arm bones
        features.extend(bone_vector(left_shoulder, l_elbow))   # Left upper arm
        features.extend(bone_vector(l_elbow, l_wrist))         # Left forearm
        # Right arm bones
        features.extend(bone_vector(right_shoulder, r_elbow))  # Right upper arm
        features.extend(bone_vector(r_elbow, r_wrist))         # Right forearm
        # Shoulder line
        features.extend(bone_vector(left_shoulder, right_shoulder))  # Shoulder direction
        # Torso direction
        features.extend(bone_vector(mid_hip, mid_shoulder))    # Torso vertical
        
        # ===== E. Acceleration (NEW) = 12 features =====
        # Rate of change of velocity (requires prev_velocity)
        if prev_velocity and len(prev_velocity) == 12:
            for i in range(12):
                accel = (current_velocity[i] - prev_velocity[i]) * 2.0
                features.append(accel)
        else:
            features.extend([0.0] * 12)
        
        # ===== F. Distance Features (NEW) = 6 features =====
        # Key distance ratios (normalized by torso_size)
        features.append(np.linalg.norm(l_wrist - left_shoulder) / torso_size)   # L wrist reach
        features.append(np.linalg.norm(r_wrist - right_shoulder) / torso_size)  # R wrist reach
        features.append(np.linalg.norm(l_wrist - mid_hip) / torso_size)         # L wrist to hip
        features.append(np.linalg.norm(r_wrist - mid_hip) / torso_size)         # R wrist to hip
        features.append(np.linalg.norm(l_wrist - r_wrist) / torso_size)         # Wrist separation
        features.append(np.linalg.norm(l_elbow - r_elbow) / torso_size)         # Elbow separation
        
        return features, current_velocity
    
    def draw_landmarks(self, frame, results, 
                      landmark_color=(0, 255, 0), 
                      connection_color=(255, 0, 0)):
        """Draws Upper Body landmarks only (11-16: Shoulders & Arms) - No Hips"""
        if results.pose_landmarks:
            import cv2
            h, w, c = frame.shape
            landmarks = results.pose_landmarks.landmark
            
            # Draw Points (11-16 Only: Shoulders, Elbows, Wrists)
            for i in range(11, 17):
                lm = landmarks[i]
                if lm.visibility < 0.5: continue
                
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(frame, (cx, cy), 5, landmark_color, -1)
                
            # Draw Connections (Arms Only)
            body_connections = [
                (11,12),           # Shoulder Line
                (11,13), (13,15),  # Left Arm
                (12,14), (14,16)   # Right Arm
            ]
            
            for start_idx, end_idx in body_connections:
                lm1 = landmarks[start_idx]
                lm2 = landmarks[end_idx]
                
                if lm1.visibility < 0.5 or lm2.visibility < 0.5: continue
                
                x1, y1 = int(lm1.x * w), int(lm1.y * h)
                x2, y2 = int(lm2.x * w), int(lm2.y * h)
                
                cv2.line(frame, (x1, y1), (x2, y2), connection_color, 2)
                
        return frame

    
    def close(self):
        """Release MediaPipe resources"""
        self.pose.close()
