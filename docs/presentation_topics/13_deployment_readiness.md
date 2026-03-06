# 13) Deployment Readiness (Roblox)

## โมเดลที่เลือกสำหรับ Production

**เลือก: MLP (`models/boxing_model.pkl`)**

เหตุผล:
1. Accuracy สูงสุดใน benchmark ล่าสุด (99.54%)
2. pipeline runtime เรียบง่าย ดูแลง่าย
3. latency เชิงสถาปัตยกรรมเหมาะกับ real-time control
4. ผสานกับ input handler และ websocket ได้ครบ

---

## Deployment Architecture สำหรับ Roblox

มี 2 โหมดใช้งาน:

### โหมด A: Direct Input (เร็วสุด, local)
- AI ส่ง action ไป `pydirectinput`
- เหมาะกับการเล่นบนเครื่องเดียวกัน (local game focus)

### โหมด B: WebSocket Integration (ยืดหยุ่นสูง)
- AI broadcast JSON ไป `ws://localhost:8765`
- Roblox-side bridge/client รับ action แล้วแปลงเป็น animation/ability
- เหมาะกับการแยก service หรือทำ telemetry

---

## Latency Plan (โดยประมาณ + วิธีวัดจริง)

### Latency budget ที่แนะนำ
1. Capture + pose extraction
2. feature + inference
3. smoothing/decision
4. action dispatch (input/websocket)

เป้าหมายเชิง UX:
- ผู้เล่นควรรู้สึกตอบสนองทันจังหวะเกม
- ควบคุมได้ต่อเนื่องในระดับ 30 FPS target

> หมายเหตุ: ตัวเลข ms แบบ final ต้อง benchmark บนเครื่อง target + Roblox scene จริง (stress test 5–10 นาที)

---

## Fallback Strategy เมื่อ Confidence ต่ำ

จากโค้ดปัจจุบันมี `CONFIDENCE_THRESHOLD` และ `MotionAnalyzer`

แนะนำ policy สำหรับ production:

1. ถ้า confidence < threshold:
   - ไม่ trigger action
   - คง state ที่ปลอดภัย (neutral/hold off)

2. ถ้า prediction สวิงเร็ว:
   - ใช้ temporal smoothing + consistency check

3. ถ้า tracking หาย:
   - reset history
   - disable aggressive actions ชั่วคราว

4. ถ้า websocket หลุด:
   - retry connect
   - fallback เป็น local overlay แจ้งผู้เล่น

---

## Operational Checklist ก่อนปล่อยจริง

1. Lock เวอร์ชัน model/scaler/encoder เป็นชุดเดียว
2. ตั้งค่า threshold ตาม environment จริง
3. ทำ calibration flow ให้ผู้เล่นเข้าใจง่าย
4. เก็บ log สำคัญ: action, confidence, dropped frames, reconnects
5. เตรียม emergency toggle ปิด motion control ในเกม

---

## Security & Safety (สำหรับ Roblox context)

1. validate action whitelist ฝั่ง game client
2. ใส่ cooldown ฝั่งเกมซ้ำอีกชั้น (defense in depth)
3. จำกัด rate ของ action message
4. แยก dev/test port จาก production

---

## Go/No-Go Criteria

**Go ถ้า:**
- false trigger ต่ำใน neutral
- response ลื่นในแมตช์จริง
- ไม่มี crash ต่อเนื่อง 30 นาที

**No-Go ถ้า:**
- trigger ผิดจนกระทบ gameplay
- confidence drop มากในสภาพแสงทั่วไป
- websocket/input ไม่เสถียร

---

## สรุป

ระบบพร้อมสำหรับ **Pilot Deployment** กับ Roblox โดยใช้ MLP เป็น production model พร้อม fallback policy และ monitoring plan ครบสำหรับยกระดับสู่ production เต็มรูปแบบ