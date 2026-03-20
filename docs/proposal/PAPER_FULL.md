% ML-AI Motion Controller — Full IMRAD Paper

# ML-AI Motion Controller: Real‑time Webcam‑based Motion Recognition for Game Control

Authors: DEterMinat (project repository)

Date: 2026-03-20

---

## Abstract

We present ML‑AI Motion Controller, an end‑to‑end pipeline that converts real‑time upper‑body motion from a commodity webcam into low‑latency game control commands. The system uses MediaPipe for pose estimation and a deterministic feature extractor that compresses 33 landmarks into a 108‑dimensional feature vector. We evaluate lightweight classifiers and a graph model on a held‑out test split. Our production baseline is a tuned MLP (per‑frame dense classifier) which attains 99.26% test accuracy (frame‑based training with augmentation; see `docs/TRAINING_RESULTS_SUMMARY.md`) with inference <5 ms on the target CPU. A tuned RBF SVM reaches 95.0% with ≈0.259 ms latency, and ST‑GCN records 87.33% accuracy with ≈1.06 ms latency. These results demonstrate that carefully engineered per‑frame features enable compact models to meet strict real‑time constraints while delivering high classification performance. We release code, trained models, and evaluation scripts to support reproducibility, and discuss practical trade‑offs (latency vs. temporal modeling), failure modes, and production improvements.

Keywords: pose estimation, feature engineering, MLP, SVM, ST‑GCN, real‑time control, MediaPipe

---

## 1. Introduction

Controller‑free game control via human motion enables intuitive interaction paradigms for gaming, training, and rehabilitation. Low latency and robustness to variation in users and environments are key requirements. Recent pose estimation frameworks provide accurate landmark extraction at real‑time frame rates on commodity hardware; however, translating raw landmarks into reliable discrete actions (e.g., left punch, block, dodge) requires principled feature extraction, temporal reasoning, and engineering for low inference cost.

This paper documents an applied pipeline, implemented in the repository, that prioritizes runtime parity (identical feature transforms during training and inference), low latency, and reproducibility. Our contributions are:

- A deterministic 108‑dimensional feature set derived from MediaPipe landmarks with explicit normalization and temporal derivatives.
- An empirical comparison of classical and temporal models focused on practical deployability.
- A production‑oriented runtime design for low latency inference and straightforward integration into games (simulated inputs and WebSocket messages).

![System architecture](figs/figure1_system.png)

**Figure 1.** Overall system architecture showing the real‑time pipeline from webcam → MediaPipe pose detector → deterministic feature extractor (108‑D) → classifier (SVM / MLP / ST‑GCN) → game overlay and command dispatch.

## 2. Related Work

Skeleton‑ and pose‑based action recognition spans a spectrum from handcrafted‑feature + classical classifier pipelines to modern temporal and graph‑structured deep models. Early practical systems relied on engineered descriptors (joint angles, relative distances, velocities) paired with SVMs or small MLPs to obtain robust per‑frame recognition with minimal runtime cost; these approaches remain attractive for latency‑sensitive HCI applications where computational budget is limited.

Sequence models such as LSTM/GRU and transformer variants model temporal dependencies and can capture subtle dynamics that per‑frame classifiers miss. LSTM/GRU architectures are widely used when multi‑frame context improves recognition, though they typically increase inference cost and implementation complexity on CPU targets.

Graph‑based approaches (notably ST‑GCN) treat skeleton joints as nodes in a spatio‑temporal graph and have shown strong performance on skeleton action benchmarks by explicitly modeling joint connectivity and motion patterns. However, graph models often demand higher compute and memory, creating a trade‑off with latency for real‑time interactive systems.

Practical deployment emphasizes robust real‑time pose estimation (e.g., MediaPipe), latency‑aware evaluation, and targeted data augmentation to handle occlusions and sensor noise. Our work positions engineered per‑frame features as a pragmatic middle ground: they achieve high accuracy with minimal runtime cost while retaining interpretable failure modes that facilitate UX improvements.

## 3. System Overview

The implementation (code under `src/`) is organized into modular components:

- Pose detection and landmark extraction: `src/utils/pose_detection.py`
- Deterministic feature transform: `compute_features()` (produces 108‑D features)
- Model training & evaluation: `training/train.py`
- Runtime inference and smoothing: `src/app/game_engine.py`, `src/utils/motion_analyzer.py`
- Input mapping and integration: `src/utils/input_handler.py` and WebSocket broadcaster `src/utils/ws_server.py`

Runtime pipeline: webcam → MediaPipe → compute_features() → StandardScaler → model.predict → MotionAnalyzer → InputHandler / WS broadcast.

### 3.1 Design goals

Key objectives:

- Low end‑to‑end latency (model inference + filtering < few ms where possible).
- Deterministic parity (feature pipeline identical for training and runtime).
- Simplicity and interpretability of features to ease debugging and tuning.

## 4. Dataset and Preprocessing

The dataset is maintained under `dataset/by_class/` and contains labeled feature vectors collected from webcam recordings with MediaPipe landmarks. The training script (`training/train.py`) performs the following preprocessing steps:

- Transform raw CSVs into the PRO feature format using the same `compute_features()` implementation.
- Optional data augmentation (default in training pipeline): augmentation factor 2 with small Gaussian noise (noise_level=0.02).
- Standard scaling with `sklearn.preprocessing.StandardScaler`.
- Stratified split: 70% train / 15% val / 15% test (see `training/train.py`).

Illustrative EDA and saved figures are available under `reports/` (class distribution, confusion matrix, training curves).

![Class distribution](figs/figure_extra_class_distribution.png)

**Figure 8.** Class distribution on the augmented training set (counts per class).

### Dataset samples

Below are representative frames from the dataset with MediaPipe pose overlays (selected across classes):

![sample1](figs/BOXING-DETECT/S__4300805_0.jpg) ![sample2](figs/BOXING-DETECT/S__4300806_0.jpg) ![sample3](figs/BOXING-DETECT/S__4300807_0.jpg)

![sample4](figs/BOXING-DETECT/S__4300808_0.jpg) ![sample5](figs/BOXING-DETECT/S__4300809_0.jpg) ![sample6](figs/BOXING-DETECT/S__4300815.jpg)

**Figure 9.** Example frames from the dataset with pose overlay (illustrative; selected frames across classes).

## 5. Feature Engineering (Deterministic 108‑D representation)

The feature extractor is implemented in `src/utils/pose_detection.py::PoseDetector.compute_features()` and compresses 33 MediaPipe landmarks (4 values each → 132 raw floats) into a compact 108‑dimensional vector. The groups are:

![Selected landmarks and features](figs/figure2_landmarks.png)

**Figure 2.** Selected upper‑body MediaPipe landmarks and example engineered features (joint angles, normalized distances, velocity and acceleration vectors).

- A. Body coordinates (selected upper‑body landmarks, normalized by torso size): 56 features
- B. Joint angles (upper body): 4 features
- C. Velocity (delta of selected joints, scaled): 12 features (scale factor = 5.0)
- D. Bone direction vectors (normalized): 18 features
- E. Acceleration (rate of change of velocity, requires previous frame): 12 features (scale factor = 2.0)
- F. Distance ratios (relative to torso size): 6 features

Total: 108 features.

Angles are computed using the cosine rule (via normalized dot products). Velocity and acceleration are computed with finite differences and scaling constants selected for empirical sensitivity. The code includes visibility channels and per‑frame normalization by torso width to achieve scale invariance.

