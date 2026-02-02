# โครงสร้างโปรเจค Motion Controller

```
D:\ML-AI Motion Controller\
│
├── 📁 Core Python Scripts (ไฟล์หลักที่ใช้งาน)
│   ├── data_collector.py          # เก็บข้อมูล Training จากกล้อง
│   ├── train_model.py             # Train โมเดล Machine Learning
│   └── main.py                    # รันระบบควบคุมเกม (ใช้งานจริง)
│
├── 📁 Setup & Installation (ติดตั้งระบบ)
│   ├── setup.bat                  # ✨ ดับเบิลคลิก → ติดตั้งอัตโนมัติ (Windows)
│   ├── setup.ps1                  # PowerShell Setup Script
│   ├── setup_automated.py         # Python Setup Script (ใช้ภายใน)
│   ├── setup_helper.py            # ตรวจสอบ Package ที่ติดตั้ง
│   ├── conda-environment.yml      # Conda Environment (ถ้ามี Conda)
│   └── requirements.txt           # pip Dependencies
│
├── 📁 Documentation (เอกสารคู่มือ)
│   ├── START_HERE.txt             # 🎯 อ่านก่อน! ภาพรวมโปรเจค
│   ├── QUICKSTART.md              # เริ่มใช้งานใน 5 นาที
│   ├── README.md                  # คู่มือหลัก
│   ├── DOCUMENTATION.md           # เอกสารเทคนิคแบบละเอียด
│   ├── SYSTEM_ARCHITECTURE.md     # ระบบสถาปัตยกรรม
│   ├── PROJECT_INDEX.md           # ดัชนีไฟล์ทั้งหมด
│   └── PROJECT_STRUCTURE_TH.md    # ไฟล์นี้ (ภาษาไทย)
│
└── 📁 Generated Files (ไฟล์ที่สร้างขึ้นอัตโนมัติ)
    ├── boxing_data.csv            # ข้อมูล Training (จาก data_collector.py)
    ├── boxing_model.pkl           # โมเดลที่ Train แล้ว
    └── label_encoder.pkl          # Label Encoder
```

---

## 🚀 วิธีติดตั้งระบบ (3 ขั้นตอน)

### ขั้นที่ 1: ติดตั้ง Python (ถ้ายังไม่มี)
1. ดาวน์โหลด Python 3.10 หรือใหม่กว่า: https://www.python.org/downloads/
2. ติดตั้งและ **ติ๊กถูก "Add Python to PATH"**
3. เปิด PowerShell ใหม่ แล้วพิมพ์: `python --version` (ต้องขึ้นเวอร์ชัน)

### ขั้นที่ 2: ติดตั้ง Dependencies
**วิธีที่ 1: ใช้ Automated Setup (แนะนำ - ง่ายที่สุด)**
```powershell
# ดับเบิลคลิกไฟล์นี้:
setup.bat

# หรือใน PowerShell:
python setup_automated.py
```

**วิธีที่ 2: ติดตั้งด้วย pip เอง**
```powershell
pip install opencv-python mediapipe pandas scikit-learn pydirectinput numpy
```

**วิธีที่ 3: ใช้ Conda (ถ้ามี Anaconda/Miniconda)**
```powershell
conda env create -f conda-environment.yml
conda activate motion-controller
```

### ขั้นที่ 3: ตรวจสอบการติดตั้ง
```powershell
python setup_helper.py
```

---

## 📖 วิธีใช้งาน (3 ขั้นตอน)

### ขั้นที่ 1: เก็บข้อมูล Training (1-2 ชั่วโมง)

```powershell
python data_collector.py
```

**ทำอะไร:**
- ระบบจะเปิดกล้อง
- ใส่ชื่อท่าทาง เช่น: `neutral` (ยืนปกติ)
- กด **'s'** เพื่อบันทึกภาพ (เก็บ 50-100 ภาพต่อท่า)
- กด **'q'** เมื่อเสร็จ

**เก็บข้อมูลทั้งหมด 3 ท่า:**
1. `neutral` - ยืนปกติ (50-100 ภาพ)
2. `left_punch` - หมัดซ้าย (50-100 ภาพ)
3. `right_punch` - หมัดขวา (50-100 ภาพ)

**ไฟล์ที่ได้:** `boxing_data.csv`

---

### ขั้นที่ 2: Train โมเดล (1-2 นาที)

```powershell
python train_model.py
```

**ทำอะไร:**
- โหลดข้อมูลจาก `boxing_data.csv`
- Train โมเดล Random Forest
- แสดงค่า Accuracy (ต้อง > 0.85 ถึงจะดี)

**ไฟล์ที่ได้:** 
- `boxing_model.pkl` (โมเดล)
- `label_encoder.pkl` (ตัวแปลง Label)

---

### ขั้นที่ 3: เล่นเกม! (ใช้งานจริง)

```powershell
python main.py
```

**ทำอะไร:**
- เปิดกล้อง
- ตรวจจับท่าทางแบบ Real-time
- ถ้าหมัด → คลิกเมาส์อัตโนมัติ
- ควบคุมเกม Roblox Boxing

