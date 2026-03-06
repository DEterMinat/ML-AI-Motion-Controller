# 02) Use Case & Demo Scenario

## ผู้ใช้คือใคร (Target Users)

### Primary Users
1. ผู้เล่น Roblox แนวต่อสู้/boxing ที่อยากได้ประสบการณ์ immersive
2. ผู้เล่นใหม่ที่ยังไม่ชินคีย์คอมโบซับซ้อน
3. ผู้ทดลองระบบ Human-AI Interaction แบบ real-time

### Secondary Users
1. ทีมเกม/นักพัฒนา ที่อยากเพิ่ม alternate control mode
2. ทีมวิจัย/นักศึกษา ที่สนใจ pose-based game interaction

---

## Gameplay Flow (มุมผู้เล่น)

1. เปิดแอป Motion Controller
2. กด Start Camera
3. ยืนในเฟรมให้ระบบเห็นแขนและช่วงบนชัด
4. ทำท่าทางตาม action ที่ต้องการ
5. ระบบแปลงท่าเป็นคำสั่งเกม
6. ดูผลที่ตัวละครตอบสนองทันที

---

## Action ทั้ง 9 คลาสที่ระบบต้องแยก

1. `neutral`
2. `block`
3. `left_punch`
4. `right_punch`
5. `dodge_left`
6. `dodge_right`
7. `dodge_front`
8. `dodge_back`
9. `final_skill`

> หมวด action ในเกม:
- Attack: left/right punch, final_skill
- Defense: block
- Mobility/Evasion: dodge 4 ทิศ
- Reset state: neutral

---

## Demo Scenario ที่แนะนำบนเวที (3–5 นาที)

### ฉากเดโม A: Baseline Reliability
- ทำ `neutral -> left_punch -> neutral -> right_punch`
- เน้นว่าระบบไม่ spam action เพราะมี smoothing + cooldown

### ฉากเดโม B: Defense & Evasion
- ทำ `block` ค้าง 1–2 วินาที
- เปลี่ยนเป็น `dodge_left` และ `dodge_right`
- ชี้ให้เห็นว่า state machine กัน trigger ซ้ำโดยไม่ตั้งใจ

### ฉากเดโม C: High-impact Move
- ทำ `final_skill`
- โชว์ confidence/action บน HUD หรือ info bar

---

## Script เดโมแบบพูดตามได้ทันที

"ตอนนี้ผมเริ่มจาก neutral ก่อน เพื่อให้ระบบ reset state จากนั้นผมต่อยซ้ายและขวา ระบบจะตีความจากท่าร่างกายไม่ใช่จากปุ่ม ต่อไปเป็น block และ dodge เพื่อโชว์ว่าระบบยังแม่นแม้เปลี่ยนแอ็กชันต่อเนื่อง สุดท้ายใช้ final skill เพื่อยืนยันว่าระบบรองรับทั้ง action พื้นฐานและ action พิเศษครบ 9 คลาส"

---

## Demo Checklist (ก่อนขึ้นพรีเซนต์)

1. กล้องเห็นไหล่-ศอก-ข้อมือชัด
2. แสงไม่ย้อน ไม่มืดเกินไป
3. หน้าต่าง Roblox/เกมมี focus (กรณี direct input)
4. ตั้ง confidence threshold ให้เหมาะกับผู้เดโม (เช่น 0.75–0.85)
5. เตรียม fallback: ถ้าเวทีแสงแย่ ให้โชว์ log + overlay ร่วม

---

## KPI ที่ควรอ้างอิงตอนเดโม

- Trigger accuracy ของ action หลักต้องนิ่ง
- Delay ที่ผู้เล่นรับรู้ต้องไม่หน่วงจนเสียจังหวะเกม
- False trigger ต้องต่ำในช่วงที่ผู้เล่นอยู่ neutral
- ผู้ชมเข้าใจ mapping ระหว่างท่าและ action ได้ภายใน 1 นาที