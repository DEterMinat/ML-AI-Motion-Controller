# ML-AI Motion Controller - Documentation

## 1. Overview

ML-AI Motion Controller is a webcam-based motion recognition system for boxing game control.

Core flow:

1. Capture human pose from webcam with MediaPipe.
2. Convert raw landmarks (132 values) into engineered motion features (108 values).
3. Classify action with a trained model.
4. Smooth predictions with MotionAnalyzer.
5. Trigger mapped game input and broadcast action over WebSocket.

Main runtime entrypoint is `run.py`.

## 2. Project Entry Points

- Run app (Python): `python run.py`
- Run app (Batch): `scripts\run_app.bat`
- Setup environment: `scripts\setup_env.bat`
- Data collection: `python -m src.data.collection`
- Train model (MLP pipeline): `python training/train.py`

## 3. System Architecture

### 3.1 Runtime Components

- GUI application: `src/app/main.py`
- Game engine loop: `src/app/game_engine.py`
- Pose detection + feature extraction: `src/utils/pose_detection.py`
- Prediction smoothing/state machine: `src/utils/motion_analyzer.py`
- Input trigger layer: `src/utils/input_handler.py`
- WebSocket broadcaster: `src/utils/ws_server.py`
- Global settings: `src/config.py`

### 3.2 Runtime Model Files

At runtime, the game engine loads:

- `models/boxing_model.pkl`
- `models/label_encoder.pkl`
- `models/scaler.pkl`

These are the latest alias files produced by training.

## 4. Data Pipeline

### 4.1 Raw Data

Data collection stores class-separated CSV files at:

- `dataset/by_class/*.csv`

Each frame contains MediaPipe landmarks:

- 33 landmarks x 4 values (`x, y, z, visibility`) = 132 raw values
- plus `label`

### 4.2 Engineered Features

Training/runtime share the same feature logic from `PoseDetector.compute_features()`.

Feature output is fixed at 108 values (`TOTAL_FEATURES = 108` in `src/config.py`):

- Body coordinates (upper body subset)
- Joint angles
- Velocity terms
- Bone direction vectors
- Acceleration terms
- Distance features

This guarantees feature consistency between offline training and online inference.

## 5. Training Pipeline (Current)

Main script: `training/train.py`

Default pipeline:

1. Load and merge all class CSV files from `dataset/by_class/`.
2. Transform raw landmarks to 108 engineered features.
3. Optional augmentation (`augment_dataset`).
4. Stratified split with `train_test_split` (70/15/15).
5. Train MLP (default uses GridSearchCV).
6. Evaluate and export confusion matrix/class distribution plots.
7. Save versioned artifacts and update latest model alias files.

### 5.1 Training Commands

- Full training (augmentation + grid): `python training/train.py`
- No grid search: `python training/train.py --no-grid`
- No augmentation: `python training/train.py --no-augment`

### 5.2 Model Comparison Notebooks

Additional model experiments are maintained in notebooks under `training/` and executed copies in `training/executed/`:

- MLP baseline
- Transformer (temporal)
- LSTM/GRU
- SVM
- ST-GCN

Metrics snapshots are stored in `reports/model_comparison/*_metrics.json`.

## 6. Runtime Action Flow

Per frame in `GameControllerThreaded.process_frame()`:

1. Read frame from `CameraStream`.
2. Run pose detection.
3. Extract raw landmarks.
4. Build 108 features (including velocity/acceleration from frame history).
5. Scale features with saved scaler.
6. Predict class and confidence.
7. Smooth with `MotionAnalyzer`.
8. If confidence >= threshold, trigger mapped input.
9. Broadcast action payload over WebSocket.

## 7. Action Mapping and Profiles

Key bindings are profile-driven.

Source of truth:

- Active profile and bindings: `src/app/profiles.json`
- Profile manager UI: `src/app/profiles_ui.py`

Default active profile is `Boxing (Default)`.

Current default bindings:

- `left_punch`: `left`
- `right_punch`: `right`
- `defense`: `f`
- `dodge_left`: `q`
- `dodge_right`: `e`
- `dodge_front`: `w space`
- `dodge_back`: `s space`
- `final_skill`: `x`

Note on label naming:

- Dataset/training often uses action label `block`.
- Runtime hold action key uses `defense` in trigger logic.
- If documenting class-to-input mapping, explicitly map `block -> defense`.

## 8. WebSocket Integration

WebSocket server runs at:

- `ws://localhost:8765`

Broadcast payload shape:

```json
{
  "action": "left_punch",
  "confidence": 0.97,
  "state": "ACTION"
}
```

Server implementation: `src/utils/ws_server.py`.

## 9. Configuration Reference

Main runtime configuration is in `src/config.py`.

Important settings:

- `CAMERA_INDEX`
- `TARGET_FPS`
- `CONFIDENCE_THRESHOLD` (default `0.8`)
- `ACTION_COOLDOWN` (default `0.5`)
- Pose detection parameters (`POSE_*`)
- Paths for model/data directories

## 10. Setup and Installation

### 10.1 Fast Setup (Recommended on Windows)

Run:

```bash
scripts\setup_env.bat
```

What it does:

1. Checks Python
2. Creates `.venv`
3. Installs dependencies from `requirements.txt`
4. Runs system health check (`scripts/system_health_check.py`)

### 10.2 Manual Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 11. Troubleshooting

### 11.1 App Cannot Start

- Ensure `.venv` exists and dependencies are installed.
- Run `scripts\setup_env.bat`.
- Then run `python run.py`.

### 11.2 Webcam Not Detected

- Update `CAMERA_INDEX` in `src/config.py`.
- Verify camera is not locked by another app.

### 11.3 Wrong or Delayed Action Triggers

- Check confidence threshold (`CONFIDENCE_THRESHOLD`).
- Check cooldown (`ACTION_COOLDOWN`).
- Recalibrate in app and verify data quality.
- Retrain model if dataset drifted.

### 11.4 Missing Model Files

If app reports missing model artifacts, run training first:

```bash
python training/train.py
```

## 12. Notes on Documentation Consistency

This document is aligned to the current codebase structure where:

- Setup uses `scripts/setup_env.bat`
- Runtime starts from `run.py`
- Training uses `training/train.py`
- Features are engineered to 108 dimensions
- Runtime key mapping is profile-based via `profiles.json`

If implementation changes, update this file together with `README.md` and result summary docs.