**การใช้งาน:**
- ยืนหน้ากล้อง (2-3 เมตร)
- ทำท่าหมัด → เกมจะตอบสนอง!
- กด **'q'** เพื่อออก

---

## ⚙️ ปรับแต่งระบบ

### ปรับค่าความแม่นยำ (ไฟล์: `main.py`)

```python
# บรรทัดที่ 14-15
CONFIDENCE_THRESHOLD = 0.8    # เพิ่มถ้าคลิกผิด (0.85-0.95)
COOLDOWN_DURATION = 0.5       # เพิ่มถ้าคลิกเยอะไป (0.7-1.0)
```

**เมื่อไหร่ต้องปรับ:**
- **คลิกผิดบ่อย** → เพิ่ม `CONFIDENCE_THRESHOLD` เป็น 0.9
- **คลิกติดๆ** → เพิ่ม `COOLDOWN_DURATION` เป็น 0.7 หรือ 1.0
- **ช้าเกินไป** → ลด `COOLDOWN_DURATION` เป็น 0.3

---

## 🔧 แก้ปัญหาที่เจอบ่อย

### ❌ ปัญหา: "conda: command not found"
**วิธีแก้:**
- ติดตั้ง Anaconda: https://www.anaconda.com/download/
- หรือใช้ pip แทน: `pip install -r requirements.txt`

### ❌ ปัญหา: "Cannot open webcam"
**วิธีแก้:**
1. ปิดโปรแกรมที่ใช้กล้อง (Zoom, Teams, Skype)
2. ตรวจสอบ Windows Settings → Privacy → Camera → อนุญาต Python

### ❌ ปัญหา: "Model files not found"
**วิธีแก้:**
- รัน `python data_collector.py` ก่อน (เก็บข้อมูล)
- แล้วค่อยรัน `python train_model.py` (สร้างโมเดล)

### ❌ ปัญหา: Accuracy ต่ำ (< 0.85)
**วิธีแก้:**
1. เก็บข้อมูลเพิ่ม (100-200 ภาพต่อท่า)
2. เก็บในที่ที่แสงสว่างดี
3. เปลี่ยนมุมกล้องและระยะ

### ❌ ปัญหา: เกมไม่ตอบสนอง
**วิธีแก้:**
1. คลิกที่หน้าต่างเกม Roblox ให้ Focus
2. ตรวจสอบ Confidence Score บนหน้าจอ
3. ถ้าต่ำกว่า 0.8 → เก็บข้อมูลเพิ่ม

---

## 📊 สรุป Workflow

```
┌─────────────────────────────────────┐
│ 1. ติดตั้ง Python & Dependencies   │
│    → setup.bat หรือ pip install    │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│ 2. เก็บข้อมูล Training              │
│    → python data_collector.py      │
│    → boxing_data.csv               │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│ 3. Train โมเดล                      │
│    → python train_model.py         │
│    → boxing_model.pkl              │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│ 4. เล่นเกม!                         │
│    → python main.py                │
│    → ควบคุมด้วยท่าทาง               │
└─────────────────────────────────────┘
```

---

## 💡 เคล็ดลับสำหรับผลลัพธ์ที่ดี

1. **แสงสว่าง:** ใช้แสงที่สว่างและสม่ำเสมอ
2. **ระยะห่าง:** ยืนห่างกล้อง 2-3 เมตร (ให้เห็นตัวเต็มๆ)
3. **พื้นหลัง:** ใช้พื้นหลังเรียบๆ (กำแพงสีเดียว)
4. **ท่าทาง:** ทำท่าชัดเจน (neutral ต้างจาก punch)
5. **ข้อมูล:** เก็บข้อมูลหลากหลาย (มุม ระยะ แสง)

---

## 📚 เอกสารเพิ่มเติม

| ไฟล์ | เหมาะกับ | ความยาว |
|------|----------|----------|
| **START_HERE.txt** | เริ่มต้น | 1 หน้า |
| **QUICKSTART.md** | ติดตั้งเร็ว | 2 หน้า |
| **README.md** | ภาพรวม | 5 หน้า |
| **DOCUMENTATION.md** | เทคนิคละเอียด | 30+ หน้า |
| **SYSTEM_ARCHITECTURE.md** | สถาปัตยกรรม | 20+ หน้า |

---

## 🎯 คำสั่งที่ใช้บ่อย

```powershell
# ติดตั้งระบบ (ครั้งแรก)
python setup_automated.py

# เก็บข้อมูล
python data_collector.py

# Train โมเดล
python train_model.py

# เล่นเกม
python main.py

# ตรวจสอบ Package
python setup_helper.py
```

---

## 📞 ต้องการความช่วยเหลือ?

1. อ่าน **START_HERE.txt** (ภาพรวมโปรเจค)
2. อ่าน **QUICKSTART.md** (เริ่มใช้งาน)
3. ดูที่ **DOCUMENTATION.md** → Troubleshooting
4. ตรวจสอบ Console Error Message

---

**สร้างเมื่อ:** 9 ธันวาคม 2025  
**เวอร์ชัน:** 1.0  
**สถานะ:** ✅ พร้อมใช้งาน

ขอให้สนุกกับการควบคุมเกมด้วยท่าทาง! 🎮👊
