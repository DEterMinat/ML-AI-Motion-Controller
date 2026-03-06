# 12) Why ~99% is Good (และไม่ใช่การล็อกคะแนน)

## ประเด็นที่ผู้ฟังมักถาม

"คะแนนสูงขนาดนี้เชื่อได้ไหม?"

คำตอบสำหรับโปรเจกต์นี้คือ: **เชื่อได้ในขอบเขตที่เราประเมินถูกต้อง** และปัจจุบันเราแก้จุดเสี่ยงสำคัญแล้ว (leakage + class coverage)

---

## ทำไม ~99% ถึงสมเหตุสมผล

1. **Feature engineering คุณภาพสูง**
   - ไม่ใช่ raw landmark ตรง ๆ แต่เป็น 108 features ที่มีความหมายต่อ action โดยตรง

2. **Split กัน leakage จริง**
   - ใช้ video-based split + stratified ต่อคลาส
   - ลดคะแนนหลอกจากการเห็นเฟรมคล้ายกันข้าม split

3. **ทดสอบครบ 9 คลาส**
   - เคยมีปัญหาคลาสหายใน test แล้วถูกแก้แล้ว

4. **สถาปัตยกรรมเหมาะงาน**
   - MLP ขนาดพอดี + scaler + early stopping + tuning ที่ดี

---

## “ไม่ล็อก 99” หมายถึงอะไรในทางปฏิบัติ

- เราไม่ได้ hard-code ให้คะแนนออกมา 99
- คะแนนเป็นผลจาก data + split + model settings จริง
- เมื่อเปลี่ยน settings (เช่น augmentation หรือ random_state) คะแนนเปลี่ยนตามธรรมชาติ

ตัวอย่างจากการรันจริง:
- no augmentation: ต่ำลงชัดเจน
- moderate augmentation + proper split: ขึ้นมาระดับ ~99
- heavy augmentation บางรันอาจแตะ 100

นี่สะท้อนว่าโมเดลตอบสนองต่อเงื่อนไขจริง ไม่ได้ถูก fix ตัวเลข

---

## Offline Metric vs Real-world Performance

### Offline (สิ่งที่รายงานใน notebook)
- วัดบน test set ที่เตรียมไว้
- ควบคุมเงื่อนไขได้
- เหมาะกับการเทียบโมเดลเชิงวิจัย

### Real-world (สิ่งที่ผู้เล่นสัมผัส)
- เจอแสง/ฉาก/ระยะ/ผู้เล่นหลากหลาย
- มี motion blur และ occlusion
- มี network/input delay และ game state จริง

**ดังนั้นการรายงานที่ถูกต้องควรพูดสองค่า:**
1. Offline accuracy (ปัจจุบัน ~99.54% สำหรับ MLP)
2. In-game reliability (ต้องเก็บ telemetry ตอนใช้งานจริง)

---

## วิธีสื่อสารกับกรรมการ/ผู้ฟังให้น่าเชื่อถือ

ประโยคแนะนำ:

"คะแนน ~99% ของเราไม่ได้มาจากการล็อกผล แต่เกิดจาก pipeline ที่ถูกต้อง: feature engineering ดี, split ป้องกัน leakage และประเมินครบทุกคลาส อย่างไรก็ตามเรายังแยกชัดเจนว่า offline metric กับ real-world performance ไม่เท่ากัน และมีแผนเก็บ telemetry ในเกมจริงเพื่อยืนยันผลเชิง deployment"

---

## KPI ฝั่ง real-world ที่ควรเพิ่มหลังพรีเซนต์

1. Action success rate ต่อแมตช์
2. False trigger rate ระหว่าง neutral
3. Time-to-action (gesture → game event)
4. User correction rate (ผู้เล่นต้องแก้ท่าบ่อยแค่ไหน)

---

## สรุปสั้น

- ~99% เป็นคะแนนที่ดีและสมเหตุสมผล
- ไม่ใช่ตัวเลขที่บังคับให้เกิด
- ใช้ได้สำหรับตัดสินใจ deploy pilot
- ต้องมี monitoring ต่อเนื่องในสภาพจริงของ Roblox