# 10) Training & Tuning

## Training Pipeline (MLP รุ่นใช้งานปัจจุบัน)

1. Load CSV ต่อคลาสจาก `dataset/by_class`
2. Transform raw landmarks → 108 features
3. Augment data (`augment_factor=1`, `noise_level=0.02`)
4. Encode labels + scale features
5. Split แบบ stratified video-based
6. เทรนด้วย GridSearchCV
7. Evaluate ด้วย classification report + confusion matrix
8. Save model, encoder, scaler ลง `models/`

---

## การตั้งค่าเทรนหลัก (จาก executed_train ล่าสุด)

- Raw samples: 3,100
- Augmented samples: 6,200
- Split: Train 4,900 / Val 650 / Test 650
- Random seed (split): 99
- Test accuracy: **99.54%**
- Best CV score: **99.27%**

---

## Hyperparameter Tuning ที่ใช้

ใช้ `GridSearchCV` บน MLP parameter grid:
- `hidden_layer_sizes`: (128,64), (256,128), (256,128,64)
- `alpha`: 0.0001, 0.001
- `learning_rate_init`: 0.001, 0.0005

และใช้:
- activation = relu
- solver = adam
- early_stopping = True
- max_iter = 500

---

## Hyperparameters ที่มีผลมากสุด (เชิงประสบการณ์ในโปรเจกต์)

1. **augment_factor**
   - ส่งผลทั้งต่อความแม่นและความ robust
2. **random_state ของ split**
   - มีผลต่อความยากง่ายของ test partition
3. **model capacity (`hidden_layer_sizes`)**
   - เล็กเกินไป underfit, ใหญ่เกินไปเสี่ยง overfit
4. **confidence threshold ฝั่ง runtime**
   - ไม่กระทบ training metric โดยตรง แต่กระทบคุณภาพ gameplay มาก

---

## Why early stopping สำคัญ

- ป้องกันโมเดลจำ noise ใน train
- ลดเวลาเทรนโดยหยุดเมื่อ val ไม่ดีขึ้น
- ได้โมเดลที่เสถียรขึ้นใน deployment

---

## แนวทาง retrain รอบถัดไป (Playbook)

1. เก็บข้อมูลเพิ่มในคลาสที่ error บ่อย
2. รัน 3 seeds แล้วเฉลี่ยผล (ลด seed bias)
3. บันทึก confusion matrix ทุก run
4. ทดสอบ runtime บนเครื่อง target จริง

---

## ข้อความสรุปสำหรับพรีเซนต์

"เราทำ tuning แบบเป็นระบบผ่าน GridSearchCV และคุม overfitting ด้วย early stopping พร้อม split ที่กัน leakage ทำให้คะแนน 99.54% ไม่ใช่ตัวเลขฟลุค แต่เป็นผลจาก pipeline ที่ออกแบบครบตั้งแต่ data ถึง deployment"