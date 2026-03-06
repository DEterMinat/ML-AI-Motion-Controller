# Training Results Summary - All Models

**Date**: 2025-03-05  
**Split Method**: Video-Based Split (chunk_size=50, no data leakage)  
**Dataset**: 3,100 samples, 9 classes (boxing actions)

---

## 📊 Quick Results

| Rank | Model | Test Accuracy | Training Method | Inference Time |
|------|-------|--------------|-----------------|----------------|
| 🥇 1 | **MLP** | **99.26%** | Frame-based + Augmentation (2x data) | <5ms (CPU) |
| 🥈 2 | **Transformer** | **99.12%** | Temporal sequences (10 frames) | ~10ms (CPU) |
| 🥉 3 | **LSTM/GRU** | **95.50%** | BiLSTM+GRU, temporal patterns | 15-20ms (CPU) |
| 4 | **SVM** | **95.00%** | Baseline, RBF kernel | <2ms (CPU) |
| 5 | **ST-GCN** | **87.33%** | Graph convolution on skeleton | ~15ms (GPU) |

---

## 📁 Model Files

### MLP (99.26%)
- **Location**: `models/boxing_model.pkl`, `models/label_encoder.pkl`, `models/scaler.pkl`
- **Notebook**: [training/executed/executed_train.ipynb](../training/executed/executed_train.ipynb)
- **Features**: 108 engineered features (angles, velocities, distances)
- **Architecture**: MLPClassifier (256, 128, 64), early stopping
- **Training**: GridSearchCV with data augmentation (noise, scale, mirror)

### Transformer (99.12%)
- **Location**: `models/boxing_model.pkl` (latest), `models/label_encoder.pkl`
- **Notebook**: [training/executed/executed_train_temporal.ipynb](../training/executed/executed_train_temporal.ipynb)
- **Features**: 108 features × 10 frames = (10, 108) sequences
- **Architecture**: PoseTransformerWrapper (custom), 50 epochs
- **Training**: Attention mechanism on temporal sequences

### LSTM/GRU (95.50%)
- **Location**: `reports/model_comparison/lstm_gru/lstm_gru_20260305_230108/`
- **Notebook**: [training/executed/executed_train_lstm_gru.ipynb](../training/executed/executed_train_lstm_gru.ipynb)
- **Features**: 108 features × 10 frames sequences
- **Architecture**: BiLSTM(128) + GRU(128) + Dense(64, 9)
- **Training**: 30 epochs, early stopping (patience=6), batch_size=32

### SVM (95.00%)
- **Location**: `reports/model_comparison/svm/svm_20260305_230033/`
- **Notebook**: [training/executed/executed_train_svm.ipynb](../training/executed/executed_train_svm.ipynb)
- **Features**: 108 static features (frame-by-frame)
- **Architecture**: SVC with RBF kernel
- **Training**: GridSearchCV, C=10, gamma=0.1

### ST-GCN (87.33%)
- **Location**: `reports/model_comparison/stgcn/stgcn_20260305_230138/`
- **Notebook**: [training/executed/executed_train_stgcn.ipynb](../training/executed/executed_train_stgcn.ipynb)
- **Features**: 14 body landmarks × 4 values (x,y,z,v) + skeleton graph
- **Architecture**: Spatial-Temporal Graph Convolutional Network
- **Training**: 30 epochs, batch_size=32, learning_rate=0.001

---

## 🎯 Key Insights

### Why MLP & Transformer Excel?
1. **Data Augmentation**: 2x training samples with noise, scaling, mirroring
2. **Feature Engineering**: 108 domain-specific features (not just raw landmarks)
3. **Temporal Context** (Transformer): 10-frame sequences capture motion dynamics

### Why ST-GCN Lower?
1. **Complex Model + Small Dataset**: ST-GCN needs 10k+ samples to shine
2. **Most Affected by Honest Split**: Graph models memorize more → honest split hurts more
3. **No Augmentation**: Currently not using data augmentation for ST-GCN

### Video-Based Split Impact
**Old Results** (random split with data leakage):
- SVM: 100% (overfitted)
- LSTM/GRU: 99.83% (overfitted)
- ST-GCN: 100% (overfitted)

**New Results** (video-based split, honest):
- SVM: 95.00% (-5%)
- LSTM/GRU: 95.50% (-4.33%)
- ST-GCN: 87.33% (-12.67%)

**Accuracy drop is EXPECTED and GOOD** - it proves models now generalize to unseen video chunks!

---

## 🚀 Production Recommendations

### For Real-Time Game (Low Latency Required)
**Use MLP** - 99.26% accuracy, <5ms inference, simple deployment

### For Best Accuracy with Temporal Understanding
**Use Transformer** - 99.12% accuracy, understands motion sequences

### For Baseline/Comparison
**Use SVM** - 95.00% accuracy, fastest inference (<2ms)

### For Research/Future Work
**Use ST-GCN** - Improve with more data + augmentation

---

## 📝 Training Details

### Common Settings
- **Split**: video_based_split(chunk_size=50, test_size=0.2)
- **Features**: 108 engineered (from 14 body landmarks)
- **Classes**: 9 boxing actions
  - `neutral`, `block`, `final_skill`
  - `left_punch`, `right_punch`
  - `dodge_left`, `dodge_right`, `dodge_front`, `dodge_back`

### Data Augmentation (MLP, Transformer)
- **Augment Factor**: 2x
- **Noise Level**: σ = 0.02 (2% Gaussian)
- **Scale**: ±10% (p=0.3)
- **Mirror**: Swap L/R (p=0.3, exclude directional)

### Validation Split
- **MLP**: 70% train / 15% val / 15% test
- **Deep Models**: 68% train / 12% val / 20% test
- **SVM**: 80% train / 20% test (CV in GridSearchCV)

---

## ✅ Verified Production-Ready

All models trained with:
- ✅ No data leakage (video-based split)
- ✅ Honest evaluation on unseen video chunks
- ✅ All notebooks print "⚠️ Using VIDEO-BASED SPLIT (no data leakage)"
- ✅ Results archived in `training/executed/`

---

## 📚 Related Documentation

- [OVERFITTING_ANALYSIS.md](OVERFITTING_ANALYSIS.md) - Data leakage problem & solution
- [RESULTS.md](RESULTS.md) - Detailed analysis & comparison
- [experiment_plan.md](experiment_plan.md) - Training methodology
- [model_explanation.md](model_explanation.md) - Architecture details

---

**Status**: ✅ All 5 models trained and validated  
**Ready for**: Production deployment and real-time game integration
