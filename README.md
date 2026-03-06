# 🥊 ML-AI Motion Controller - Boxing Game (+GUI & WebSocket)

AI-powered motion controller ที่ใช้ webcam และ body movements ควบคุม Roblox Boxing Game  
**Punch ในชีวิตจริง → ตัวละครชกในเกม!**

---

## ✨ Features

- **Real-time Pose Detection** - ใช้ Google MediaPipe (BlazePose) ตรวจจับท่าทาง
- **108 Pro-Level Features** - Landmarks + Angles + Velocity + Bone Vectors + Acceleration + Distance
- **Machine Learning (MLP)** - Neural Network พร้อม Data Augmentation & GridSearchCV
- **Smart AI** - Motion Analyzer กรอง Noise และ Smoothing
- **Modern GUI** - CustomTkinter (Clean Look, Floating Arms style)
- **WebSocket Server** - ส่งข้อมูลไปยัง Unity/Roblox/Web (Port 8765)
- **Auto Game Control** - ส่งคำสั่งกดปุ่มให้เกมอัตโนมัติ

---

## 📁 โครงสร้างโปรเจกต์

```
📂 ML-AI Motion Controller/
│
├── 📂 dataset/                  # ข้อมูลดิบ (CSV)
├── 📂 models/                   # AI Model (.pkl)
├── 📂 reports/                  # Training Reports (Plots)
├── 📂 docs/                     # Documentation & Research
├── 📂 archive/                  # เอกสารเก่า (Legacy)
│
├── 📂 src/                      # Source Code
│   ├── 📂 app/
│   │   ├── main.py             # 🖥️ GUI Application (Entry Point)
│   │   └── game_engine.py      # ⚙️ Game Logic & Camera Thread
│   │
│   ├── 📂 data/
│   │   ├── collection.py       # เก็บข้อมูลท่าทาง
│   │   ├── processing.py       # Transform Raw → 108 Features
│   │   └── augmentation.py     # Data Augmentation (Noise, Scale, Mirror)
│   │
│   ├── 📂 model/
│   │   └── temporal_model.py   # PoseTransformer (Temporal Model)
│   │
│   ├── 📂 utils/
│   │   ├── pose_detection.py   # MediaPipe Pose Detection
│   │   ├── camera_stream.py    # Threaded Camera
│   │   ├── motion_analyzer.py  # AI Smoothing Logic
│   │   ├── ws_server.py        # 📡 WebSocket Server
│   │   └── input_handler.py    # Keyboard Input
│   │
│   └── config.py               # ⚙️ Configuration (108 features)
│
├── 📂 training/                 # 🤖 Training Scripts & Notebooks
│   ├── train.py                # Training Script (CLI)
│   ├── train.ipynb             # Training Notebook (MLP)
│   └── train_temporal.ipynb    # Training Notebook (Transformer)
│
├── 📂 scripts/                  # Project Scripts
│   ├── setup_env.bat           # ติดตั้ง Environment อัตโนมัติ
│   ├── run_app.bat             # เปิดโปรแกรม
│   ├── system_health_check.py  # เช็คระบบ
│   └── test_camera.py          # ทดสอบกล้อง
│
├── 📂 maintenance/              # 🔧 System Maintenance Tools
│
├── 📄 run.py                    # 🚀 Launch Script
└── 📄 requirements.txt
```

---

## 🚀 Quick Start

### Step 1: ติดตั้ง Environment

```bash
# อัตโนมัติ (แนะนำ)
scripts\setup_env.bat

# หรือแบบ Manual
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: เปิดโปรแกรม

```bash
python run.py
```

- กดปุ่ม **Start Camera** เพื่อเริ่มใช้งาน
- ปรับ **Confidence** ได้สดๆ ขณะเล่น
- กด **C** เพื่อ Calibrate ท่าทางใหม่

---

## 🤖 Training Model

### วิธีที่ 1: Jupyter Notebook (แนะนำ)

```bash
jupyter notebook training/train.ipynb
```

### วิธีที่ 2: CLI

```bash
# แบบเต็ม (Augmentation + GridSearchCV)
python training/train.py

# แบบเร็ว (ไม่ทำ GridSearch)
python training/train.py --no-grid

# ไม่ทำ Augmentation
python training/train.py --no-augment
```

### ขั้นตอนการ Train:

1. **เก็บข้อมูล:**

   ```bash
   python -m src.data.collection
   ```

   - กด **[N]** เปลี่ยนท่า | **[S]** เลือก Burst Size | **[R]** เริ่มอัด

2. **Train:**

   ```bash
   python training/train.py
   ```

3. **เล่นเลย!** → `python run.py`

---

## 📡 WebSocket Integration

ส่ง JSON ผ่าน `ws://localhost:8765` อัตโนมัติ:

```json
{
  "action": "left_punch",
  "confidence": 0.98,
  "state": "ACTION"
}
```

---

## 🎮 Controls (Default)

| Action          | Key Binding   | Description    |
| :-------------- | :------------ | :------------- |
| **Left Punch**  | `Left`        | ต่อยซ้าย       |
| **Right Punch** | `Right`       | ต่อยขวา        |
| **Dodge Left**  | `Q`           | หลบซ้าย        |
| **Dodge Right** | `E`           | หลบขวา         |
| **Dodge Front** | `W` + `Space` | หลบหน้า (Dash) |
| **Dodge Back**  | `S` + `Space` | หลบหลัง        |
| **Defense**     | `F`           | ป้องกัน        |
| **Final Skill** | `X`           | ท่าไม้ตาย      |

---

## 🔧 Troubleshooting

| ปัญหา           | วิธีแก้                                      |
| --------------- | -------------------------------------------- |
| Webcam ไม่ขึ้น  | เปลี่ยน `CAMERA_INDEX` ใน `src/config.py`    |
| AI จับไม่แม่น   | กด C (Calibrate) + ปรับ Confidence (0.7-0.8) |
| MediaPipe Error | รัน `scripts\setup_env.bat` ใหม่             |

**Happy Punching! 🥊🎮**
