"""
Pose Detection Utility
======================
Handles MediaPipe pose detection and landmark extraction
"""

import cv2
import mediapipe.python.solutions as mp_solutions

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

    def compute_features(self, raw_landmarks, prev_landmarks=None):
        """
        Convert RAW landmarks (132) to SMART features (72) for Model.
        - Upper Body Only (11-24)
        - Normalizes to mid-hip
        - Adds Upper Body Angles
        - Adds Velocity (if prev_landmarks exists)
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
        
        # 2. Normalization
        mid_hip = (left_hip + right_hip) / 2
        torso_size = np.linalg.norm(left_shoulder - right_shoulder)
        if torso_size < 0.01: torso_size = 1.0
        
        features = []
        
        # A. Body Coords (11-24 ONLY)
        for i in range(11, 25):
            coords = get_coords(raw_landmarks, i)
            rel_coords = (coords - mid_hip) / torso_size
            features.extend(rel_coords.tolist())
            features.append(get_vis(raw_landmarks, i))
            
        # B. Upper Body Angles
        def calc_angle(a, b, c):
            ba = a - b; bc = c - b
            cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
            angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
            return np.degrees(angle) / 180.0
            
        l_elbow = get_coords(raw_landmarks, 13); l_wrist = get_coords(raw_landmarks, 15)
        r_elbow = get_coords(raw_landmarks, 14); r_wrist = get_coords(raw_landmarks, 16)
        
        # 1. Elbow Angles
        features.append(calc_angle(left_shoulder, l_elbow, l_wrist))
        features.append(calc_angle(right_shoulder, r_elbow, r_wrist))
        
        # 2. Shoulder Angles
        features.append(calc_angle(left_hip, left_shoulder, l_elbow))
        features.append(calc_angle(right_hip, right_shoulder, r_elbow))
        
        # C. Velocity (Delta)
        # Key Points: Elbows (13,14), Wrists (15,16) -> 4 points * 3 coords = 12 features
        velocity_points = [13, 14, 15, 16] 
        
        if prev_landmarks:
            for i in velocity_points:
                curr = get_coords(raw_landmarks, i)
                prev = get_coords(prev_landmarks, i)
                # Calculate Delta
                delta = (curr - prev) * 5.0 # Scale up for better sensitivity
                features.extend(delta.tolist())
        else:
            # First frame or no history -> Zero velocity
            features.extend([0.0] * 12)
        
        return features
    
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
        """
        Draw pose landmarks on frame
        
        Args:
            frame: BGR image from OpenCV
            results: MediaPipe Pose detection results
            landmark_color: RGB color tuple for landmarks
            connection_color: RGB color tuple for connections
            
        Returns:
            Frame with landmarks drawn
        """
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                self.mp_drawing.DrawingSpec(color=landmark_color, thickness=2, circle_radius=2),
                self.mp_drawing.DrawingSpec(color=connection_color, thickness=2)
            )
        return frame
    
    def close(self):
        """Release MediaPipe resources"""
        self.pose.close()
