# 08) Critical Fix: Stratified Video-Based Split

## ปัญหาวิกฤตที่เจอ

ในช่วงก่อนแก้ระบบ split พบว่า:
- test set มีแค่ 7 จาก 9 คลาส
- คลาสที่หายคือ `dodge_right` และ `left_punch`
- accuracy สูงมากแต่ไม่สะท้อนความจริง เพราะไม่ได้ทดสอบครบ action

นี่เป็นปัญหาเชิงคุณภาพการประเมินที่สำคัญที่สุดของโปรเจกต์

---

## Root Cause

สาเหตุหลักคือ split แบบ chunk ที่ยัง **ไม่ stratify ต่อคลาส**:
1. shuffle chunk ทั้งก้อนรวมกัน
2. แบ่ง train/val/test ทีเดียว
3. มีโอกาสที่บางคลาสจะไม่ถูกสุ่มเข้า test เลย

---

## วิธีแก้ที่นำไปใช้

แก้ `video_based_split()` ให้ทำงานแบบ **stratified-by-class**:
1. วนทีละคลาส
2. สร้าง chunk ภายในคลาสนั้น
3. แบ่ง chunk เป็น train/val/test ต่อคลาส
4. บังคับให้แต่ละ split มีอย่างน้อย 1 chunk (เมื่อข้อมูลพอ)

ผลคือ test set มีตัวแทนครบทุกคลาสแน่นอน

---

## ทำไมผลใหม่น่าเชื่อถือกว่า

1. ครอบคลุม action ครบ 9 คลาส
2. ลด bias จาก class omission
3. ลดโอกาสคะแนนหลอกสูงจากการทดสอบไม่ครบ
4. สอดคล้องกับเป้าหมายเกมจริงที่ต้องเจอทุก action

---

## ผลหลังแก้ (snapshot ล่าสุดที่ใช้งาน)

- MLP: **99.54%**
- Transformer: **97.45%**
- LSTM/GRU: **95.50%**
- SVM: **95.00%**
- ST-GCN: **87.33%**

จุดสำคัญไม่ใช่แค่ตัวเลขสูง แต่เป็นตัวเลขที่ **ประเมินบน test ที่ครบคลาสและกัน leakage แล้ว**

---

## Lesson Learned (ควรพูดในพรีเซนต์)

1. Accuracy สูงไม่ได้แปลว่า evaluation ถูกเสมอ
2. ในงาน multi-class ต้องตรวจ class coverage ทุก split
3. data pipeline quality สำคัญเท่ากับ model architecture
4. critical fix ที่ถูกจุด ทำให้ผลทั้งโปรเจกต์น่าเชื่อถือขึ้นทันที

---

## แนวปฏิบัติถาวรหลังจากนี้

1. ทุกครั้งที่ retrain ต้องพิมพ์ class distribution ของ train/val/test
2. ตั้ง regression test สำหรับ split function
3. เก็บรายงานก่อน/หลังแก้ split เพื่อ audit ได้
4. ถ้าขยาย dataset ให้ตรวจ edge case ของคลาสเล็กเสมอ