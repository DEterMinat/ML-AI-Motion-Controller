# Experiment Plan — ML-AI Motion Controller (NINFaceNet)

**Due:** 23 February 2026  
**Project:** Real-time Pose-Based Game Controller  
**Task:** 9-Class Action Classification from 108 Skeleton Features via Webcam  
**Classes:** `neutral`, `left_punch`, `right_punch`, `block`, `dodge_left`, `dodge_right`, `dodge_front`, `dodge_back`, `final_skill`

---

## 1. Baseline Model

### 1.1 Input Feature Engineering

ก่อนเข้าโมเดล ข้อมูลดิบ 132 ค่าจาก MediaPipe (33 landmarks × 4 ค่า) จะถูก transform เป็น **108 Pro-Level Features** ดังนี้:

| Feature Group                            | ขนาด    | รายละเอียด              |
| ---------------------------------------- | ------- | ----------------------- |
| Body Landmarks (14 จุดบนร่างกาย × 4 ค่า) | 56      | x, y, z, visibility     |
| Key Angles                               | 4       | ข้อศอก L/R, ข้อไหล่ L/R |
| Velocity (4 จุด × 3 ค่า)                 | 12      | ∆position ระหว่างเฟรม   |
| Bone Vectors (6 กระดูก × 3 ค่า)          | 18      | ทิศทางของแต่ละ segment  |
| Acceleration (4 จุด × 3 ค่า)             | 12      | ∆velocity ระหว่างเฟรม   |
| Distance Features                        | 6       | ระยะห่างระหว่างจุดสำคัญ |
| **รวม**                                  | **108** |                         |

### 1.2 Baseline: MLP Classifier (Frame-by-Frame)

| รายการ               | ค่า                                                   |
| -------------------- | ----------------------------------------------------- |
| Architecture         | Multi-Layer Perceptron (scikit-learn `MLPClassifier`) |
| Input                | 108 features / frame                                  |
| Hidden Layers        | (128, 64)                                             |
| Activation           | ReLU                                                  |
| Solver               | Adam                                                  |
| Learning Rate Init   | 0.001                                                 |
| Max Iterations       | 500                                                   |
| Early Stopping       | ✅                                                    |
| Preprocessing        | `StandardScaler`                                      |
| Train/Val/Test Split | 70% / 15% / 15%                                       |

**ไม่มี temporal context** — แต่ละเฟรมทำนายอิสระจากกัน (snapshot-based)

---

## 2. Hyperparameters

### 2.1 MLP (Baseline) — ค่าที่ทดสอบด้วย GridSearchCV

```python
param_grid = {
    'hidden_layer_sizes': [(128, 64), (256, 128), (256, 128, 64)],
    'alpha':              [0.0001, 0.001],
    'learning_rate_init': [0.001, 0.0005]
}
# cv=3, scoring='accuracy', n_jobs=-1
```

> รวมทั้งหมด **12 combination** ทดสอบด้วย 3-Fold CV

### 2.2 Data Augmentation — ค่าคงที่

| Parameter            | ค่า                                          |
| -------------------- | -------------------------------------------- |
| `augment_factor`     | 2 (copies ต่อ 1 sample ต้นฉบับ)              |
| `noise_level`        | 0.02 (Gaussian σ = 2%)                       |
| `use_scale` (p=0.3)  | ±10% scale                                   |
| `use_mirror` (p=0.3) | swap left/right (ยกเว้น directional actions) |

---

## 3. Evaluation Metrics

### 3.1 Primary Metrics

| Metric                           | สูตร                   | เหตุผลที่เลือก        |
| -------------------------------- | ---------------------- | --------------------- |
| **Accuracy**                     | Correct / Total        | ภาพรวมความถูกต้อง     |
| **F1-Score (Macro)**             | Avg F1 per class       | class ไม่ balanced    |
| **Per-Class Precision / Recall** | TP/(TP+FP), TP/(TP+FN) | ดู error per action   |
| **Confusion Matrix**             | Heatmap 9×9            | ดู action ที่สับสนกัน |

### 3.2 Real-time Performance Metrics

สำคัญไม่แพกัน เพราะระบบ inference แบบ real-time บน webcam:

| Metric                | Target        | วิธีวัด                     |
| --------------------- | ------------- | --------------------------- |
| **App FPS**           | ≥ 30 fps      | `FPSLimiter.get_fps()`      |
| **Camera FPS**        | ≥ 30 fps      | `CameraStream.get_fps()`    |
| **Inference Latency** | < 15 ms/frame | `time.perf_counter()`       |
| **Action Confidence** | ≥ 0.80        | `model.predict_proba()` max |

### 3.3 Human Evaluation (Game-Context)

| Metric                      | วิธี                                                   |
| --------------------------- | ------------------------------------------------------ |
| **Responsiveness**          | เวลาตั้งแต่ทำท่า → key ถูกกด (Human-perceived latency) |
| **False Trigger Rate**      | ครั้งที่ระบบ trigger action ผิด / นาที ขณะ neutral     |
| **Action Recognition Rate** | % ท่าที่ทำแล้วระบบ detect ถูกใน 5 รอบทดสอบ             |

---

## 4. Experiment Variations

### Exp-1: Baseline (No Augmentation + No GridSearch)

> เป้าหมาย: หา **lower bound** ของ performance

```
Model:   MLP(128, 64)
Data:    Raw samples only (no augmentation)
Search:  No GridSearchCV — default hyperparameters
```

**คาดการณ์:** Accuracy ~ 85–90%

---

### Exp-2: Baseline + Augmentation (Official Baseline)

> เป้าหมาย: วัด impact ของ data augmentation

```
Model:   MLP(128, 64)
Data:    Original + Augmented (factor=2, noise=0.02)
Search:  No GridSearchCV
```

**คาดการณ์:** Accuracy ~ 90–95%

---

### Exp-3: MLP + GridSearchCV (Best MLP)

> เป้าหมาย: หา hyperparameter ที่ดีที่สุดสำหรับ MLP

```
Model:   MLPClassifier + GridSearchCV (12 combinations, 3-Fold CV)
Data:    Original + Augmented
Search:  hidden_layer_sizes, alpha, learning_rate_init
```

**คาดการณ์:** Accuracy ~ 93–97%  
**Trade-off:** Training time นาน (~10–30 นาที)

---

### สรุปเปรียบเทียบ

| Experiment | Model        | Augment | Tuning        | คาดการณ์ Accuracy |
| ---------- | ------------ | ------- | ------------- | ----------------- |
| Exp-1      | MLP (128,64) | ❌      | ❌            | ~85–90%           |
| Exp-2      | MLP (128,64) | ✅      | ❌            | ~90–95%           |
| Exp-3      | MLP (best)   | ✅      | ✅ GridSearch | ~93–97%           |

---

## 5. Run Commands

```bash
# Exp-1: MLP baseline (ไม่ augment, ไม่ grid)
python training/train.py --no-augment --no-grid

# Exp-2: MLP + Augmentation
python training/train.py --no-grid

# Exp-3: MLP + Augmentation + GridSearchCV (default)
python training/train.py
```

---

_เอกสารนี้จัดทำขึ้นตาม codebase จริงใน `training/train.py`, `src/model/temporal_model.py`, `src/data/augmentation.py`_
