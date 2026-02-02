# 🥊 ML-AI Motion Controller - Boxing Game (+GUI & WebSocket)

AI-powered motion controller ที่ใช้ webcam และ body movements ควบคุม Roblox Boxing Game  
**Punch ในชีวิตจริง → ตัวละครชกในเกม!**

---

## ✨ Features

- **Real-time Pose Detection** - ใช้ Google MediaPipe ตรวจจับท่าทางแบบ real-time
- **Dynamic AI (Velocity)** - ตรวจจับ "ความเร็ว" ของหมัด (Punch Speed) ไม่ใช่แค่ท่าทาง! ⚡
- **Machine Learning (Neural Network)** - ใช้ MLP Classifier ความแม่นยำสูง (99%+)
- **Smart AI** - มีระบบ Motion Analyzer ช่วยกรอง Noise และ Smoothing
- **Modern GUI** - หน้าจอควบคุมสวยงาม Clean Look (No Legs, Floating Arms style)
- **WebSocket Server** - ส่งข้อมูลท่าทางไปยัง Unity/Roblox/Web ได้ (Port 8765)
- **Auto Game Control** - ส่งคำสั่งกดปุ่มให้เกมอัตโนมัติ

---

## 📁 โครงสร้างโปรเจกต์ (Refactored)

```
📂 ML-AI Motion Controller/
│
├── 📂 dataset/                  # ข้อมูลดิบ (CSV)
├── 📂 models/                   # AI Model (.pkl)
│
├── 📂 src/                      # Source Code
│   ├── 📂 app/
│   │   ├── main.py             # 🖥️ GUI Application (Entry Point)
│   │   └── game_engine.py      # ⚙️ Game Logic & Camera Thread
│   │
│   ├── 📂 data/                 # Scripts สำหรับเก็บข้อมูล
│   ├── 📂 model/                # Scripts สำหรับเทรน AI
│   │
│   ├── 📂 utils/                # Utilities
│   │   ├── camera_stream.py    # Threaded Camera
│   │   ├── motion_analyzer.py  # AI Smoothing Logic
│   │   ├── ws_server.py        # 📡 WebSocket Server
│   │   └── input_handler.py    # Keyboard Input
│   │
│   ├── 📂 legacy/               # Code เวอร์ชั่นเก่า (Backup)
│   └── config.py               # ⚙️ Configuration
│
├── 📄 run.py                    # 🚀 Launch Script (กดรันไฟล์นี้!)
├── 📄 requirements.txt          # Python packages
└── 📄 README.md                 # คู่มือนี้
```

---

## Quick Start

### Step 1: ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: เปิดโปรแกรม (GUI Ver.)

```bash
python run.py
```

- จะมีหน้าต่าง GUI ขึ้นมา
- กดปุ่ม **Start Camera** เพื่อเริ่มใช้งาน
- ปรับ **Confidence** ได้สดๆ ขณะเล่น
- กด **C** เพื่อ Calibrate ท่าทางใหม่

---

## 📡 WebSocket Integration (New!)

ระบบจะส่งข้อมูล JSON ผ่าน `ws://localhost:8765` โดยอัตโนมัติเมื่อตรวจพบท่าทาง

**ตัวอย่างข้อมูล:**

```json
{
  "action": "left_punch",
  "confidence": 0.98,
  "state": "ACTION"
}
```

---

## � Troubleshooting

### Webcam ไม่ขึ้น

- เช็คว่ามีโปรแกรมอื่นใช้กล้องอยู่หรือไม่
- ลองเปลี่ยน `CAMERA_INDEX` ใน `src/config.py` เป็น 0 หรือ 1

### AI จับท่าไม่แม่น

1.  กดปุ่ม **C** หรือ **re-Calibrate** ใน GUI
2.  ปรับ Slider **Confidence** ลงมาหน่อย (แนะนำ 0.7 - 0.8)
3.  ลองเก็บข้อมูลท่าฝึกใหม่ให้ชัดเจนขึ้น (`python -m src.data.collection`)

---

### Step 3: Train New Model (Custom Moves)

ถ้าอยากเพิ่มท่าใหม่ หรือปรับความแม่นยำ:

1.  **เก็บข้อมูล (Data Collection):**

    ```bash
    python -m src.data.collection
    ```

    - กด **[N]** เปลี่ยนท่าที่จะเก็บ (เช่น left_punch, dodge_right)
    - กด **[S]** เลือกจำนวนรูป (Burst Size: 100/300/500/1000)
    - กด **[R]** เพื่อเริ่มอัด (หยุดเองเมื่อครบ)

2.  **เริ่มสอน AI (Training):**

    ```bash
    python train_pro.py
    ```

3.  **เล่นได้เลย!** (`python run.py`)

---

## 🎮 Controls (Default)

| Action          | Key Binding   | Description    |
| :-------------- | :------------ | :------------- |
| **Left Punch**  | `Left Click`  | ต่อยซ้าย       |
| **Right Punch** | `Right Click` | ต่อยขวา        |
| **Dodge Left**  | `A` + `Space` | หลบซ้าย        |
| **Dodge Right** | `D` + `Space` | หลบขวา         |
| **Dodge Front** | `W` + `Space` | หลบหน้า (Dash) |
| **Dodge Back**  | `S` + `Space` | หลบหลัง        |
| **Block**       | `B`           | ป้องกัน        |
| **Final Skill** | `F`           | ท่าไม้ตาย      |

**Happy Punching! 🥊🎮**
