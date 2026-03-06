# 06) Feature Engineering (108 Features)

## ทำไมไม่ใช้ Raw Pose ตรง ๆ

Raw pose จาก MediaPipe = 33 landmarks × 4 ค่า (x,y,z,visibility) = 132 มิติ

ข้อจำกัดของ raw โดยตรง:
1. มีข้อมูลที่ไม่เกี่ยวกับเกมจำนวนมาก (บางจุดไม่สำคัญกับ action)
2. ไวต่อระยะกล้อง/สรีระผู้เล่น
3. โมเดลต้องเรียนรู้ทั้ง geometry + semantics พร้อมกัน (ยากขึ้น)

แนวทางของโปรเจกต์นี้คือ **แปลง raw เป็น feature เชิงความหมายของท่าต่อสู้** เพื่อให้โมเดลแยกคลาสได้ง่ายขึ้นและเร็วขึ้น

---

## Feature Breakdown (อ้างอิง `compute_features`)

รวมทั้งหมด 108 features แบ่งเป็น:

1. **Body Coords (56)**
   - 14 จุดช่วงบน (landmarks 11–24)
   - ต่อจุดใช้ 4 ค่า: normalized x, y, z + visibility

2. **Upper-body Angles (4)**
   - มุมศอกซ้าย/ขวา
   - มุมไหล่ซ้าย/ขวา

3. **Velocity (12)**
   - ความต่างตำแหน่งระหว่างเฟรมของ elbow/wrist (4 จุด × 3 แกน)
   - ช่วยจับ "การเคลื่อนที่" ไม่ใช่แค่ pose static

4. **Bone Vectors (18)**
   - ทิศทางกระดูกส่วนแขน/ไหล่/ลำตัวแบบ normalized
   - ทำให้โมเดลเห็น orientation ชัดเจน

5. **Acceleration (12)**
   - การเปลี่ยนของ velocity
   - มีประโยชน์กับท่าที่เร็ว/กระชาก

6. **Distance Features (6)**
   - ระยะข้อมือถึงไหล่/สะโพก
   - ระยะระหว่างข้อมือและศอก
   - ทำให้แยก action ที่คล้ายกันแต่ reach ต่างกันได้ดีขึ้น

---

## เทคนิค Normalization สำคัญ

- ใช้ `mid_hip` เป็น reference origin
- normalize ด้วย `torso_size`

ผลลัพธ์:
1. ลดผลกระทบจากระยะผู้เล่นกับกล้อง
2. ลดผลกระทบจาก body scale ของแต่ละคน
3. feature distribution เสถียรกว่า

---

## กลุ่ม Feature ที่สำคัญต่อแต่ละ action (เชิง intuition)

- `left_punch` / `right_punch`:
  - elbow angle + wrist reach + velocity wrist
- `block`:
  - shoulder/elbow geometry คงที่ + ความเร็วต่ำ
- `dodge_left/right/front/back`:
  - bone vectors + shoulder/torso orientation + velocity pattern
- `final_skill`:
  - pattern ผสมหลายจุดพร้อมกัน (distance + acceleration)

---

## ผลเชิงโมเดลที่เห็นจริง

การใช้ 108 engineered features ช่วยให้:
1. MLP ที่ lightweight ก็ทำผลงานสูงได้ (99.54%)
2. convergence เร็วขึ้นใน training
3. ลด dependency ต่อ architecture ที่ซับซ้อนเกินจำเป็น

---

## ประเด็นพรีเซนต์ที่ควรเน้น

1. เราไม่ได้พึ่ง "โมเดลใหญ่" อย่างเดียว
2. เราเพิ่ม intelligence ในระดับ feature design
3. Feature design ทำให้ระบบเหมาะกับงานเกมจริงที่ต้องเร็วและนิ่ง

---

## ข้อเสนอพัฒนาต่อ

1. เพิ่ม feature เฉพาะคอมโบ (transition-aware features)
2. เพิ่ม dynamic hand dominance adaptation (ซ้าย/ขวาถนัด)
3. ผสาน temporal embedding สำหรับโมเดล sequence โดยตรง