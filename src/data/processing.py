import numpy as np
import pandas as pd
import sys
import os

# Ensure we can import src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.utils.pose_detection import PoseDetector
import src.config as config

def transform_dataset(df_raw):
    """
    Transform Raw Skeleton Data(132) -> Pro-Level Features(108)
    Uses the shared PoseDetector logic to ensure Training matches Runtime.
    Includes:
    - Normalization
    - Upper Body Filter
    - Angles
    - Velocity (Delta from previous frame)
    - Bone Vectors [NEW]
    - Acceleration [NEW]
    - Distance Features [NEW]
    """
    detector = PoseDetector()
    pro_data = []
    
    # Iterate through rows to maintain sequence for velocity/acceleration
    prev_raw_landmarks = None
    prev_velocity = None
    
    # Identify feature columns (everything except label)
    feature_cols = [c for c in df_raw.columns if c != 'label']
    
    for _, row in df_raw.iterrows():
        # Get raw landmarks list (132 floats)
        raw_landmarks = row[feature_cols].values.tolist()
        
        # Compute features with velocity and acceleration
        result = detector.compute_features(raw_landmarks, prev_raw_landmarks, prev_velocity)
        
        if result:
            features, current_velocity = result
            # Append Label
            features.append(row['label'])
            pro_data.append(features)
            
            # Update history
            prev_raw_landmarks = raw_landmarks
            prev_velocity = current_velocity
        else:
            # If feature extraction fails, reset history
            prev_raw_landmarks = None
            prev_velocity = None
            
    # Create Feature Names
    new_cols = [f"f_{i}" for i in range(config.TOTAL_FEATURES)] + ['label']
    
    if not pro_data:
        # Return empty DF with correct columns
        return pd.DataFrame(columns=new_cols)
        
    return pd.DataFrame(pro_data, columns=new_cols)

def create_sequences(df_pro, window_size=10, step_size=1):
    """
    Create Sliding Window Sequences from Pro-level features.
    Input: df_pro (N, 109) - features + label
    Output: X (Samples, window_size, 108), y (Samples,)
    """
    sequences = []
    labels = []
    
    # Process by label to avoid mixing different actions in one window
    for label in df_pro['label'].unique():
        df_class = df_pro[df_pro['label'] == label].copy()
        
        # Extract features
        X_class = df_class.drop(columns=['label']).values
        
        # Create sliding windows
        for i in range(0, len(X_class) - window_size + 1, step_size):
            window = X_class[i : i + window_size]
            sequences.append(window)
            labels.append(label)
            
    return np.array(sequences), np.array(labels)

