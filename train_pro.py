import os
import sys
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Setup Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import src.config as config
from src.data.processing import transform_dataset

def create_reports_dir():
    report_dir = os.path.join(config.PROJECT_ROOT, "reports")
    os.makedirs(report_dir, exist_ok=True)
    return report_dir

def train():
    print("="*60)
    print("🤖 PROFESSIONAL AI TRAINING PIPELINE")
    print("="*60)
    
    reports_dir = create_reports_dir()
    
    # =================================================================
    # 1. Data Preparation (การเตรียมข้อมูล)
    # =================================================================
    print("\n[STEP 1] Data Preparation & Cleaning...")
    data_dir = os.path.join(config.DATASET_DIR, "by_class")
    dfs = []
    
    if os.path.exists(data_dir):
        csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
        for file in csv_files:
            file_path = os.path.join(data_dir, file)
            try:
                # Load Raw Data
                df_raw = pd.read_csv(file_path)
                
                # Check for nulls
                if df_raw.isnull().values.any():
                    print(f"  ⚠ Warning: Null values found in {file}. Dropping...")
                    df_raw = df_raw.dropna()
                
                # TRANSFORM to Pro-Level Features
                df_pro = transform_dataset(df_raw)
                dfs.append(df_pro)
                print(f"  ✓ Loaded {file}: {len(df_pro)} clean samples")
            except Exception as e:
                print(f"  ❌ Error loading {file}: {e}")
    
    if not dfs:
        print("❌ No data found! Please collect data first.")
        return
        
    df = pd.concat(dfs, ignore_index=True)
    print(f"  📊 Total Dataset: {len(df)} samples")
    print(f"  🧠 Features: {len(df.columns) - 1} input neurons")
    
    # EDA: Class Distribution Plot
    plt.figure(figsize=(10, 5))
    sns.countplot(x='label', data=df)
    plt.title("Class Distribution")
    plt.savefig(os.path.join(reports_dir, "class_distribution.png"))
    print(f"  ✓ EDA Plot saved to reports/class_distribution.png")

    # =================================================================
    # 2. Data Splitting (การแบ่งชุดข้อมูล)
    # =================================================================
    print("\n[STEP 2] Data Splitting (Train / Validation / Test)...")
    X = df.iloc[:, :-1].values
    y = df['label'].values
    
    # Encode and Scale
    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)
    
    # Neural Nets need scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X) # Clean data -> mean=0, std=1
    
    # Split: Train (70%), Temp (30%)
    X_train, X_temp, y_train, y_temp = train_test_split(
        X_scaled, y_encoded, test_size=0.3, random_state=42, stratify=y_encoded
    )
    
    # Split Temp: Val (15%), Test (15%)
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
    )
    
    print(f"  🔸 Training Set:   {len(X_train)} samples (70%)")
    print(f"  🔸 Validation Set: {len(X_val)} samples (15%)")
    print(f"  🔸 Test Set:       {len(X_test)} samples (15%)")

    # =================================================================
    # 3. Model Selection & Configuration (เลือกโมเดลและตั้งค่า)
    # 4. The Training Loop (การฝึกสอน - Forward/Backward Prop)
    # =================================================================
    print("\n[STEP 3 & 4] Model Architecture & Training Loop...")
    # MLP = Multi-Layer Perceptron (Classic Neural Network)
    # Architecture: Input(96) -> Hidden(128) -> Hidden(64) -> Output(Classes)
    model = MLPClassifier(
        hidden_layer_sizes=(128, 64), # Layers & Neurons
        activation='relu',            # Activation Function
        solver='adam',                # Optimizer
        alpha=0.0001,                 # Regularization (L2)
        batch_size='auto',            # Mini-batch 
        learning_rate_init=0.001,     # Learning Rate
        max_iter=500,                 # Epochs
        early_stopping=True,          # Monitor Validation Set
        validation_fraction=0.1,      # Internal validation
        verbose=True,                 # Show Loop Progress
        random_state=42
    )
    
    print(f"  🧠 Architecture: Input(96) -> Dense(128) -> ReLU -> Dense(64) -> ReLU -> Output")
    print("  🚀 Starting Backpropagation...")
    model.fit(X_train, y_train)

    # =================================================================
    # 5. Evaluation & Tuning (การประเมินผล)
    # =================================================================
    print("\n[STEP 5] Evaluation (Test Set)...")
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print(f"  🏆 Test Accuracy: {acc*100:.2f}%")
    print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=encoder.classes_))
    
    # Confusion Matrix
    plt.figure(figsize=(8, 6))
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', xticklabels=encoder.classes_, yticklabels=encoder.classes_, cmap='Blues')
    plt.title("Confusion Matrix")
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.savefig(os.path.join(reports_dir, "confusion_matrix.png"))
    print(f"  ✓ Confusion Matrix saved to reports/confusion_matrix.png")

    # =================================================================
    # 6. Deployment (การนำไปใช้งาน)
    # =================================================================
    print("\n[STEP 6] Deployment & Export...")
    config.ensure_directories()
    
    # Save Model
    with open(config.MODEL_FILE, 'wb') as f:
        pickle.dump(model, f)
        
    # Save Encoder
    with open(config.ENCODER_FILE, 'wb') as f:
        pickle.dump(encoder, f)
        
    # Save Scaler (Crucial for Neural Nets!)
    with open(config.SCALER_FILE, 'wb') as f:
        pickle.dump(scaler, f)
        
    print(f"  ✅ Model saved:   {config.MODEL_FILE}")
    print(f"  ✅ Encoder saved: {config.ENCODER_FILE}")
    print(f"  ✅ Scaler saved:  {config.SCALER_FILE}")
    print("\n🎉 TRAINING COMPLETE! System is ready.")

if __name__ == "__main__":
    train()