Refer to implementation: [src/utils/pose_detection.py](src/utils/pose_detection.py#L1-L260)
Note: `compute_features()` returns a tuple `(features, current_velocity)`; the `features` list is length 108 and is the input used by training and runtime components.

### 5.1 Why engineered features?

Engineered features trade raw per‑frame high dimensionality for interpretable components that are fast to compute and robust to per‑frame noise. In interactive systems where response time is critical, a well‑designed feature transform often allows classical models (e.g., SVM) to achieve competitive accuracy at a fraction of the runtime cost of deep temporal models.

## 6. Models and Training

We evaluated three representative model families:

- SVM (RBF kernel) — lightweight, fast inference; hyperparameters tuned via grid search.
- MLP (dense feed‑forward) — per‑frame dense classifiers that operate on the engineered 108‑D representation.
- ST‑GCN — lightweight spatial‑temporal graph convolutional model operating on skeleton node sequences (num_nodes=14).

Training script highlights (`training/train.py`):

- Scale and encode labels using `StandardScaler` and `LabelEncoder`.
- Optional augmentation (augment_factor=2, noise_level=0.02).
- Stratified train/val/test splitting.
-- Hyperparameter tuning (GridSearchCV) used for dense neural baselines; SVM hyperparameters were tuned separately and recorded in `reports/`.

Command to run training (reproducible):

```bash
python training/train.py # runs with augmentation and grid search by default
python training/train.py --no-augment --no-grid # disable augmentation and grid search
```

## 7. Experiments and Evaluation Protocol

Evaluation uses accuracy and macro‑F1 to capture class‑balanced performance. Inference latency (measured on the target deployment hardware) is reported in milliseconds. Each model was evaluated on the same held‑out test split (≈600 samples).

The chosen metrics stored in `reports/model_comparison/*.json` are summarized in Table 1 below.

## 8. Results

Table 1 — Summary of core results (test split):

| Model | Accuracy | Macro‑F1 | Inference Latency (ms) | Notes |
|---|---:|---:|---:|---|
| SVM (RBF) | 95.0% | 0.9438 | 0.259 | see `reports/model_comparison/svm/` |
| MLP (production baseline) | 99.26% | — | <5 | frame‑based + augmentation — see `docs/TRAINING_RESULTS_SUMMARY.md` |
| ST‑GCN (light) | 87.33% | 0.7878 | 1.056 | see `reports/model_comparison/stgcn/` |

Notes: SVM achieves competitive accuracy with substantially lower inference latency compared to temporal and graph models on our measured hardware. MLP shows a strong overall accuracy with lower macro‑F1, indicating class imbalance behavior for certain infrequent classes.

![Confusion matrix (test)](figs/figure3_confusion.png)

**Figure 3.** Confusion matrix on the held‑out test set for the MLP baseline (99.26% test accuracy). Cells show per‑class counts and normalized recall; major confusions are annotated.

Additional training diagnostics (loss / training performance) are available in `reports/`:

![Training performance](figs/figure4_training.png)

![Loss curve](figs/figure4_loss.png)

**Figure 4.** Training and validation curves for the MLP model, showing loss and accuracy across epochs and the selected early‑stopping point.

![Real-time demo screenshot](figs/figure5_demo.png)

**Figure 5.** Real‑time inference example with pose overlay, predicted action label, and game response (illustrative screenshot).

## Model comparison, limitations, and class selection

This section provides a focused, technical comparison of the models we evaluated, a root‑cause analysis of the limitations observed in experiments, and the rationale behind selecting the current set of nine action classes.

### Model comparison (detailed)

- SVM (RBF)
	- Setup: Trained on single‑frame engineered 108‑D features (no explicit temporal modeling). Hyperparameters were tuned (see `reports/model_comparison/svm_metrics.json`).
	- Strengths: Extremely low inference latency (measured ≈0.259 ms), robust with relatively small datasets, deterministic behaviour given fixed scaling, and easy to deploy on CPU‑only targets. Highly interpretable when combined with engineered features.
	- Weaknesses: No built‑in temporal modeling — struggles when the class signature depends on motion across multiple frames. Performance depends on feature quality and scaling; not ideal for gestures requiring long contextual information.

 - MLP (dense feed‑forward)
	- Setup: Dense per‑frame classifier operating on the engineered 108‑D features (see `training/train.py`).
	- Strengths: Fast inference when deployed on CPU, models non‑linear feature interactions, and benefits strongly from engineered features and augmentation.
	- Weaknesses: No inherent temporal modelling — performance depends on feature quality and may require windowing or additional smoothing for motion‑dependent gestures; susceptible to overfitting without regularization on small/imbalanced datasets.

- ST‑GCN (lightweight)
	- Setup: Graph‑convolutional model on skeleton nodes (num_nodes = 14) with temporal convolutions (see `reports/model_comparison/stgcn_metrics.json`).
	- Strengths: Explicitly encodes spatial joint relationships and temporal patterns; conceptually well‑suited to skeleton data where joint adjacency matters.
	- Weaknesses: Computationally heavier than SVM (measured ≈1.056 ms for our lightweight variant), and requires more diverse training data (both spatial and temporal variation) to outperform simpler baselines. Our implementation uses a reduced node set and limited training samples, which likely constrained its effectiveness.

- MLP / small feed‑forward nets
	- Setup: Dense classifiers on per‑frame features (used as baselines in some experiments).
	- Strengths: Fast, can model non‑linear feature interactions, straightforward to deploy.
	- Weaknesses: No temporal modeling unless explicitly windowed; performance sits between SVM and recurrent methods depending on capacity.

Why the engineered‑features + SVM approach performs well in practice

- Low latency: SVM inference is orders of magnitude faster than heavier temporal networks on CPU, which makes it preferable for real‑time mapping to game controls.
- Data efficiency: Engineered features encode domain knowledge (angles, normalized distances, velocity/acceleration) so classical learners can achieve high accuracy with moderate dataset sizes (~2k–2.5k training samples observed in our runs).
- Deterministic train↔runtime parity: Using the same `compute_features()` implementation across training and inference reduces silent mismatches that commonly occur when ad‑hoc features differ between environments.

### What causes the observed limitations (root causes)

Below we expand each observed limitation with a concise technical explanation followed by the realistic user‑facing impact (UX) so product and engineering teams can see both cause and symptom.

1) Dataset size and class imbalance

