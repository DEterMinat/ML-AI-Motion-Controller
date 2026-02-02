"""
Video Validation Script
=======================
Validates model accuracy using a pre-recorded video file.
This allows for consistent testing of specific actions.

Usage:
    python src/validate_with_video.py
"""

import cv2
import numpy as np
import pickle
import os
import sys
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.pose_detection import PoseDetector
import config

class VideoValidator:
    def __init__(self):
        self.model, self.encoder = self.load_model_and_encoder()
        self.detector = PoseDetector(
            static_image_mode=False,
            model_complexity=config.POSE_MODEL_COMPLEXITY,
            smooth_landmarks=config.POSE_SMOOTH_LANDMARKS,
            min_detection_confidence=config.POSE_MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=config.POSE_MIN_TRACKING_CONFIDENCE
        )
        self.valid_labels = list(self.encoder.classes_)

    def load_model_and_encoder(self):
        if not os.path.exists(config.MODEL_FILE) or not os.path.exists(config.ENCODER_FILE):
            print("❌ Error: Model files not found! Please run train_model.py first.")
            sys.exit(1)
            
        with open(config.MODEL_FILE, 'rb') as f:
            model = pickle.load(f)
        with open(config.ENCODER_FILE, 'rb') as f:
            encoder = pickle.load(f)
        return model, encoder

    def predict_frame(self, landmarks):
        if not landmarks:
            return None, 0.0
            
        # Convert to numpy array and reshape
        landmarks_array = np.array(landmarks).reshape(1, -1)
        
        # Predict
        prediction = self.model.predict(landmarks_array)[0]
        probabilities = self.model.predict_proba(landmarks_array)[0]
        confidence = np.max(probabilities)
        
        predicted_label = self.encoder.inverse_transform([prediction])[0]
        return predicted_label, confidence

    def run(self):
        print("=" * 60)
        print("Motion Controller - Video Validation Tool")
        print("=" * 60)
        
        # 1. Get Video Path
        while True:
            video_path = input("\nEnter path to video file (e.g., test_punch.mp4): ").strip()
            # Remove quotes if user dragged and dropped file
            video_path = video_path.strip('"').strip("'")
            
            if os.path.exists(video_path):
                break
            print(f"❌ File not found: {video_path}")

        # 2. Get Expected Label
        print("\nAvailable Labels:")
        for i, label in enumerate(self.valid_labels):
            print(f"  {i+1}. {label}")
            
        while True:
            try:
                choice = input("\nSelect the expected action in this video (number or name): ").strip()
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(self.valid_labels):
                        expected_label = self.valid_labels[idx]
                        break
                elif choice in self.valid_labels:
                    expected_label = choice
                    break
            except:
                pass
            print("❌ Invalid selection. Please try again.")

        print(f"\nStarting validation for '{expected_label}' on '{os.path.basename(video_path)}'...")
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("❌ Error opening video file.")
            return

        total_frames = 0
        detected_frames = 0
        correct_predictions = 0
        high_conf_correct = 0
        
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                break
                
            total_frames += 1
            
            # Process frame
            image, landmarks = self.detector.find_pose(image, draw=True)
            
            status_text = "No Pose"
            status_color = config.COLOR_YELLOW
            
            if landmarks:
                detected_frames += 1
                predicted_label, confidence = self.predict_frame(landmarks)
                
                is_correct = (predicted_label == expected_label)
                
                if is_correct:
                    correct_predictions += 1
                    if confidence >= config.CONFIDENCE_THRESHOLD:
                        high_conf_correct += 1
                    status_text = f"CORRECT: {predicted_label} ({confidence:.2f})"
                    status_color = config.COLOR_GREEN
                else:
                    status_text = f"WRONG: {predicted_label} ({confidence:.2f})"
                    status_color = config.COLOR_RED
            
            # Draw UI
            cv2.putText(image, f"Expected: {expected_label}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, config.COLOR_WHITE, 2)
            cv2.putText(image, status_text, (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)
            
            # Show stats on screen
            if detected_frames > 0:
                acc = (correct_predictions / detected_frames) * 100
                cv2.putText(image, f"Accuracy: {acc:.1f}%", (10, 110), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, config.COLOR_WHITE, 2)

            cv2.imshow('Video Validation', image)
            
            # Press 'q' to quit, 'p' to pause
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('p'):
                cv2.waitKey(0)

        cap.release()
        cv2.destroyAllWindows()
        
        # Final Report
        print("\n" + "=" * 60)
        print("Validation Results")
        print("=" * 60)
        print(f"Video: {os.path.basename(video_path)}")
        print(f"Expected Action: {expected_label}")
        print("-" * 30)
        print(f"Total Frames: {total_frames}")
        print(f"Frames with Pose: {detected_frames} ({(detected_frames/total_frames*100 if total_frames else 0):.1f}%)")
        print("-" * 30)
        
        if detected_frames > 0:
            raw_acc = (correct_predictions / detected_frames) * 100
            conf_acc = (high_conf_correct / detected_frames) * 100
            
            print(f"Raw Accuracy (Any Confidence): {raw_acc:.2f}%")
            print(f"High Confidence Accuracy (>{config.CONFIDENCE_THRESHOLD}): {conf_acc:.2f}%")
            
            if raw_acc < 50:
                print("\n⚠ Low Accuracy Detected!")
                print("Suggestions:")
                print("1. Check if the video lighting matches training data.")
                print("2. Ensure the full body/upper body is visible.")
                print("3. Consider collecting more training data for this action.")
        else:
            print("⚠ No poses detected in the video!")

if __name__ == "__main__":
    validator = VideoValidator()
    validator.run()
