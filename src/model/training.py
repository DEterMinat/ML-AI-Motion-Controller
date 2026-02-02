"""
Model Training Script
=====================
Trains a classification model using collected pose data

Usage:
    python -m src.train_model
    
    Or from project root:
    python src/train_model.py
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config

def load_and_validate_data():
    """Load and validate the collected data from multiple CSV files"""
    data_dir = os.path.join(config.DATASET_DIR, "by_class")
    
    print("=" * 60)
    print("Motion Controller - Model Training Script")
    print("=" * 60)
    
    dfs = []
    
    # 1. Try loading from split files (New method)
    if os.path.exists(data_dir):
        csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
        if csv_files:
            print(f"\nLoading data from {data_dir}...")
            for file in csv_files:
                file_path = os.path.join(data_dir, file)
                try:
                    df_part = pd.read_csv(file_path)
                    dfs.append(df_part)
                    print(f"  ✓ Loaded {file}: {len(df_part)} samples")
                except Exception as e:
                    print(f"  ⚠ Error loading {file}: {e}")
    
    # 2. Fallback to single file (Old method)
    if not dfs and os.path.exists(config.RAW_DATA_FILE):
        print(f"\n⚠ No split data found. Falling back to {config.RAW_DATA_FILE}")
        dfs.append(pd.read_csv(config.RAW_DATA_FILE))
        
    if not dfs:
        raise FileNotFoundError(
            f"❌ Error: No training data found!\n"
            f"Please run data_collector.py to collect data."
        )
    
    # Combine all data
    df = pd.concat(dfs, ignore_index=True)
    
    print(f"\n✓ Total samples loaded: {len(df)}")
    print(f"  Features: {len(df.columns) - 1}")
    print(f"\nLabel distribution:")
    print(df['label'].value_counts())
    
    # Validate data
    if len(df) < 10:
        raise ValueError(
            "❌ Error: Not enough training samples!\n"
            f"Please collect at least {config.RECOMMENDED_SAMPLES_PER_ACTION} samples per action."
        )
    
    return df

def prepare_features_and_labels(df):
    """Prepare feature matrix and label vector"""
    # Separate features and labels
    X = df.iloc[:, :-1].values  # All columns except last (label)
    y = df['label'].values       # Last column (label)
    
    # Check for missing values
    if np.isnan(X).any():
        print("⚠ Warning: Found NaN values in features. Filling with 0...")
        X = np.nan_to_num(X, nan=0.0)
    
    print(f"\n✓ Feature matrix shape: {X.shape}")
    print(f"✓ Label vector shape: {y.shape}")
    
    return X, y

def encode_labels(y):
    """Encode string labels to integers"""
    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)
    
    print(f"\n✓ Encoded {len(encoder.classes_)} unique classes:")
    for idx, label in enumerate(encoder.classes_):
        print(f"  {idx}: {label}")
    
    return y_encoded, encoder

def train_model(X_train, y_train):
    """Train Random Forest classifier"""
    print("\n" + "=" * 60)
    print("Training Random Forest Classifier...")
    print("=" * 60)
    
    model = RandomForestClassifier(
        n_estimators=config.N_ESTIMATORS,
        max_depth=config.MAX_DEPTH,
        min_samples_split=config.MIN_SAMPLES_SPLIT,
        min_samples_leaf=config.MIN_SAMPLES_LEAF,
        random_state=config.RANDOM_STATE,
        n_jobs=-1,
        verbose=1
    )
    
    model.fit(X_train, y_train)
    print("\n✓ Model training completed!")
    
    return model

def evaluate_model(model, X_test, y_test, encoder):
    """Evaluate model performance"""
    print("\n" + "=" * 60)
    print("Model Evaluation")
    print("=" * 60)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n✓ Test Accuracy: {accuracy * 100:.2f}%")
    
    # Classification report
    print("\nClassification Report:")
    print("-" * 60)
    print(classification_report(y_test, y_pred, target_names=encoder.classes_))
    
    # Confusion matrix
    print("Confusion Matrix:")
    print("-" * 60)
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    
    return accuracy

def save_model_and_encoder(model, encoder):
    """Save trained model and label encoder"""
    config.ensure_directories()
    
    # Save model
    with open(config.MODEL_FILE, 'wb') as f:
        pickle.dump(model, f)
    print(f"\n✓ Model saved to: {config.MODEL_FILE}")
    
    # Save encoder
    with open(config.ENCODER_FILE, 'wb') as f:
        pickle.dump(encoder, f)
    print(f"✓ Encoder saved to: {config.ENCODER_FILE}")

def main():
    """Main training pipeline"""
    try:
        # Load data
        df = load_and_validate_data()
        
        # Prepare features and labels
        X, y = prepare_features_and_labels(df)
        
        # Encode labels
        y_encoded, encoder = encode_labels(y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded,
            test_size=config.TEST_SIZE,
            random_state=config.RANDOM_STATE,
            stratify=y_encoded
        )
        
        print(f"\n✓ Data split:")
        print(f"  Training samples: {len(X_train)}")
        print(f"  Testing samples: {len(X_test)}")
        
        # Train model
        model = train_model(X_train, y_train)
        
        # Evaluate model
        accuracy = evaluate_model(model, X_test, y_test, encoder)
        
        # Save model and encoder
        save_model_and_encoder(model, encoder)
        
        print("\n" + "=" * 60)
        print("✅ Training completed successfully!")
        print("=" * 60)
        print(f"Final Accuracy: {accuracy * 100:.2f}%")
        print("\nYou can now run game_controller.py to use the trained model!")
        
    except Exception as e:
        print(f"\n❌ Error during training: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