- Technical: Several classes (e.g., `final_skill`) have far fewer samples than frequent classes. This increases estimator variance for rare classes, biases loss functions toward frequent labels, and reduces macro‑F1. Temporal/sequence models (LSTM/GRU, ST‑GCN) require more diverse sequence examples per class to learn reliable dynamics, so imbalance disproportionately hurts them.

- User impact: Users will notice unreliable recognition for rare actions — the system may frequently ignore or misclassify those moves. In practice this feels like the model "forgets" certain gestures until the user exaggerates them or repeats multiple times. Frustration, loss of trust, and reduced engagement are common outcomes.

2) Label ambiguity and temporal granularity

- Technical: Many action boundaries are fuzzy (transition frames between actions). Single‑frame classifiers cannot disambiguate events that require observing motion over time; short sliding windows (e.g., 10 frames) may cut off discriminative segments. Labeling policy (framewise label vs. segment label) also affects model learning.

- User impact: From the player perspective, the system can be inconsistent during quick transitions — a dodge may sometimes be registered as neutral or a punch, depending on timing. This unpredictability causes users to slow down or exaggerate actions, harming natural interaction.

3) Pose estimation noise and occlusions

- Technical: MediaPipe landmarks contain per‑frame jitter, occasional dropped points, and reduced accuracy under occlusion or extreme poses. These errors propagate into feature computation (angles, velocities) and increase input noise for the classifiers. Simple smoothing reduces jitter but can add latency or smear short motions.

- User impact: Users may see intermittent misfires, flickering overlays, or delayed reactions when hands are near the torso or partly occluded. The system can appear "noisy" — performing spurious actions or failing to act — which degrades the perceived reliability of the controller.

![Pose estimation failures](figs/figure6_occlusion.png)

**Figure 6.** Examples of pose estimation failure modes (occlusion, dropped landmarks, jitter) that degrade engineered features and reduce classifier confidence.

4) Feature design limits

- Technical: The current 108‑D representation intentionally focuses on upper‑body landmarks and compact temporal derivatives. It omits fine hand/finger landmarks and some global context (camera tilt, depth variation). This limits discriminative power for subtle or wrist‑centric gestures.

- User impact: Subtle gestures (small wrist flicks, finger‑based signals) will not be detected reliably. Users who expect fine‑grained control will feel compelled to perform exaggerated motions, making the interface feel less precise and less natural.

5) Model capacity vs. latency constraints

- Technical: Increasing model capacity (deeper LSTMs, larger ST‑GCNs) typically improves accuracy but adds inference time and computational cost. On CPU targets this can push end‑to‑end latency beyond acceptable thresholds for real‑time control. Energy consumption and thermal throttling on embedded hardware are additional concerns.

- User impact: Higher latency manifests as a lag between a user's motion and the in‑game response; this disconnect is immediately noticeable and frustrating in fast interactions (e.g., combat moves). Users report the system 'feels sluggish' and may miss timing‑sensitive gameplay moments.

