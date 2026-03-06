# 07) Data Split & Leakage Prevention

## ทำไมเรื่อง Split สำคัญมาก

ถ้า split ผิด แม้โมเดลได้ accuracy สูง ก็อาจเป็นคะแนนหลอก

ในงาน pose sequence ถ้า split แบบสุ่มรายเฟรม:
- เฟรมใกล้เคียงจากคลิปเดียวกันอาจไปอยู่ทั้ง train และ test
- โมเดลจำ pattern เฉพาะคลิปได้ง่าย
- test accuracy สูงเกินจริง (data leakage)

---

## แนวคิด Video-Based Split

โครงการนี้ใช้หลักการ:
1. จัดข้อมูลเป็น chunk ตามลำดับเวลา (`chunk_size=50`)
2. split ในระดับ chunk ไม่ใช่ sample เดี่ยว
3. ทำให้เฟรมจากวิดีโอเดียวกันไม่ข้าม train/test

ใน MLP run ล่าสุด (`executed_train.ipynb`):
- Total หลัง augment: 6,200
- Train: 4,900
- Val: 650
- Test: 650

---

## ค่าที่ใช้จริงใน notebook ล่าสุด

- `test_size=0.15`
- `val_size=0.15`
- `chunk_size=50`
- `random_state=99`

---

## ความเสี่ยง leakage ถ้า split ผิด

1. **Temporal leakage**: เฟรมคล้ายกันมากอยู่คนละ split
2. **Augmentation leakage**: ตัวอย่าง augment ที่คล้ายต้นฉบับหลุดไป test
3. **Class coverage leakage**: บางคลาสหายจาก test โดยไม่รู้ตัว

---

## วิธีป้องกัน leakage ที่ใช้แล้วในโปรเจกต์

1. video-based chunk splitting
2. stratified ต่อคลาส (ดูหัวข้อ 08)
3. ตรวจ class distribution หลัง split ทุกครั้ง
4. อ่าน confusion matrix + per-class metrics ไม่พึ่ง accuracy รวมอย่างเดียว

---

## Checklist ก่อนประกาศผลโมเดล

1. test set มีครบทุกคลาสหรือไม่
2. split logic ทำงานระดับ video chunk จริงหรือไม่
3. run ซ้ำหลาย seed แล้วยังนิ่งหรือไม่
4. metric รายคลาสสอดคล้องกับ use case เกมหรือไม่

---

## ข้อความสรุปสำหรับเวทีพรีเซนต์

"คะแนนที่ได้สูงเพราะโมเดลเก่งจริง ไม่ใช่เพราะ leakage เนื่องจากเรา split แบบ video-based และตรวจ class coverage ทุกครั้ง จึงมั่นใจได้ว่าผลประเมินสะท้อนการใช้งานจริงมากกว่า split แบบสุ่มทั่วไป"