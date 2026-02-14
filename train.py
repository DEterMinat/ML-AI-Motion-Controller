"""
Professional Training Script v2
===============================
Upgraded with:
- Data Augmentation
- Hyperparameter Tuning (GridSearchCV)
- Cross-Validation
- Improved Reporting
"""

import os
import sys
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Setup Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import src.config as config
from src.data.processing import transform_dataset
from src.data.augmentation import augment_dataset

def create_reports_dir():
    report_dir = os.path.join(config.PROJECT_ROOT, "reports")
    os.makedirs(report_dir, exist_ok=True)
    return report_dir

def load_data():
    """Load and transform raw data."""
    print("\n[STEP 1] Data Loading & Transformation...")
    data_dir = os.path.join(config.DATASET_DIR, "by_class")
    dfs = []
    
    if os.path.exists(data_dir):
        csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
        for file in csv_files:
            file_path = os.path.join(data_dir, file)
            try:
                df_raw = pd.read_csv(file_path)
                if df_raw.isnull().values.any():
                    print(f"  ⚠ Warning: Null values in {file}. Dropping...")
                    df_raw = df_raw.dropna()
                
                df_pro = transform_dataset(df_raw)
                dfs.append(df_pro)
                print(f"  ✓ Loaded {file}: {len(df_pro)} samples")
            except Exception as e:
                print(f"  ❌ Error loading {file}: {e}")
    
    if not dfs:
        raise FileNotFoundError("No data found!")
    
    return pd.concat(dfs, ignore_index=True)

def train(use_augmentation=True, use_grid_search=True):
    """Main training function with upgrades."""
    print("=" * 60)
    print("🤖 PROFESSIONAL AI TRAINING PIPELINE v2.0")
    print("=" * 60)
    
    reports_dir = create_reports_dir()
    
    # =================================================================
    # 1. Load Data
    # =================================================================
    df = load_data()
    print(f"  📊 Total Dataset: {len(df)} samples")
    
    # =================================================================
    # 2. Data Augmentation (NEW)
    # =================================================================
    if use_augmentation:
        print("\n[STEP 2] Data Augmentation...")
        original_size = len(df)
        df = augment_dataset(df, augment_factor=2, noise_level=0.02)
        print(f"  ✓ Augmented: {original_size} → {len(df)} samples (+{len(df)-original_size})")
    
    # EDA: Class Distribution
    plt.figure(figsize=(10, 5))
    sns.countplot(x='label', data=df)
    plt.title("Class Distribution (After Augmentation)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(reports_dir, "class_distribution.png"))
    print(f"  ✓ EDA Plot saved")

    # =================================================================
    # 3. Data Splitting
    # =================================================================
    print("\n[STEP 3] Data Splitting...")
    X = df.iloc[:, :-1].values
    y = df['label'].values
    
    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    X_train, X_temp, y_train, y_temp = train_test_split(
        X_scaled, y_encoded, test_size=0.3, random_state=42, stratify=y_encoded
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
    )
    
    print(f"  🔸 Training Set:   {len(X_train)} samples (70%)")
    print(f"  🔸 Validation Set: {len(X_val)} samples (15%)")
    print(f"  🔸 Test Set:       {len(X_test)} samples (15%)")

    # =================================================================
    # 4. Model Training with GridSearchCV (NEW)
    # =================================================================
    if use_grid_search:
        print("\n[STEP 4] Hyperparameter Tuning (GridSearchCV)...")
        param_grid = {
            'hidden_layer_sizes': [(128, 64), (256, 128), (256, 128, 64)],
            'alpha': [0.0001, 0.001],
            'learning_rate_init': [0.001, 0.0005]
        }
        
        base_model = MLPClassifier(
            activation='relu',
            solver='adam',
            max_iter=500,
            early_stopping=True,
            random_state=42,
            verbose=False
        )
        
        grid_search = GridSearchCV(
            base_model, param_grid, 
            cv=3, scoring='accuracy', 
            n_jobs=-1, verbose=1
        )
        grid_search.fit(X_train, y_train)
        
        print(f"\n  ✅ Best Parameters: {grid_search.best_params_}")
        print(f"  ✅ Best CV Score: {grid_search.best_score_*100:.2f}%")
        
        best_model = grid_search.best_estimator_
    else:
        print("\n[STEP 4] Training MLP (Default)...")
        best_model = MLPClassifier(
            hidden_layer_sizes=(128, 64),
            activation='relu',
            solver='adam',
            alpha=0.0001,
            learning_rate_init=0.001,
            max_iter=500,
            early_stopping=True,
            verbose=True,
            random_state=42
        )
        best_model.fit(X_train, y_train)

    # =================================================================
    # 5. Evaluation
    # =================================================================
    print("\n[STEP 5] Evaluation...")
    
    # Validation Accuracy
    y_val_pred = best_model.predict(X_val)
    val_acc = accuracy_score(y_val, y_val_pred)
    print(f"  📊 Validation Accuracy: {val_acc*100:.2f}%")
    
    # Test Accuracy
    y_pred = best_model.predict(X_test)
    test_acc = accuracy_score(y_test, y_pred)
    print(f"  🏆 Test Accuracy: {test_acc*100:.2f}%")
    
    print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=encoder.classes_))
    
    # Confusion Matrix
    plt.figure(figsize=(8, 6))
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', 
                xticklabels=encoder.classes_, 
                yticklabels=encoder.classes_, 
                cmap='Blues')
    plt.title(f"Confusion Matrix (Acc: {test_acc*100:.1f}%)")
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(os.path.join(reports_dir, "confusion_matrix.png"))
    print(f"  ✓ Confusion Matrix saved")

    # =================================================================
    # 6. Save Model
    # =================================================================
    print("\n[STEP 6] Saving Model...")
    config.ensure_directories()
    
    with open(config.MODEL_FILE, 'wb') as f:
        pickle.dump(best_model, f)
    with open(config.ENCODER_FILE, 'wb') as f:
        pickle.dump(encoder, f)
    with open(config.SCALER_FILE, 'wb') as f:
        pickle.dump(scaler, f)
        
    print(f"  ✅ Model saved: {config.MODEL_FILE}")
    print(f"  ✅ Encoder saved: {config.ENCODER_FILE}")
    print(f"  ✅ Scaler saved: {config.SCALER_FILE}")
    
    print("\n" + "=" * 60)
    print(f"🎉 TRAINING COMPLETE! Test Accuracy: {test_acc*100:.2f}%")
    print("=" * 60)
    
    return best_model, encoder, scaler, test_acc


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Train Motion Controller Model v2')
    parser.add_argument('--no-augment', action='store_true', help='Disable data augmentation')
    parser.add_argument('--no-grid', action='store_true', help='Disable GridSearchCV')
    args = parser.parse_args()
    
    train(
        use_augmentation=not args.no_augment,
        use_grid_search=not args.no_grid
    )
