# 14) Limitations & Next Steps

## ข้อจำกัดปัจจุบัน (Current Limitations)

### 1) Data Scope
- ข้อมูลยังเน้นผู้เล่น/สภาพแวดล้อมจำกัด
- domain shift อาจเกิดเมื่อเปลี่ยนคน/แสง/ฉากหลังมาก

### 2) Evaluation Scope
- ตัวเลขหลักเป็น offline benchmark
- in-game telemetry ระยะยาวยังต้องเก็บเพิ่ม

### 3) Runtime Variability
- คุณภาพกล้องและแสงมีผลต่อ landmark stability
- hardware ต่างกันอาจให้ latency/performance ต่างกัน

### 4) Action Semantics
- บาง action ใกล้กันเชิง transition pose (เช่นกลุ่ม dodge)
- ต้อง refine ด้วยข้อมูล edge cases เพิ่ม

---

## ความเสี่ยงเชิงผลิตภัณฑ์

1. ผู้ใช้บางกลุ่มอาจคาดหวัง 100% ในทุกสถานการณ์
2. สภาพหน้างานจริงไม่สะอาดเท่า dataset ที่ควบคุมได้
3. ถ้าไม่มี fallback UX ที่ดี ผู้เล่นจะรู้สึกระบบ “ไม่แน่นอน”

---

## Next Steps (Roadmap เชิงเทคนิค)

### Phase 1: Stabilize (1–2 สัปดาห์)
1. เก็บ telemetry in-game (action success, false trigger, frame drop)
2. benchmark latency บนเครื่อง target 2–3 สเปก
3. tune confidence/cooldown per profile

### Phase 2: Generalize (2–4 สัปดาห์)
1. เก็บข้อมูลหลายคน (ต่างสรีระ/ทักษะ)
2. เก็บหลาย environment (แสง/มุมกล้อง/ฉากหลัง)
3. retrain + compare across seeds

### Phase 3: Productize (4–8 สัปดาห์)
1. เพิ่ม deployment tooling (model versioning + rollback)
2. เพิ่ม robust reconnect/recovery flow
3. ทำ QA checklist แบบ release gate

---

## Milestones ที่เสนอ

### Milestone M1: Pilot-Ready
- โมเดล MLP 99%+ offline
- action mapping ครบ
- demo Roblox เสถียร

### Milestone M2: Multi-user Validation
- ข้อมูลจากผู้เล่นหลายคน
- report แยก per-user performance
- policy threshold เฉพาะโปรไฟล์

### Milestone M3: Production Candidate
- telemetry dashboard
- rollback plan
- latency SLA ตามเครื่องเป้าหมาย

---

## Success Criteria รอบถัดไป

1. ลดความคลาดเคลื่อนในคลาส dodge transition
2. รักษา UX real-time ใน match จริงต่อเนื่อง
3. เพิ่มความเชื่อมั่นในการใช้งานข้ามผู้เล่น
4. ลด effort การตั้งค่าของผู้ใช้ใหม่ให้น้อยที่สุด

---

## Closing Message สำหรับสไลด์สุดท้าย

"งานนี้ผ่านจุดพิสูจน์หลักแล้ว: โมเดลแม่น, pipeline ถูกต้อง, และพร้อมใช้งานกับ Roblox ในระดับ pilot ขั้นต่อไปคือขยายความสามารถจาก single-environment ไปสู่ multi-user production พร้อมระบบ monitoring และ rollback ที่ครบถ้วน"