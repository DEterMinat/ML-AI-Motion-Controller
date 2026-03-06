# 11) Evaluation Results

## Snapshot ผลประเมินล่าสุด (Current Benchmark)

| Model | Test Accuracy | หมายเหตุ |
|---|---:|---|
| **MLP** | **99.54%** | `executed_train.ipynb` (6200 samples after augmentation) |
| **Transformer** | **97.45%** | `executed_train_temporal.ipynb` |
| **LSTM/GRU** | **95.50%** | `executed_train_lstm_gru.ipynb` |
| **SVM** | **95.00%** | `executed_train_svm.ipynb` |
| **ST-GCN** | **87.33%** | `executed_train_stgcn.ipynb` |

---

## รายละเอียด MLP (โมเดลใช้งานปัจจุบัน)

ผลจาก `training/executed/executed_train.ipynb`:
- Best CV Score: **99.27%**
- Test Accuracy: **99.54%**
- Support (test): 650

### Per-class report (MLP)

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| block | 1.00 | 1.00 | 1.00 | 150 |
| dodge_back | 1.00 | 1.00 | 1.00 | 50 |
| dodge_front | 1.00 | 0.94 | 0.97 | 50 |
| dodge_left | 0.98 | 1.00 | 0.99 | 50 |
| dodge_right | 0.96 | 1.00 | 0.98 | 50 |
| final_skill | 1.00 | 1.00 | 1.00 | 50 |
| left_punch | 1.00 | 1.00 | 1.00 | 50 |
| neutral | 1.00 | 1.00 | 1.00 | 150 |
| right_punch | 1.00 | 1.00 | 1.00 | 50 |

**Insight หลัก:** คลาสที่ท้าทายสุดคือ `dodge_front` (recall ต่ำกว่าเพื่อน) ซึ่งสะท้อนว่าท่าหลบหน้าอาจ overlap กับ transition pose บางช่วงของ dodge ฝั่งซ้าย/ขวา

---

## ภาพรวม Precision/Recall ของโมเดลอื่น

### Transformer (97.45%)
- จุดแข็ง: block, dodge_back, dodge_right, final_skill, left_punch ได้ระดับสูงมาก
- จุดที่ตก: neutral และ right_punch บางส่วน
- เหมาะเป็น candidate รุ่นถัดไปที่เน้น temporal robustness

### SVM (95.00%)
- Macro F1: **0.9438**
- เป็น baseline ที่ดีและตีความง่าย

### LSTM/GRU (95.50%)
- Macro F1: **0.8469**
- temporal model แบบ recurrent ให้ผลเสถียร แต่ยังสู้ MLP/Transformer ไม่ได้ในชุดข้อมูลนี้

### ST-GCN (87.33%)
- Macro F1: **0.7878**
- ชี้ว่า graph model ยังต้องการข้อมูลหรือ tuning เพิ่มเพื่อดึงศักยภาพ

---

## Confusion Matrix: วิธีเล่าให้คนฟังเข้าใจง่าย

1. เส้นทแยงมุมเข้ม = โมเดลทายถูกเป็นส่วนใหญ่
2. ช่องนอกทแยงมุม = ความสับสนระหว่าง action คล้ายกัน
3. ดูเฉพาะ accuracy ไม่พอ ต้องอ่าน per-class ด้วย
4. ความผิดพลาดระดับเล็กน้อยในคลาส dodge ยังรับได้ถ้า gameplay ลื่นและไม่ trigger ผิดซ้ำ

---

## ข้อสรุปเชิงธุรกิจ/เกม

- ระบบพร้อมใช้งานในโหมด production pilot
- ค่า accuracy รวมสูงมากและรายคลาสส่วนใหญ่ใกล้เพดาน
- bottleneck ต่อจากนี้คือ generalization ข้ามผู้เล่น/สภาพแวดล้อม มากกว่า architecture หลัก

---

## Suggested Slide Layout (หัวข้อนี้)

- Slide A: ตารางเทียบ 5 โมเดล
- Slide B: MLP per-class metrics + confusion matrix
- Slide C: Insight + decision (ทำไมเลือก MLP สำหรับ production)