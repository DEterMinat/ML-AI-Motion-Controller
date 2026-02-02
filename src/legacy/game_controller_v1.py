"""
Game Controller Script
======================
Loads trained model and controls game inputs based on real-time pose predictions

Usage:
    python -m src.app.game_controller
    
    Or from project root:
    python src/app/game_controller.py
"""

import cv2
import numpy as np
import pickle
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.pose_detection import PoseDetector
from utils.input_handler import InputHandler
import config

class GameController:
    """Main game controller class"""
    
    def __init__(self):
        """Initialize game controller"""
        self.model, self.encoder = self.load_model_and_encoder()
        self.detector = PoseDetector(
            static_image_mode=config.POSE_STATIC_IMAGE_MODE,
            model_complexity=config.POSE_MODEL_COMPLEXITY,
            smooth_landmarks=config.POSE_SMOOTH_LANDMARKS,
            min_detection_confidence=config.POSE_MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=config.POSE_MIN_TRACKING_CONFIDENCE
        )
        self.input_handler = InputHandler(cooldown_duration=config.ACTION_COOLDOWN)
        
        # Statistics
        self.frame_count = 0
        self.action_count = {}
    
    def load_model_and_encoder(self):
        """Load trained model and label encoder"""
        if not os.path.exists(config.MODEL_FILE) or not os.path.exists(config.ENCODER_FILE):
            raise FileNotFoundError(
                f"❌ Error: Model files not found!\n"
                f"Please run train_model.py first to train the model.\n"
                f"Looking for:\n"
                f"  - {config.MODEL_FILE}\n"
                f"  - {config.ENCODER_FILE}"
            )
        
        with open(config.MODEL_FILE, 'rb') as f:
            model = pickle.load(f)
        
        with open(config.ENCODER_FILE, 'rb') as f:
            encoder = pickle.load(f)
        
        print(f"✓ Loaded model from {config.MODEL_FILE}")
        print(f"✓ Loaded encoder from {config.ENCODER_FILE}")
        print(f"✓ Recognized classes: {list(encoder.classes_)}")
        
        return model, encoder
    
    def predict_pose(self, landmarks):
        """
        Predict the pose class and confidence
        
        Args:
            landmarks: Extracted landmarks list
            
        Returns:
            Tuple of (predicted_label, confidence)
        """
        if landmarks is None:
            return None, 0.0
        
        # Convert to numpy array and reshape for model input
        landmarks_array = np.array(landmarks).reshape(1, -1)
        
        # Make prediction
        prediction = self.model.predict(landmarks_array)[0]
        
        # Get confidence (probability) for the predicted class
        probabilities = self.model.predict_proba(landmarks_array)[0]
        confidence = np.max(probabilities)
        
        # Decode label
        predicted_label = self.encoder.inverse_transform([prediction])[0]
        
        return predicted_label, confidence
    
    def trigger_game_action(self, predicted_label, confidence):
        """
        Trigger game actions based on prediction
        
        Args:
            predicted_label: Predicted action label
            confidence: Confidence score (0-1)
            
        Returns:
            String describing the action taken
        """
        if confidence < config.CONFIDENCE_THRESHOLD:
            return f"Low confidence ({confidence:.2f})"
        
        # Get key binding for this action
        key = config.KEY_BINDINGS.get(predicted_label)
        
        if key is None:
            return f"{predicted_label} (No key binding)"
        
        # Try to press the key
        if self.input_handler.press_key(key, action_name=predicted_label):
            # Track action count
            self.action_count[predicted_label] = self.action_count.get(predicted_label, 0) + 1
            
            # Format key display string
            key_display = key
            if key == 'click_left': key_display = 'L-Click'
            elif key == 'click_right': key_display = 'R-Click'
            elif isinstance(key, list): key_display = '+'.join(key).upper()
            
            return f"✓ {predicted_label.upper()} [{key_display}] (Conf: {confidence:.2f})"
        else:
            return f"{predicted_label} (Cooldown)"
    
    def add_overlay(self, frame, predicted_label, confidence, action_status):
        """Add informational overlay to frame"""
        # Background for better text visibility
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (640, 140), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        
        # Prediction info
        color = config.COLOR_GREEN if confidence >= config.CONFIDENCE_THRESHOLD else config.COLOR_YELLOW
        cv2.putText(frame, f"Prediction: {predicted_label}", (10, 30),
                   config.FONT, config.FONT_SCALE, color, config.FONT_THICKNESS)
        cv2.putText(frame, f"Confidence: {confidence:.2f}", (10, 65),
                   config.FONT, config.FONT_SCALE, color, config.FONT_THICKNESS)
        
        # Action status
        cv2.putText(frame, f"Action: {action_status}", (10, 100),
                   config.FONT, 0.6, config.COLOR_WHITE, 1)
        
        # Controls
        cv2.putText(frame, "Press 'q' to quit | 'r' to reset stats", (10, 130),
                   config.FONT, 0.5, config.COLOR_YELLOW, 1)
        
        # Statistics (top-right)
        y_offset = 30
        for action, count in self.action_count.items():
            text = f"{action}: {count}"
            cv2.putText(frame, text, (450, y_offset),
                       config.FONT, 0.5, config.COLOR_GREEN, 1)
            y_offset += 25
        
        return frame
    
    def run(self):
        """Main game loop"""
        print("\n" + "=" * 60)
        print("Motion Controller - Game Controller")
        print("=" * 60)
        print(f"Confidence Threshold: {config.CONFIDENCE_THRESHOLD}")
        print(f"Action Cooldown: {config.ACTION_COOLDOWN}s")
        print(f"Key Bindings: {config.KEY_BINDINGS}")
        print("\nStarting game controller...")
        print("Press 'q' to quit, 'r' to reset statistics\n")
        
        # Open webcam
        cap = cv2.VideoCapture(config.CAMERA_INDEX)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
        
        if not cap.isOpened():
            print("❌ Error: Cannot open webcam")
            return 1
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("❌ Error: Cannot read from webcam")
                    break
                
                self.frame_count += 1
                
                # Flip frame for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Run pose detection
                results = self.detector.process_frame(frame)
                
                # Extract landmarks
                landmarks = self.detector.extract_landmarks(results)
                
                # Predict pose
                predicted_label, confidence = self.predict_pose(landmarks)
                
                # Trigger game action
                action_status = "No pose detected"
                if predicted_label is not None:
                    action_status = self.trigger_game_action(predicted_label, confidence)
                
                # Draw landmarks
                frame = self.detector.draw_landmarks(frame, results,
                                                    landmark_color=config.COLOR_GREEN,
                                                    connection_color=config.COLOR_BLUE)
                
                # Add overlay
                frame = self.add_overlay(frame, predicted_label or "None", confidence, action_status)
                
                # Display frame
                cv2.imshow("Game Controller - Press 'q' to quit", frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("\n✓ Shutting down...")
                    break
                elif key == ord('r'):
                    self.action_count.clear()
                    self.input_handler.reset_cooldown()
                    print("✓ Statistics reset")
        
        finally:
            cap.release()
            cv2.destroyAllWindows()
            self.detector.close()
            
            # Print final statistics
            print("\n" + "=" * 60)
            print("Session Statistics")
            print("=" * 60)
            print(f"Total frames: {self.frame_count}")
            print(f"Actions triggered:")
            for action, count in sorted(self.action_count.items()):
                print(f"  {action}: {count}")
            print("=" * 60)
        
        return 0

def main():
    """Main entry point"""
    try:
        controller = GameController()
        return controller.run()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
