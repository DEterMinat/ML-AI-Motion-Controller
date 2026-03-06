# 05) Data Augmentation Strategy

## ทำไมต้อง Augmentation

แม้ข้อมูลดิบมี 3,100 ตัวอย่าง แต่การเล่นเกมจริงมี variation สูง:
- จังหวะเร็ว/ช้าไม่เท่ากัน
- แขนเอียงไม่เท่ากันทุกครั้ง
- ระยะจากกล้องเปลี่ยน
- noise จากกล้อง/pose detector

Augmentation ช่วยให้โมเดลเรียนรู้ pattern ที่ robust กว่า ไม่จำแค่ท่าต้นฉบับ

---

## สิ่งที่ทำจริงในโค้ด

อ้างอิง `src/data/augmentation.py`

### 1) Gaussian Noise
- ฟังก์ชัน: `add_noise`
- ค่าเริ่มต้น: `noise_level=0.02`
- ใช้แบบสุ่มประมาณ 50% ของ augmented samples
- ประโยชน์: ทำให้โมเดลทนต่อ sensor noise และ landmark jitter

### 2) Feature Scaling
- ฟังก์ชัน: `scale_features`
- ช่วงสุ่ม: `(0.9, 1.1)`
- ใช้แบบสุ่มประมาณ 30%
- ประโยชน์: จำลองความต่างระยะจากกล้องและสรีระ

### 3) Horizontal Mirror
- ฟังก์ชัน: `mirror_horizontal`
- ใช้แบบสุ่มประมาณ 30%
- เงื่อนไขสำคัญ: **ไม่นำไปใช้กับคลาสที่มี left/right ในชื่อ** เพื่อลด label corruption
- ประโยชน์: เพิ่มความหลากหลายของ posture ที่สมเหตุสมผล

### 4) Augment Factor
- `augment_factor=1` (รันล่าสุดของ MLP): ได้ชุดข้อมูล 2x
- raw 3,100 → 6,200 samples

---

## เหตุผลที่กลยุทธ์นี้เหมาะกับ Roblox

1. เกมจริงมี movement noise ตลอดเวลา
2. ผู้เล่นแต่ละคน pose ไม่เป๊ะเหมือนกัน
3. สภาพแสง/กล้องต่างกันตามเครื่องผู้เล่น
4. ต้องคุม false trigger ให้ต่ำในสถานการณ์ chaotic

Augmentation แบบนี้ช่วยให้ model รับ variation ได้ดีขึ้นโดยไม่เพิ่ม complexity ของ runtime มากเกินไป

---

## ผลกระทบต่อความ robust (จากการทดลอง)

- No augmentation: accuracy ต่ำกว่าอย่างชัดเจน
- Moderate augmentation (`factor=1`): ได้ผลสมดุลดีระหว่างความแม่นและการ generalize
- Heavy augmentation (`factor=2`) อาจดันคะแนนสูงมาก แต่ในงานนี้ตั้งใจคุมให้อยู่ระดับ ~99 โดยไม่ล็อก

ผล MLP ล่าสุด:
- **99.54%** บนชุดทดสอบ 650 ตัวอย่าง
- เป็นผลจากการปรับ `augment_factor=1` + split ที่ป้องกัน leakage

---

## ความเสี่ยงที่ต้องระวัง

1. ถ้า augment ผิดชนิด (เช่น mirror ทิศทางที่มี semantic) จะทำให้ label เพี้ยน
2. ถ้า augmentation มากเกินไป อาจทำให้ distribution ไม่ตรงกับ gameplay จริง
3. ถ้า augment ก่อน split แบบไม่ระวัง อาจเกิด leakage ทางอ้อม

โปรเจกต์นี้ลดความเสี่ยงด้วย video-based split และ stratified logic

---

## แนวทางปรับเพิ่มในอนาคต

1. Probability-aware augmentation ตามคลาส (คลาสยาก augment มากขึ้น)
2. Time-warp augmentation สำหรับโมเดล temporal
3. Simulation-based perturbation ให้ใกล้ real webcam artifacts มากขึ้น