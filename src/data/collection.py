"""
Data Collection Script
======================
Collects pose landmarks from webcam using MediaPipe and saves to CSV

Usage:
    python -m src.data_collector
    
    Or from project root:
    python src/data_collector.py
"""

import cv2
import csv
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.pose_detection import PoseDetector
import config

def get_class_file_path(label):
    """Get the CSV file path for a specific label"""
    # Sanitize label for filename
    safe_name = "".join([c for c in label if c.isalnum() or c in ('_', '-')])
    return os.path.join(config.DATASET_DIR, "by_class", f"{safe_name}.csv")

def initialize_csv_for_label(label):
    """Initialize CSV file for a specific label if needed"""
    file_path = get_class_file_path(label)
    directory = os.path.dirname(file_path)
    
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            # Create headers for landmarks + label
            headers = []
            for i in range(config.NUM_LANDMARKS):
                headers.extend([f'landmark_{i}_x', f'landmark_{i}_y', 
                               f'landmark_{i}_z', f'landmark_{i}_visibility'])
            headers.append('label')
            writer.writerow(headers)

def save_frame_to_csv(landmarks, label):
    """Save landmarks and label to class-specific CSV file"""
    if landmarks is None:
        print("⚠ No pose detected in frame. Skipping save.")
        return False
    
    # Ensure file exists with headers
    initialize_csv_for_label(label)
    file_path = get_class_file_path(label)
    
    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(landmarks + [label])
    
    print(f"✓ Saved frame to {os.path.basename(file_path)}")
    return True

def draw_hud_box(frame, x, y, w, h, color=(0, 0, 0), alpha=0.5):
    """Draw a semi-transparent box"""
    overlay = frame.copy()
    cv2.rectangle(overlay, (x, y), (x + w, y + h), color, -1)
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    return frame

def add_text_overlay(frame, label, saved_count, is_recording, burst_progress, burst_target):
    """Add modern HUD information to the frame"""
    h, w, c = frame.shape
    
    # 1. Top-Left Status Panel (HUD)
    panel_w = 320
    panel_h = 130
    draw_hud_box(frame, 10, 10, panel_w, panel_h, (0, 0, 0), 0.6)
    
    # Status Colors
    color_status = (0, 0, 255) if is_recording else (0, 255, 255) # Red vs Yellow
    status_text = "● RECORDING" if is_recording else "STANDBY"
    
    # Text Layout
    # Label
    cv2.putText(frame, f"ACTION: {label.upper()}", (25, 45), 
                config.FONT, 0.7, (255, 255, 255), 2)
    
    # Status
    cv2.putText(frame, status_text, (25, 80), 
                config.FONT, 0.8, color_status, 2)
    
    # Saved Count
    cv2.putText(frame, f"Saved: {saved_count}", (200, 80), 
                config.FONT, 0.6, (200, 200, 200), 1)

    # Progress Bar (Dynamic)
    bar_x, bar_y, bar_w, bar_h = 25, 100, 290, 15
    # Draw Background
    cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h), (50, 50, 50), -1)
    
    if is_recording:
        progress = min(burst_progress / burst_target, 1.0)
        fill_w = int(progress * bar_w)
        # Draw Fill
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + fill_w, bar_y + bar_h), color_status, -1)
        # Draw Text
        cv2.putText(frame, f"{burst_progress}/{burst_target}", (bar_x + 10, bar_y + 11), 
                    config.FONT, 0.4, (255, 255, 255), 1)
    else:
        cv2.putText(frame, "Press 'R' to Record", (bar_x + 80, bar_y + 11), 
                    config.FONT, 0.4, (150, 150, 150), 1)

    # 2. Bottom Help Panel
    help_text = f"[R] Record  [N] Next  [S] Burst: {burst_target}  [Q] Quit"
    start_x = 10
    start_y = h - 20
    
    # Simple shadow for readability without box
    cv2.putText(frame, help_text, (start_x+1, start_y+1), config.FONT, 0.6, (0,0,0), 3)
    cv2.putText(frame, help_text, (start_x, start_y), config.FONT, 0.6, (0, 255, 0), 2)
    
    return frame

def main():
    """Main data collection loop"""
    print("=" * 60)
    print("Motion Controller - Data Collection Script (Auto-Burst Mode)")
    print("=" * 60)
    
    # Ensure output directory exists
    output_dir = os.path.join(config.DATASET_DIR, "by_class")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Initialize pose detector
    detector = PoseDetector(
        static_image_mode=config.POSE_STATIC_IMAGE_MODE,
        model_complexity=config.POSE_MODEL_COMPLEXITY,
        smooth_landmarks=config.POSE_SMOOTH_LANDMARKS,
        min_detection_confidence=config.POSE_MIN_DETECTION_CONFIDENCE,
        min_tracking_confidence=config.POSE_MIN_TRACKING_CONFIDENCE
    )
    
    # Open webcam
    print("⏳ Opening webcam...")
    cap = cv2.VideoCapture(config.CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, config.TARGET_FPS)
    
    if not cap.isOpened():
        print("❌ Error: Cannot open webcam")
        return
    
    # Setup labels
    available_labels = config.DEFAULT_ACTIONS
    current_label_idx = 0
    label = available_labels[current_label_idx]
    saved_count = 0
    
    # Burst Options
    burst_index = config.DEFAULT_BURST_INDEX
    
    # Auto-Recording State
    is_recording = False
    burst_count = 0
    
    print(f"✓ Webcam opened! Default label: '{label}'")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Flip frame
            frame = cv2.flip(frame, 1)
            
            # Run pose detection
            results = detector.process_frame(frame)
            
            # Draw landmarks
            frame = detector.draw_landmarks(frame, results, 
                                           landmark_color=config.COLOR_GREEN,
                                           connection_color=config.COLOR_RED)
            
            # Current Burst Target
            current_burst_target = config.BURST_OPTIONS[burst_index]
            
            # Auto-Save Logic
            if is_recording:
                landmarks = detector.extract_landmarks(results)
                if landmarks:
                    if save_frame_to_csv(landmarks, label):
                        saved_count += 1
                        burst_count += 1
                        
                    # Stop condition
                    if burst_count >= current_burst_target:
                        is_recording = False
                        print(f"✅ Burst Complete! Collected {burst_count} samples for '{label}'.")
                        burst_count = 0 
                else:
                    # Optional: Visual warning if pose lost during recording
                    cv2.putText(frame, "POSE LOST", (200, 240), config.FONT, 1.0, config.COLOR_BLUE, 2)
            
            # Add Overlay
            frame = add_text_overlay(frame, label, saved_count, is_recording, burst_count, current_burst_target)
            
            # Display frame
            cv2.imshow("Data Collector", frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('r'):
                # Toggle Recording
                if not is_recording:
                    is_recording = True
                    burst_count = 0
                    print(f"🔴 Started Recording: {label}...")
                else:
                    is_recording = False
                    print("Ref stopped manually.")
                    
            elif key == ord('s'):
                # Cycle Burst size
                burst_index = (burst_index + 1) % len(config.BURST_OPTIONS)
                print(f"➜ Burst size set to: {config.BURST_OPTIONS[burst_index]}")
            
            elif key == ord('n'):
                if is_recording:
                    is_recording = False # Safety stop
                    
                current_label_idx = (current_label_idx + 1) % len(available_labels)
                label = available_labels[current_label_idx]
                print(f"➜ Switched to label: '{label}'")
                
            elif key == ord('q'):
                break
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        detector.close()
        print("✓ Session Closed.")

if __name__ == "__main__":
    main()
