"""
Data Augmentation Utilities
============================
Functions to augment pose data for improved model robustness.
"""

import numpy as np
import pandas as pd
from typing import List, Tuple


def add_noise(features: np.ndarray, noise_level: float = 0.02) -> np.ndarray:
    """
    Add Gaussian noise to features.
    
    Args:
        features: Feature array (N, num_features)
        noise_level: Standard deviation of noise (default 2%)
    
    Returns:
        Augmented features with noise
    """
    noise = np.random.normal(0, noise_level, features.shape)
    return features + noise


def scale_features(features: np.ndarray, scale_range: Tuple[float, float] = (0.9, 1.1)) -> np.ndarray:
    """
    Scale features by random factor (simulates distance variation).
    
    Args:
        features: Feature array (N, num_features)
        scale_range: Min and max scale factors
    
    Returns:
        Scaled features
    """
    scale = np.random.uniform(scale_range[0], scale_range[1])
    return features * scale


def mirror_horizontal(features: np.ndarray, num_landmarks: int = 14) -> np.ndarray:
    """
    Mirror pose horizontally (swap left/right).
    Note: This requires knowing the landmark structure.
    For upper body (14 points): swap indices 0-1, 2-3, 4-5 etc.
    
    Args:
        features: Feature array (single sample)
        num_landmarks: Number of body landmarks
    
    Returns:
        Mirrored features
    """
    mirrored = features.copy()
    coords_per_landmark = 4  # x, y, z, visibility
    
    # Swap left/right pairs (0↔1, 2↔3, 4↔5, 6↔7)
    # Left shoulder (0) ↔ Right shoulder (1)
    # Left elbow (2) ↔ Right elbow (3)
    # Left wrist (4) ↔ Right wrist (5)
    # etc.
    swap_pairs = [(0, 1), (2, 3), (4, 5), (6, 7)]
    
    for left_idx, right_idx in swap_pairs:
        left_start = left_idx * coords_per_landmark
        right_start = right_idx * coords_per_landmark
        
        # Swap the coordinate blocks
        temp = mirrored[left_start:left_start + coords_per_landmark].copy()
        mirrored[left_start:left_start + coords_per_landmark] = mirrored[right_start:right_start + coords_per_landmark]
        mirrored[right_start:right_start + coords_per_landmark] = temp
    
    # Flip X coordinates (negate them)
    for i in range(num_landmarks):
        x_idx = i * coords_per_landmark
        mirrored[x_idx] = -mirrored[x_idx]
    
    return mirrored


def augment_dataset(df: pd.DataFrame, 
                    augment_factor: int = 2,
                    noise_level: float = 0.02,
                    use_mirror: bool = True,
                    use_scale: bool = True) -> pd.DataFrame:
    """
    Augment entire dataset by applying random transformations.
    
    Args:
        df: DataFrame with features and 'label' column
        augment_factor: How many augmented copies per original sample
        noise_level: Noise standard deviation
        use_mirror: Whether to include mirrored samples
        use_scale: Whether to include scaled samples
    
    Returns:
        Augmented DataFrame (original + augmented samples)
    """
    augmented_data = []
    feature_cols = [c for c in df.columns if c != 'label']
    
    for _, row in df.iterrows():
        features = row[feature_cols].values.astype(float)
        label = row['label']
        
        for _ in range(augment_factor):
            aug_features = features.copy()
            
            # Random augmentation selection
            if np.random.random() < 0.5:
                aug_features = add_noise(aug_features, noise_level)
            
            if use_scale and np.random.random() < 0.3:
                aug_features = scale_features(aug_features)
            
            if use_mirror and np.random.random() < 0.3:
                # Only mirror if action is not directional
                if 'left' not in label.lower() and 'right' not in label.lower():
                    aug_features = mirror_horizontal(aug_features)
            
            augmented_data.append(list(aug_features) + [label])
    
    # Combine original + augmented
    aug_df = pd.DataFrame(augmented_data, columns=list(feature_cols) + ['label'])
    return pd.concat([df, aug_df], ignore_index=True)


if __name__ == "__main__":
    # Test
    print("Data Augmentation Module Loaded")
    print("Functions: add_noise, scale_features, mirror_horizontal, augment_dataset")