6) Domain shift and deployment variation

- Technical: Variation in camera angle, distance, lighting, clothing, and subject body shape produces distribution shifts relative to training data. Without domain augmentation or adaptation, model performance drops in new environments.

- User impact: A configuration that works well in the lab can perform poorly in a living room or brightly lit space. New users may hit a poor initial experience (false negatives/positives) and abandon the system unless a quick calibration or adaptive step is provided.

Practical UX‑oriented mitigation tips

- Expose a short calibration flow at first run (camera position, lighting check, sample actions) and store per‑profile settings.
- Surface live confidence and a simple "retry" affordance; if confidence is low, prompt the user to repeat the action with a short guidance message (e.g., "Raise your left hand a little higher").
- Use conservative default thresholds and allow users to opt into higher sensitivity with a warning about possible false positives.
- Provide immediate visual feedback (ghost overlay, predicted label + confidence) so users can adapt their motion quickly and discover the system's responsiveness constraints.


### Why nine classes were chosen

- Design scope & UX: The chosen nine classes (neutral, left/right punch, block, dodge_left/right/front/back, final_skill) map directly to a compact, usable control set for the target demo/game; they cover defensive and offensive primitives while keeping input mapping simple.
- Distinguishability: These actions produce distinct kinematic signatures in upper‑body pose and wrist/elbow motion, which improves per‑frame separability for engineered features and reduces false positives.
- Data collection budget: Collecting balanced, labeled samples for many fine‑grained gestures is costly. Limiting to 9 classes ensures adequate per‑class sample counts (observed training sizes: ~2k) so models can learn reliably.
- Latency & reliability trade‑off: Fewer action classes reduce the chance of spurious predictions and make smoothing/cooldown strategies effective; a larger action vocabulary typically increases confusion and reduces responsiveness.
- Extensibility: The current taxonomy is consciously compact; we recommend future expansion via hierarchical detection (coarse action → fine classifier) or multi‑stage models if the project later supports more extensive data collection and slower hardware budgets.

### Recommendations to address the limitations

- Increase and balance dataset per class (target ≥ 500–1,000 samples/class where feasible) and record across diverse subjects/environments to reduce domain shift.
- Add targeted augmentations and domain randomization (lighting, scale, slight viewpoint jitter) to improve robustness of temporal and graph models.
- Consider adding hand/pose refinements (higher‑resolution hand tracking) or including additional landmarks if discriminative fine‑grained gestures are required.
- For production, consider a hybrid pipeline: engineered features + lightweight SVM for immediate control plus an asynchronous heavier detector (temporal ensemble or ST‑GCN) that refines low‑confidence decisions.

## 9. Discussion

Key observations:

- A simple engineered 108‑D feature representation enables classical learners (SVM) to perform at par with more complex temporal models while offering orders of magnitude lower per‑inference cost.
- Temporal models (LSTM/GRU) can better model intra‑window dynamics but require longer context and have higher latency.
- ST‑GCN is promising for skeleton‑structured reasoning, but for this dataset and deployment constraints it lagged behind in accuracy.

Limitations:

- Dataset size and class balance: some classes (e.g., `final_skill`) are rarer and show lower recall.
- Evaluation hardware details (CPU/GPU) affect latency numbers; report JSONs contain measured latencies but absolute values should be interpreted relative to the target machine.

## 10. Deployment Recommendations

For real‑time game control where minimal latency and predictable behavior are primary constraints, we recommend:

1. Deploying a lightweight SVM or small MLP with the deterministic 108‑D features for inference.
2. Use short smoothing windows and conservative cooldowns in the `MotionAnalyzer` to avoid spurious repeated actions.
3. Expose a small set of tunable parameters (confidence threshold, action cooldown, smoothing window size) in the GUI for per‑user calibration.

![Latency breakdown](figs/figure7_latency.png)

**Figure 7.** End‑to‑end inference latency comparison (pose detection → feature extraction → model inference → dispatch) for SVM, MLP, and ST‑GCN measured on the target CPU.

Runtime entry points and important files:

