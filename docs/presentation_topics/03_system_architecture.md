# 03) System Architecture

## ภาพรวม Pipeline

```text
Webcam Frame
   ↓
MediaPipe Pose Detection (33 landmarks × 4 = 132 raw)
   ↓
Feature Engineering (132 → 108)
   ↓
Scaler + Trained Model (.pkl)
   ↓
Prediction + Confidence
   ↓
Motion Analyzer (temporal smoothing + state machine)
   ↓
Action Trigger
   ├─ Direct Input (keyboard/mouse)
   └─ WebSocket Broadcast (ws://localhost:8765)
   ↓
Roblox Game Action
```

---

## องค์ประกอบหลักและไฟล์สำคัญ

### 1) Acquisition Layer
- รับภาพจากกล้องผ่าน threaded camera stream
- จุดเด่น: ลด frame drop และลด jitter ของ input stream
- ไฟล์เกี่ยวข้อง:
  - `src/utils/camera_stream.py`
  - `src/app/game_engine.py`

### 2) Perception Layer
- ใช้ MediaPipe Pose ในการตรวจ landmark
- ได้ข้อมูลดิบ 33 จุด พร้อม x,y,z,visibility
- ไฟล์เกี่ยวข้อง:
  - `src/utils/pose_detection.py`

### 3) Feature Layer
- แปลง raw landmarks เป็น 108 pro-level features
- ทำ normalization และคำนวณ feature เชิง movement
- ไฟล์เกี่ยวข้อง:
  - `src/utils/pose_detection.py` (`compute_features`)
  - `src/data/processing.py`

### 4) ML Inference Layer
- ใช้ scaler + classifier ที่ train แล้ว
- คืนผล `predicted_label` และ `confidence`
- ไฟล์เกี่ยวข้อง:
  - `models/*.pkl`
  - `src/app/game_engine.py`

### 5) Decision Layer
- MotionAnalyzer ทำ smoothing + consistency check + state machine
- ช่วยลด false positive จาก jitter รายเฟรม
- ไฟล์เกี่ยวข้อง:
  - `src/utils/motion_analyzer.py`

### 6) Control & Integration Layer
- ส่งคำสั่งเกมผ่านสองเส้นทาง:
  1. Direct input (`pydirectinput`)
  2. WebSocket JSON broadcast (`ws://localhost:8765`)
- ไฟล์เกี่ยวข้อง:
  - `src/utils/input_handler.py`
  - `src/utils/ws_server.py`

---

## Runtime Control Plane

### GUI Layer
- มี slider ปรับ confidence threshold และ cooldown
- มี profile/binding settings
- แสดง prediction/action/FPS
- ไฟล์: `src/app/main.py`

### Configuration Layer
- ตั้งค่า camera, target FPS, threshold, key bindings
- ไฟล์: `src/config.py`

---

## Data Contract (สำคัญสำหรับ Roblox Integration)

WebSocket payload ตัวอย่าง:

```json
{
  "action": "left_punch",
  "confidence": 0.98,
  "state": "ACTION"
}
```

แนวทางใน Roblox side:
1. subscribe WebSocket message
2. validate action + confidence
3. map action → animation/ability
4. ใส่ debounce/fallback อีกชั้นใน game logic

---

## จุดแข็งเชิงสถาปัตยกรรม

1. แยก concerns ชัด (detect / infer / decide / trigger)
2. รองรับทั้ง direct control และ network integration
3. ปรับค่า runtime ได้โดยไม่ต้อง retrain
4. scale ต่อได้ (เพิ่ม model ใหม่/เพิ่ม game client ใหม่)

---

## จุดที่ควร monitor ตอน deploy

1. FPS กล้องจริงบนเครื่องผู้เล่น
2. confidence distribution ตามสภาพแสง
3. false trigger rate ใน neutral state
4. WebSocket stability (latency/jitter/disconnect)