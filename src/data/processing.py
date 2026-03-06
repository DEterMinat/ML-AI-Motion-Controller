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


def video_based_split(X, y, test_size=0.2, val_size=0.15, chunk_size=50, random_state=42):
    """
    STRATIFIED Split data by video chunks instead of random frames to prevent data leakage.
    
    Ensures EVERY CLASS appears in train/val/test sets by splitting each class separately.
    Assumes sequential frames are from same video. Splits data into chunks (pseudo-videos)
    and ensures no chunk appears in both train and test sets.
    
    Args:
        X: Feature array (N, ...) or (N, window, features)
        y: Labels (N,)
        test_size: Proportion for test set (0-1)
        val_size: Proportion for validation set (0-1), only used if > 0
        chunk_size: Number of consecutive samples per video chunk
        random_state: Random seed
        
    Returns:
        If val_size > 0: X_train, X_val, X_test, y_train, y_val, y_test
        If val_size == 0: X_train, X_test, y_train, y_test
    """
    np.random.seed(random_state)
    
    # Initialize split containers
    train_indices = []
    val_indices = []
    test_indices = []
    
    # Process each class separately (STRATIFIED)
    unique_classes = np.unique(y)
    
    for label in unique_classes:
        # Get indices for this class
        class_mask = (y == label)
        class_indices = np.where(class_mask)[0]
        n_class_samples = len(class_indices)
        
        # Create chunk IDs for this class
        n_class_chunks = (n_class_samples + chunk_size - 1) // chunk_size
        chunk_ids = np.repeat(np.arange(n_class_chunks), chunk_size)[:n_class_samples]
        
        # Shuffle chunk order (but keep frames within chunk together)
        unique_chunks = np.unique(chunk_ids)
        np.random.shuffle(unique_chunks)
        
        # Split chunks into train/val/test (ensure at least 1 chunk per split)
        n_test_chunks = max(1, int(len(unique_chunks) * test_size))
        n_val_chunks = max(1, int(len(unique_chunks) * val_size)) if val_size > 0 else 0
        n_train_chunks = len(unique_chunks) - n_test_chunks - n_val_chunks
        
        # Handle case where we don't have enough chunks
        if n_train_chunks < 1:
            # Fallback: at least 1 chunk for train
            n_train_chunks = 1
            n_test_chunks = max(1, (len(unique_chunks) - 1) // 2)
            n_val_chunks = len(unique_chunks) - n_train_chunks - n_test_chunks
        
        train_chunks = unique_chunks[:n_train_chunks]
        test_chunks = unique_chunks[n_train_chunks:n_train_chunks + n_test_chunks]
        
        # Get indices for each split (relative to class_indices)
        for i, chunk_id in enumerate(chunk_ids):
            actual_idx = class_indices[i]
            if chunk_id in train_chunks:
                train_indices.append(actual_idx)
            elif chunk_id in test_chunks:
                test_indices.append(actual_idx)
            elif val_size > 0:
                val_indices.append(actual_idx)
    
    # Convert to arrays and sort (to maintain some order)
    train_indices = np.array(train_indices)
    test_indices = np.array(test_indices)
    
    if val_size > 0:
        val_indices = np.array(val_indices)
        return (X[train_indices], X[val_indices], X[test_indices], 
                y[train_indices], y[val_indices], y[test_indices])
    else:
        return X[train_indices], X[test_indices], y[train_indices], y[test_indices]