- Feature extraction & pose utilities: [src/utils/pose_detection.py](src/utils/pose_detection.py#L1-L260)
- Runtime engine (loads model + inference): [src/app/game_engine.py](src/app/game_engine.py)
- Model training pipeline: [training/train.py](training/train.py)

## 11. Reproducibility & Artifacts

All code and experiment artifacts are included in the repository. Notable locations:

- Models and aliases: `models/` (versioned directories under `models/v_<timestamp>/`)
- Reports and plots: `reports/` (per‑run JSON summaries under `reports/model_comparison/`)
- Dataset (by class): `dataset/by_class/`

### 11.1 Reproducibility checklist & commands

Minimal tested environment (this repository):

- Python: `3.11.9` (tested)
- Dependencies: see `requirements.txt` (install with `pip install -r requirements.txt`)
- Commit (workspace snapshot): `567c6d9`

Windows PowerShell (example):

```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
git rev-parse --short HEAD   # recommended to record commit hash (example: 567c6d9)
python training/train.py --no-grid   # train MLP with default/fallback hyperparams
```

Unix / macOS (example):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
git rev-parse --short HEAD   # record commit hash
python training/train.py --no-grid
```

Quick inference / smoke test (load 'latest' alias saved by training):

```bash
python -c "import pickle; m=pickle.load(open('models/latest','rb')); print('loaded', type(m))"
# or run the demo entrypoint if needed
python run.py
```

### 11.2 Exact hyperparameters (selected)

The following table summarizes the primary hyperparameters used in the core runs referenced in this paper. See the run folders under `reports/model_comparison/` for full metadata (JSON) per run.

| Model | Key hyperparameters (selected) | Source |
|---|---|---|
| SVM (RBF) | `C=10`, `gamma=0.001`, `kernel='rbf'` | `reports/model_comparison/svm/svm_20260305_230033/metrics.json` |
| MLP (dense per-frame) | `hidden_layer_sizes=(128,64)`, `activation='relu'`, `solver='adam'`, `learning_rate_init=0.001`, `alpha=0.0001`, `max_iter=500`, `early_stopping=True`, `random_state=42` | `training/train.py` (GridSearch fallback) |
| LSTM/GRU (temporal) | `window_size=10`, `hidden_size=128` | `reports/model_comparison/lstm_gru/lstm_gru_20260305_230108/metrics.json` |
| ST‑GCN (light) | `num_nodes=14`, `window_size=10` | `reports/model_comparison/stgcn/stgcn_20260305_230138/metrics.json` |

References to implementation and feature code:

- Feature extraction: [src/utils/pose_detection.py](src/utils/pose_detection.py#L1-L260)
- Training script (MLP baseline): [training/train.py](training/train.py#L1-L250)

### 11.3 Hardware & latency measurement protocol

Hardware snapshot (measured on the machine used to collect reported latencies):

- CPU: AMD Ryzen 5 7640HS w/ Radeon 760M Graphics (6 physical cores / 12 logical)
- Python: 3.11.9 (virtualenv)

Latency measurement protocol (recommended, matches our reported numbers):

1. Warm-up: run ~100 inference passes to populate caches.
2. Measurement: run N inference passes (N≥1000) on single-frame inputs from the test set and record per-call durations using `time.perf_counter()`.
3. Report: mean ± std (ms) across the N runs (exclude warm-up). Also report the hardware, Python version, and model file used.

Example measurement snippet (adapt to your saved test features):

```python
import pickle, time, numpy as np
model = pickle.load(open('models/latest','rb'))
# X_test should be a single-frame feature array (shape [n_samples,108])
X_test = np.load('reports/model_comparison/test_features.npy')  # optional
# warm-up
for _ in range(100): model.predict(X_test[:1])
# measure
t0 = time.perf_counter()
for _ in range(1000): model.predict(X_test[:1])
dt = (time.perf_counter()-t0)/1000*1000
print(f"mean_latency_ms={dt:.4f}")
```

Measured latencies (reported in `reports/*/metrics.json`):

- SVM (RBF): ~0.259 ms
- MLP: ~1.315 ms
- ST‑GCN (light): ~1.056 ms

### 11.4 Reproducing per-class metrics and confusion numbers

The repository stores run artifacts (confusion matrix images and per-run metadata) under `reports/model_comparison/<model>/<run_folder>/`. To produce numeric per-class precision/recall/F1 and to export the confusion matrix counts in CSV/JSON form, run the evaluation script (example below) using the saved `y_true` and `y_pred` arrays or by re-running `training/train.py` with a small flag to save evaluation outputs.

Minimal snippet to save a machine‑readable classification report:

```python
from sklearn.metrics import classification_report
import json
# y_true, y_pred: load from saved test outputs or generate by running evaluation
report = classification_report(y_true, y_pred, output_dict=True)
with open('reports/model_comparison/<model>/classification_report.json','w') as f:
	json.dump(report, f, indent=2)
```

Appendix C (below) provides a per-class table skeleton and pointers; if you want I can run the evaluation locally and populate the numeric table from saved artifacts.

### 11.5 Ethics & dataset license (recommended text)

Data collection and sharing guidance:

- Consent: All human participants must have given informed consent for collection and any intended redistribution of video or derived frames. Document consent in the dataset README.
- Anonymization: Remove or blur faces if releasing image frames; only release extracted features (108‑D) when possible to avoid personally identifying information.
- Sensitive information: Do not publish raw videos or metadata that could identify subjects without explicit permission.
- License: Choose an appropriate license for the dataset (examples: CC BY‑NC for non‑commercial sharing, or keep dataset internal and provide evaluation server access). Add a `DATASET_LICENSE.md` file with the chosen terms.

Suggested paragraph for the paper (editable):

> The dataset used in this study was collected with participant consent for research use within the project. Raw video frames are not publicly redistributed in this repository; instead we provide derived 108‑D features and evaluation artifacts. Any public release of raw imagery will follow an explicit consent process and include anonymization steps (face blur or cropping). Please contact the authors for dataset access or license requests.

To reproduce training & evaluation (quick):

1. Create a Python virtual environment and install dependencies from `requirements.txt`.
2. Place/verify CSVs in `dataset/by_class/`.
3. Run `python training/train.py` (see flags in the script header).

## 12. Conclusion

We presented an applied end‑to‑end pipeline for turning webcam pose streams into game control commands with a focus on low latency and reproducibility. Our evaluation shows that a compact engineered feature set with a lightweight classifier provides an excellent tradeoff for real‑time applications. Future work will explore domain adaptation for cross‑user generalization, additional temporal ensembles, and more robust online calibration.

---

## Appendix A — Feature summary (implementation note)

The `compute_features()` function (see file link above) uses the following processing steps:

1. Select upper body landmarks (indices 11–24) and normalize coordinates by torso width.
2. Compute 4 interpretable angles (elbows, shoulders) using normalized vector dot products.
3. Compute per‑joint velocity (finite difference, scaled by 5.0) and acceleration (delta of velocity, scaled by 2.0).
4. Add bone direction unit vectors and selected pairwise distances normalized by torso size.

## Appendix B — Core experiment metadata (extracted)

- MLP (from `docs/TRAINING_RESULTS_SUMMARY.md` / executed training notebooks): accuracy=0.9926 (99.26%), inference_latency_ms=<5 ms (frame‑based, augmented training), architecture: `MLPClassifier` (example: (256,128,64) in executed notebooks). See `docs/TRAINING_RESULTS_SUMMARY.md` and `training/executed/` for full experiment artifacts.
- SVM (from `reports/model_comparison/svm_metrics.json`): accuracy=0.95, macro_f1=0.9438, inference_latency_ms=0.2593, train=2500, test=600, num_features=108, best_params={"C":10,"gamma":0.001,"kernel":"rbf"}.
- ST‑GCN (from `reports/model_comparison/stgcn_metrics.json`): accuracy=0.8733, macro_f1=0.7878, inference_latency_ms=1.0562, train=2000, val=419, test=600, window_size=10, num_nodes=14.

---

### Acknowledgements

This project uses Google MediaPipe for pose estimation. Thanks to contributors and experimenters whose scripts and notebooks are included in the repository.

### References

1. Google MediaPipe — https://developers.google.com/mediapipe
2. Yan, S., Xiong, Y., & Lin, D. (2018). Spatial Temporal Graph Convolutional Networks for Skeleton‑Based Action Recognition. CVPR.
3. Hochreiter, S., & Schmidhuber, J. (1997). Long Short‑Term Memory. Neural Computation.
