"""
Visual Data Cleaner
===================
A tool to visualize recorded pose data (stick figures) and manually remove bad samples.
This is the best way to "clean" data that has wrong poses or glitches.

Usage:
    python src/visualize_and_clean.py
"""

import cv2
import numpy as np
import pandas as pd
import os
import sys
import mediapipe as mp

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config

class VisualCleaner:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.connections = self.mp_pose.POSE_CONNECTIONS
        self.width = 640
        self.height = 480
        self.current_df = None
        self.delete_mask = [] # True = keep, False = delete
        self.current_index = 0
        self.file_path = ""

    def select_file(self):
        data_dir = os.path.join(config.DATASET_DIR, "by_class")
        if not os.path.exists(data_dir):
            print(f"❌ Directory not found: {data_dir}")
            print("Please run 'src/clean_and_split_data.py' first.")
            return False

        files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
        if not files:
            print("❌ No CSV files found.")
            return False

        print("\nSelect a dataset to clean:")
        for i, f in enumerate(files):
            print(f"  {i+1}. {f}")

        while True:
            try:
                choice = input("\nEnter number: ").strip()
                idx = int(choice) - 1
                if 0 <= idx < len(files):
                    self.file_path = os.path.join(data_dir, files[idx])
                    return True
            except:
                pass
            print("Invalid selection.")

    def load_data(self):
        print(f"Loading {self.file_path}...")
        self.current_df = pd.read_csv(self.file_path)
        self.delete_mask = [False] * len(self.current_df) # False means "Do NOT delete" (Keep)
        self.current_index = 0
        print(f"Loaded {len(self.current_df)} samples.")

    def draw_skeleton(self, row, image):
        # Extract landmarks
        landmarks = {}
        
        # The CSV has columns like landmark_0_x, landmark_0_y, ...
        # We need to parse them.
        try:
            for i in range(33): # MediaPipe Pose has 33 landmarks
                x = row[f'landmark_{i}_x']
                y = row[f'landmark_{i}_y']
                vis = row[f'landmark_{i}_visibility']
                
                # Scale to image size
                px = int(x * self.width)
                py = int(y * self.height)
                
                landmarks[i] = (px, py, vis)
                
                # Draw point
                color = config.COLOR_GREEN if vis > 0.5 else config.COLOR_RED
                cv2.circle(image, (px, py), 3, color, -1)
                
            # Draw connections
            for start_idx, end_idx in self.connections:
                if start_idx in landmarks and end_idx in landmarks:
                    s = landmarks[start_idx]
                    e = landmarks[end_idx]
                    
                    # Only draw if both are somewhat visible
                    if s[2] > 0.5 and e[2] > 0.5:
                        cv2.line(image, (s[0], s[1]), (e[0], e[1]), config.COLOR_WHITE, 2)
        except KeyError:
            pass # Column might not exist if CSV format is wrong

    def run(self):
        if not self.select_file():
            return

        self.load_data()
        
        window_name = "Visual Data Cleaner"
        cv2.namedWindow(window_name)
        
        print("\nControls:")
        print("  [Left/Right]: Navigate")
        print("  [Space/Del]: Mark/Unmark for deletion")
        print("  [S]: Save changes and Exit")
        print("  [Q]: Quit without saving")

        while True:
            # Create black canvas
            image = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            
            # Get current row
            row = self.current_df.iloc[self.current_index]
            is_marked_for_deletion = self.delete_mask[self.current_index]
            
            # Draw skeleton
            self.draw_skeleton(row, image)
            
            # UI Info
            status = "DELETE" if is_marked_for_deletion else "KEEP"
            status_color = config.COLOR_RED if is_marked_for_deletion else config.COLOR_GREEN
            
            cv2.putText(image, f"File: {os.path.basename(self.file_path)}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, config.COLOR_WHITE, 1)
            cv2.putText(image, f"Sample: {self.current_index + 1}/{len(self.current_df)}", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, config.COLOR_WHITE, 1)
            cv2.putText(image, f"Status: {status}", (10, 100), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)
            
            cv2.imshow(window_name, image)
            
            key = cv2.waitKey(0) & 0xFF
            
            if key == ord('q'):
                print("Exiting without saving.")
                break
            elif key == ord('s'):
                self.save_changes()
                break
            elif key == 81 or key == 2: # Left arrow (approx codes, varies by OS)
                self.current_index = max(0, self.current_index - 1)
            elif key == 83 or key == 3: # Right arrow
                self.current_index = min(len(self.current_df) - 1, self.current_index + 1)
            elif key == ord('a'): # Alternative Left
                self.current_index = max(0, self.current_index - 1)
            elif key == ord('d'): # Alternative Right
                self.current_index = min(len(self.current_df) - 1, self.current_index + 1)
            elif key == 32 or key == 127: # Space or Delete
                self.delete_mask[self.current_index] = not self.delete_mask[self.current_index]
                # Auto advance on delete? Maybe not, user might want to toggle back.

        cv2.destroyAllWindows()

    def save_changes(self):
        # Filter out rows marked for deletion
        # delete_mask[i] is True if we want to DELETE.
        # So we keep rows where delete_mask[i] is False.
        
        rows_to_keep = [not x for x in self.delete_mask]
        new_df = self.current_df[rows_to_keep]
        
        removed_count = len(self.current_df) - len(new_df)
        
        if removed_count > 0:
            new_df.to_csv(self.file_path, index=False)
            print(f"\n✅ Saved! Removed {removed_count} bad samples.")
            print(f"New total: {len(new_df)}")
        else:
            print("\nNo changes made.")

if __name__ == "__main__":
    cleaner = VisualCleaner()
    cleaner.run()
