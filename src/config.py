"""
Configuration File
==================
Central configuration for all project settings
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ==================== PATH CONFIGURATION ====================
# Directories
# config.py is now in src/, so we need to go up two levels to reach project root
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SRC_DIR)
DATASET_DIR = os.path.join(PROJECT_ROOT, "dataset")
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")

# Data files
RAW_DATA_FILE = os.path.join(DATASET_DIR, "raw_poses.csv")
CLEANED_DATA_FILE = os.path.join(DATASET_DIR, "cleaned_data.csv")

# Model files
MODEL_FILE = os.path.join(MODELS_DIR, "boxing_model.pkl")
ENCODER_FILE = os.path.join(MODELS_DIR, "label_encoder.pkl")
SCALER_FILE = os.path.join(MODELS_DIR, "scaler.pkl")

# ==================== CAMERA CONFIGURATION ====================
CAMERA_INDEX = int(os.environ.get("CAMERA_INDEX", 0))
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
TARGET_FPS = int(os.environ.get("TARGET_FPS", 30))

# ==================== POSE DETECTION CONFIGURATION ====================
# MediaPipe Pose settings
POSE_STATIC_IMAGE_MODE = False
POSE_MODEL_COMPLEXITY = 1  # 0, 1, or 2 (higher = more accurate but slower)
POSE_SMOOTH_LANDMARKS = True
POSE_MIN_DETECTION_CONFIDENCE = 0.5
POSE_MIN_TRACKING_CONFIDENCE = 0.5

# Landmark count (MediaPipe provides 33 landmarks)
NUM_LANDMARKS = 33
features_per_landmark = 4  # x, y, z, visibility

# Total features after Pro-Level Engineering v2:
# Body Landmarks (14 points * 4 coords) = 56
# + 4 Key Angles = 60
# + 4 Velocity Points * 3 coords = 72
# + 6 Bone Vectors * 3 coords = 90 [NEW]
# + 4 Acceleration Points * 3 coords = 102 [NEW]
# + 6 Distance Features = 108 [NEW]
TOTAL_FEATURES = 108

# ==================== MOTION ANALYZER CONFIGURATION ====================
# For 60 FPS, we need slightly larger buffers to filter noise effectively
# ==================== MOTION ANALYZER CONFIGURATION ====================
# Adjusted for responsiveness (Faster reset)
ANALYZER_HISTORY_SIZE = 3       # Minimal buffer
ANALYZER_CONSISTENCY_THRESHOLD = 1 # Instant trigger (Raw output)

# Temporal Smoothing (Prediction Buffer) [NEW]
TEMPORAL_WINDOW_SIZE = 3 # Number of frames to keep in history for voting/averaging

# ==================== GAME CONTROL CONFIGURATION ====================
# Confidence threshold for predictions (0.0 - 1.0)
CONFIDENCE_THRESHOLD = float(os.environ.get("CONFIDENCE_THRESHOLD", 0.8))

# Cooldown between actions (seconds)
ACTION_COOLDOWN = 0.5 

# Dynamic Key Bindings [NEW]
# We now load this dynamically, but keep a fallback here
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), "app"))
    from profiles_ui import ProfileManager
    _pm = ProfileManager()
    KEY_BINDINGS = _pm.get_active_bindings()
except Exception as e:
    print(f"Warning: Could not load profiles, using fallback bindings ({e})")
    KEY_BINDINGS = {
        "left_punch": "left",
        "right_punch": "right",
        "defense": "f",
        "dodge_left": "q",
        "dodge_right": "e",
        'dodge_front': ['w', 'space'],  # Press W + Space
        'dodge_back': ['s', 'space'],   # Press S + Space
        'final_skill': 'q',             # Press q (Ultimate)
        'neutral': None
    }

# ==================== TRAINING CONFIGURATION ====================
# Train-test split ratio
TEST_SIZE = 0.2
RANDOM_STATE = 42

# Model hyperparameters (Random Forest)
N_ESTIMATORS = 100
MAX_DEPTH = None
MIN_SAMPLES_SPLIT = 2
MIN_SAMPLES_LEAF = 1

# ==================== UI CONFIGURATION ====================
# Colors (BGR format for OpenCV)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (0, 0, 255)
COLOR_BLUE = (255, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_YELLOW = (0, 255, 255)

# Text settings
FONT = 2  # cv2.FONT_HERSHEY_DUPLEX (Cleaner)
FONT_SCALE = 0.6
FONT_THICKNESS = 1

# ==================== DATA COLLECTION SETTINGS ====================
# Burst Collection Options
BURST_OPTIONS = [100, 300, 500, 1000]
DEFAULT_BURST_INDEX = 1  # Standard (300)

RECOMMENDED_SAMPLES_PER_ACTION = 300
SAMPLES_PER_BURST = 300  # Default fallback

# Actions to collect (example)
DEFAULT_ACTIONS = [
    'neutral',
    'left_punch',
    'right_punch',
    'block',
    'dodge_left',
    'dodge_right',
    'dodge_front', # New
    'dodge_back',  # New
    'final_skill'  # New
]

# ==================== VALIDATION ====================
def ensure_directories():
    """Create necessary directories if they don't exist"""
    os.makedirs(DATASET_DIR, exist_ok=True)
    os.makedirs(MODELS_DIR, exist_ok=True)
    print(f"✓ Directories ready: {DATASET_DIR}, {MODELS_DIR}")

if __name__ == "__main__":
    # Print configuration summary
    print("=" * 60)
    print("Configuration Summary")
    print("=" * 60)
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Dataset Directory: {DATASET_DIR}")
    print(f"Models Directory: {MODELS_DIR}")
    print(f"Raw Data File: {RAW_DATA_FILE}")
    print(f"Model File: {MODEL_FILE}")
    print(f"Total Features: {TOTAL_FEATURES}")
    print(f"Confidence Threshold: {CONFIDENCE_THRESHOLD}")
    print(f"Action Cooldown: {ACTION_COOLDOWN}s")
    print(f"Key Bindings: {KEY_BINDINGS}")
    print("=" * 60)
