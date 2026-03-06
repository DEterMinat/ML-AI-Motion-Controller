# 04) Dataset Design

## โครงสร้าง Dataset

ข้อมูลหลักอยู่ใน `dataset/by_class/` แยกไฟล์ CSV ตามคลาสท่าทาง

### คลาสและจำนวนข้อมูลดิบ (ตรวจจากไฟล์จริง)

| Class | Samples (Raw) |
|---|---:|
| block | 500 |
| neutral | 500 |
| dodge_back | 300 |
| dodge_front | 300 |
| dodge_left | 300 |
| dodge_right | 300 |
| final_skill | 300 |
| left_punch | 300 |
| right_punch | 300 |
| **รวม** | **3,100** |

---

## วิธีเก็บข้อมูล (Collection Design)

แนวทางที่ใช้ในโปรเจกต์:
1. แยกเก็บทีละ action เพื่อควบคุม label quality
2. เก็บหลาย burst ต่อคลาส (ลด bias จากช่วงเวลาเดียว)
3. ลบ/drop แถวที่มีค่าเสียหายก่อนเข้า pipeline
4. transform เป็น feature space มาตรฐานเดียวกันก่อน train

หลักการนี้ช่วยให้:
- label สะอาดขึ้น
- noise ระหว่างคลาสลดลง
- train เร็วและเสถียรกว่า raw landmark ตรง ๆ

---

## Class Balance และผลกระทบ

Dataset ไม่ได้ imbalance รุนแรง แต่มี major classes คือ `block` และ `neutral` ที่มากกว่าคลาสอื่น

ผลเชิงโมเดล:
- ข้อดี: เรียนรู้ state ที่พบบ่อยในเกมได้แม่น
- ความเสี่ยง: โมเดลอาจ bias ไปคลาสหลัก หาก split ผิด

แนวแก้ในโปรเจกต์:
1. ใช้ stratified video-based split (แยก split ต่อคลาส)
2. ใช้ augmentation เพิ่มความหลากหลายตัวอย่าง
3. ประเมินรายคลาส (ไม่ดูแค่ accuracy รวม)

---

## ขนาดข้อมูลหลัง Augmentation (MLP run ล่าสุด)

- Raw: 3,100
- หลัง augmentation (`augment_factor=1`): 6,200
- Split ล่าสุดใน `executed_train.ipynb`:
  - Train: 4,900
  - Val: 650
  - Test: 650

---

## คุณภาพข้อมูลที่ต้องคุมก่อน deploy

1. แสงต้องไม่ย้อนจน landmark visibility ต่ำ
2. ท่าทางคล้ายกัน (เช่น dodge_front กับบางช่วงของ dodge_left/right) ต้องมีตัวอย่างพอ
3. ระยะผู้เล่นจากกล้องควรอยู่ช่วงที่ระบบ detect จุดสำคัญได้ครบ
4. บังคับ naming/labeling schema เดียวกันตลอด pipeline

---

## ข้อเสนอแนะถ้าจะ scale สำหรับ Roblox production

1. เพิ่มผู้เล่นหลาย body types (สูง/ต่ำ, แขนสั้น/ยาว)
2. เก็บหลาย environment (ห้องมืด/สว่าง/ฉากหลังต่างกัน)
3. เพิ่ม camera angle variation
4. ทำ test split ข้ามผู้เล่น (cross-subject) เพื่อวัด generalization จริง

---

## ประโยคสรุปสำหรับสไลด์

"Dataset นี้ถูกออกแบบเป็น action-centric พร้อม label quality สูง และปรับสมดุลด้วย augmentation + stratified split ทำให้คะแนนที่ได้สะท้อนการใช้งานจริงมากขึ้น โดยเฉพาะใน context ของเกม Roblox ที่ต้องตอบสนองเร็วและแม่นพร้อมกัน"