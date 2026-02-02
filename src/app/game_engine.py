"""
Threaded Game Controller Script
===============================
Optimized version of game_controller.py using threaded camera input 
and FPS limiting for smoother performance.

Usage:
    python -m src.app.game_controller_threaded
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
from utils.input_handler import InputHandler
from utils.camera_stream import CameraStream
from utils.fps_limiter import FPSLimiter
from utils.motion_analyzer import MotionAnalyzer
from utils.ws_server import WebSocketServer
import config

class GameControllerThreaded:
    """Main game controller class (Threaded Version)"""
    
    def __init__(self):
        """Initialize game controller"""
        print("Initializing Threaded Game Controller...")
        
        self.model, self.encoder, self.scaler = self.load_model_and_encoder()
        self.detector = PoseDetector(
            static_image_mode=config.POSE_STATIC_IMAGE_MODE,
            model_complexity=config.POSE_MODEL_COMPLEXITY,
            smooth_landmarks=config.POSE_SMOOTH_LANDMARKS,
            min_detection_confidence=config.POSE_MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=config.POSE_MIN_TRACKING_CONFIDENCE
        )
        self.input_handler = InputHandler(cooldown_duration=config.ACTION_COOLDOWN)
        
        # Initialize utilities
        self.camera = CameraStream(src=config.CAMERA_INDEX, name="WebcamStream")
        self.limiter = FPSLimiter(max_fps=config.TARGET_FPS) # Limit to configured FPS
        self.analyzer = MotionAnalyzer(
            history_size=config.ANALYZER_HISTORY_SIZE,
            consistency_threshold=config.ANALYZER_CONSISTENCY_THRESHOLD
        )      # Smart Motion Analysis
        self.ws_server = WebSocketServer()    # WebSocket Broadcaster
        
        # Statistics
        self.action_count = {}
        
        # State for Velocity Calculation
        self.prev_raw_landmarks = None
        self.running = True

    # ... (load_model_and_encoder, predict_pose remain same) ...
        
    def load_model_and_encoder(self):
        """Load trained model, label encoder, and scaler"""
        required_files = [config.MODEL_FILE, config.ENCODER_FILE, config.SCALER_FILE]
        for f_path in required_files:
            if not os.path.exists(f_path):
                raise FileNotFoundError(
                    f"❌ Error: File not found: {f_path}\n"
                    f"Please run train_pro.py first to train the model."
                )
        
        with open(config.MODEL_FILE, 'rb') as f:
            model = pickle.load(f)
        
        with open(config.ENCODER_FILE, 'rb') as f:
            encoder = pickle.load(f)
            
        with open(config.SCALER_FILE, 'rb') as f:
            scaler = pickle.load(f)
            
        return model, encoder, scaler
    
    def predict_pose(self, features):
        """Predict the pose class and confidence"""
        if features is None:
            return None, 0.0
        
        # Convert to numpy array and reshape
        features_array = np.array(features).reshape(1, -1)
        
        # Scale features (Critical for Neural Network!)
        features_scaled = self.scaler.transform(features_array)
        
        # Make prediction
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        confidence = np.max(probabilities)
        
        # Decode label
        predicted_label = self.encoder.inverse_transform([prediction])[0]
        
        return predicted_label, confidence

    def trigger_action(self, confirmed_action, confidence):
        """Trigger game action"""
        # Broadcast via WebSocket
        self.ws_server.broadcast({
            "action": confirmed_action,
            "confidence": float(confidence), # Convert numpy float
            "state": "ACTION"
        })
        
        key = config.KEY_BINDINGS.get(confirmed_action)
        if not key:
            return f"{confirmed_action} (No Key)"
            
        # Special handling for Continuous Actions (Block)
        if confirmed_action == 'block':
            self.input_handler.handle_hold(key, True)
            return f"✓ BLOCKING (Hold)"
        else:
            # If doing anything else, ensure Block is released
            block_key = config.KEY_BINDINGS.get('block')
            if block_key:
                self.input_handler.handle_hold(block_key, False)
        
        # Standard Discrete Actions (Punch, Dodge)
        if self.input_handler.press_key(key, action_name=confirmed_action):
            # Update stats
            self.action_count[confirmed_action] = self.action_count.get(confirmed_action, 0) + 1
            
            # Format display
            key_display = str(key)
            if key == 'click_left': key_display = 'L-Click'
            elif key == 'click_right': key_display = 'R-Click'
            elif isinstance(key, list): key_display = '+'.join(key).upper()
            
            return f"✓ {confirmed_action.upper()} [{key_display}]"
        else:
            return f"{confirmed_action} (Cooldown)"

    def add_overlay(self, frame, raw_label, confirmed_action_status, confidence, fps_app, fps_cam):
        """Add info overlay with FPS stats"""
        # Dark overlay for text
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (640, 160), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        
        # Colors
        color_ok = config.COLOR_GREEN
        color_warn = config.COLOR_YELLOW
        
        # Left Side: Prediction & Action
        cv2.putText(frame, f"Raw AI: {raw_label} ({confidence:.2f})", (10, 30),
                   config.FONT, 0.6, color_warn, 1)
                   
        # Highlight Main Action
        cv2.putText(frame, f"Action: {confirmed_action_status}", (10, 70),
                   config.FONT, 0.7, color_ok, 2)
                   
        # Current State
        state_text = f"State: {self.analyzer.state}"
        cv2.putText(frame, state_text, (10, 100), config.FONT, 0.5, config.COLOR_WHITE, 1)
                   
        # Right Side: Performance Stats
        cv2.putText(frame, f"App FPS: {fps_app:.1f}", (450, 30),
                   config.FONT, 0.5, color_warn, 1)
        cv2.putText(frame, f"Cam FPS: {fps_cam:.1f}", (450, 50),
                   config.FONT, 0.5, color_warn, 1)
                   
        # Instructions
        cv2.putText(frame, "Q: Quit | R: Reset Stats | C: Recalibrate", (10, 140),
                   config.FONT, 0.5, config.COLOR_YELLOW, 1)
                   
        return frame

    def start(self):
        """Start camera and resources"""
        print("Starting camera stream...")
        self.camera.start()
        self.ws_server.start() # Start WebSocket
        time.sleep(1.0) # Warmup
        print("✓ System Ready!")
        
    def stop(self):
        """Stop camera and resources"""
        self.running = False
        print("Cleaning up resources...")
        self.camera.stop()
        self.ws_server.stop() # Stop WebSocket
        try:
            self.detector.close()
        except:
            pass # Ignore errors during shutdown
        print("✓ Shutdown complete")

    def process_frame(self):
        """
        Process a single frame (logic only).
        Returns:
            processed_frame: The frame with overlays
            status_data: Dict containing current status/stats for GUI
        """
        # 1. Get latest frame
        if not self.running: return None, None

        frame = self.camera.read()
        if frame is None:
            return None, None
            
        frame = cv2.flip(frame, 1)
        
        # 2. Pose Detection
        try:
            results = self.detector.process_frame(frame)
        except Exception as e:
            # If MediaPipe crashes (e.g. during shutdown), return safely
            # print(f"Frame Process Error: {e}")
            return frame, None

        raw_landmarks = self.detector.extract_landmarks(results)
        
        # 3. Prediction & Input
        predicted_label, confidence = None, 0.0
        
        if raw_landmarks:
            # Compute features using CURRENT + PREVIOUS landmarks (Velocity)
            features = self.detector.compute_features(raw_landmarks, self.prev_raw_landmarks)
            
            # Update history for next frame
            self.prev_raw_landmarks = raw_landmarks
            
            if features:
                predicted_label, confidence = self.predict_pose(features)
        else:
            # Lost tracking -> Reset velocity history
            self.prev_raw_landmarks = None
        
        # Smart AI Analysis
        confirmed_action, is_consistent = self.analyzer.process_prediction(predicted_label, confidence)
        
        action_status = "-"
        if confirmed_action:
            if confidence >= config.CONFIDENCE_THRESHOLD:
                action_status = self.trigger_action(confirmed_action, confidence)
            else:
                action_status = "Low Confidence"
                
        # 4. Visualization (Draw landmarks)
        self.detector.draw_landmarks(frame, results, 
                                   landmark_color=config.COLOR_GREEN, 
                                   connection_color=config.COLOR_BLUE)
        
        # Overlay for Opencv Window (Legacy support)
        # For GUI app, we might want clean frame, but let's keep it consistent for now
        frame = self.add_overlay(frame, 
                               predicted_label or "None", 
                               action_status, 
                               confidence,
                               self.limiter.get_fps(),
                               self.camera.get_fps())
                               
        self.limiter.tick()
        
        # Return data for GUI
        status_data = {
            "fps_app": self.limiter.get_fps(),
            "fps_cam": self.camera.get_fps(),
            "prediction": predicted_label,
            "confidence": confidence,
            "action": confirmed_action,
            "state": self.analyzer.state
        }
        
        return frame, status_data

    def run(self):
        """Main threaded game loop (Legacy/Headless mode)"""
        print("\n" + "=" * 60)
        print("🥊 Motion Controller - Threaded High-Performance Mode")
        print("=" * 60)
        
        self.start()
        
        try:
            while True:
                frame, _ = self.process_frame()
                
                if frame is not None:
                    cv2.imshow("Threaded Game Controller", frame)
                
                # Input Handling
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('r'):
                    self.action_count.clear()
                    self.input_handler.reset_cooldown()
                    self.analyzer.reset()
                    print("✓ Statistics reset")
                elif key == ord('c'):
                    self.analyzer.reset()
                    print("✓ Recalibrated")
                    
        except KeyboardInterrupt:
            print("\nStopping...")
            
        finally:
            self.stop()
            cv2.destroyAllWindows()
            return 0

def main():
    try:
        controller = GameControllerThreaded()
        return controller.run()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
