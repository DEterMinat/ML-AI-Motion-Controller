# Training Folder Structure

**Last Updated**: 2025-03-05 (After Video-Based Split Implementation)

---

## 📁 Current Structure

```
training/
├── executed/                          ← ✅ LATEST HONEST RESULTS (Video-based split)
│   ├── executed_train_svm.ipynb
│   ├── executed_train_lstm_gru.ipynb
│   └── executed_train_stgcn.ipynb
│
├── archive_old_results/               ← ⚠️  ARCHIVED (Data leakage - DO NOT USE)
│   └── executed_with_leakage/
│       ├── executed_train_svm.ipynb   (100% accuracy - overfitted)
│       ├── executed_train_lstm_gru.ipynb
│       └── executed_train_stgcn.ipynb
│
├── train_svm.ipynb                    ← Training notebooks (updated with video_based_split)
├── train_lstm_gru.ipynb
├── train_stgcn.ipynb
├── train.ipynb                        ← MLP training (updated)
├── train_temporal.ipynb               ← Transformer training (updated)
└── model_comparison_summary.ipynb     ← Results comparison notebook
```

---

## 🎯 Which Results to Use?

### ✅ **USE THESE** - Honest Results (No Data Leakage)
- **Location**: `training/executed/`
- **Split Method**: Video-based split (chunk_size=50)
- **Accuracy**:
  - SVM: **95.00%** (honest)
  - LSTM/GRU: **95.50%** (honest)
  - ST-GCN: **87.33%** (honest)
- **Status**: Production-ready, validates on truly unseen video chunks

### ❌ **DO NOT USE** - Old Results (Data Leakage)
- **Location**: `training/archive_old_results/executed_with_leakage/`
- **Split Method**: Random frame split (WRONG!)
- **Accuracy**: 99-100% (too good to be true - overfitted)
- **Problem**: Sequential frames from same video split into train AND test sets
- **Status**: Archived for reference only

---

## 📊 Model Artifacts

Latest trained models are saved in:
```
models/model_comparison/
├── svm/
│   └── svm_YYYYMMDD_HHMMSS/
│       ├── svm_model.pkl
│       ├── svm_scaler.pkl
│       └── svm_label_encoder.pkl
├── lstm_gru/
│   └── lstm_gru_YYYYMMDD_HHMMSS/
│       ├── lstm_gru_model.pt
│       ├── lstm_gru_scaler.pkl
│       └── lstm_gru_label_encoder.pkl
└── stgcn/
    └── stgcn_YYYYMMDD_HHMMSS/
        ├── stgcn_model.pt
        ├── stgcn_scaler.pkl
        └── stgcn_label_encoder.pkl
```

**Old models** (trained with data leakage) moved to: `models/archive_old_models/`

---

## 🔧 How Training Works Now

### 1. Data Split (Video-Based)
```python
from src.data.processing import video_based_split

# Splits by video chunks, not by random frames
X_train, X_val, X_test, y_train, y_val, y_test = video_based_split(
    X, y, test_size=0.2, val_size=0.15, chunk_size=50, random_state=42
)
```

**Key Parameters**:
- `chunk_size=50`: Assumes ~50 consecutive frames per video segment
- `test_size=0.2`: 20% of video chunks for testing
- `val_size=0.15`: 15% of video chunks for validation

### 2. Why This Matters
**OLD (WRONG)**:
```
Video1: [Frame1, Frame2, Frame3, ..., Frame100]
         ↓ random split
Train: [Frame1, Frame3, Frame5, ...]  ← Frame1 at 10:00:01
Test:  [Frame2, Frame4, Frame6, ...]  ← Frame2 at 10:00:01 (almost identical!)
Result: 100% accuracy (overfitted due to data leakage)
```

**NEW (CORRECT)**:
```
Videos: [Chunk1, Chunk2, Chunk3, ..., ChunkN]
         ↓ split by chunk
Train: [Chunk1, Chunk2, Chunk3]  (all frames from these chunks)
Test:  [ChunkN-1, ChunkN]        (completely different video segments)
Result: 87-95% accuracy (honest generalization)
```

---

## 📈 Training Timeline

| Date | Event | Accuracy (Old) | Accuracy (New) |
|------|-------|----------------|----------------|
| Before 2026-03-05 | Random frame split | SVM: 100%, LSTM: 99.83%, ST-GCN: 100% | N/A |
| 2026-03-05 | Implemented video_based_split | Archived | SVM: 95%, LSTM: 95.5%, ST-GCN: 87.33% |

**Accuracy dropped 4-13%** → This is **EXPECTED and GOOD**! Lower accuracy = more honest evaluation.

---

## 🚀 Running Training

### Train Individual Models
```bash
# Activate environment
.venv\Scripts\Activate.ps1

# Train SVM
cd training
jupyter nbconvert --to notebook --execute train_svm.ipynb --output executed/executed_train_svm.ipynb --ExecutePreprocessor.timeout=600

# Train LSTM/GRU
jupyter nbconvert --to notebook --execute train_lstm_gru.ipynb --output executed/executed_train_lstm_gru.ipynb --ExecutePreprocessor.timeout=900

# Train ST-GCN
jupyter nbconvert --to notebook --execute train_stgcn.ipynb --output executed/executed_train_stgcn.ipynb --ExecutePreprocessor.timeout=900
```

### Train All Models (One-Click)
```bash
cd training
jupyter nbconvert --to notebook --execute run_all_model_comparison_one_click.ipynb
```

---

## 📝 Notes for Future Development

### If Accuracy Needs Improvement
1. **Collect more diverse data**: Different users, angles, lighting
2. **Increase chunk_size**: Try 100-150 instead of 50
3. **Adjust STEP_SIZE**: Use larger steps (10-20) to reduce sequence overlap
4. **Add real video IDs**: Currently using pseudo-chunks; real video metadata would be better
5. **Data augmentation**: Add rotation, scaling, noise (already implemented but can tune)

### If Adding New Models
Update these notebooks:
- `train_<model_name>.ipynb` - Individual training notebook
- `run_all_model_comparison_one_click.ipynb` - Add to pipeline
- `model_comparison_summary.ipynb` - Add to comparison charts

---

## 🔍 Verification

To verify you're using correct results:
```bash
# Check for video-based split warning
grep -r "VIDEO-BASED SPLIT" training/executed/*.ipynb

# Check accuracy is NOT 100%
grep -r "Test Accuracy" training/executed/*.ipynb
```

Expected output:
```
SVM: Test Accuracy: 0.9500 (95%)
LSTM/GRU: Test Accuracy: 0.9550 (95.5%)
ST-GCN: Test Accuracy: 0.8733 (87.33%)
```

---

## 📚 Related Documentation

- [OVERFITTING_ANALYSIS.md](../docs/OVERFITTING_ANALYSIS.md) - Detailed analysis of data leakage problem
- [RESULTS.md](../docs/RESULTS.md) - Model comparison results
- [experiment_plan.md](../docs/experiment_plan.md) - Training strategy
