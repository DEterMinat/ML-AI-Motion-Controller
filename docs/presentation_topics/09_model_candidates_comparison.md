# 09) Model Candidates: MLP vs Transformer vs LSTM-GRU vs SVM vs ST-GCN

## เป้าหมายของการเทียบหลายโมเดล

เราไม่ได้ต้องการแค่โมเดลที่แม่นสุดในกระดาษ แต่ต้องการโมเดลที่:
1. แม่นพอสำหรับ gameplay
2. ตอบสนองเร็ว
3. ดูแลง่ายใน production
4. เสถียรเมื่อเจอสภาพแวดล้อมจริง

---

## ผลสรุปล่าสุด (จาก executed notebooks)

| Model | Test Accuracy | ลักษณะโมเดล |
|---|---:|---|
| **MLP** | **99.54%** | Frame-based classifier + engineered features |
| **Transformer** | **97.45%** | Temporal sequence model (window size 10) |
| **LSTM/GRU** | **95.50%** | Recurrent temporal modeling |
| **SVM (RBF)** | **95.00%** | Classical ML baseline |
| **ST-GCN** | **87.33%** | Graph-based spatio-temporal model |

---

## วิเคราะห์จุดแข็ง/จุดอ่อนรายโมเดล

### 1) MLP
**จุดแข็ง**
- แม่นสูงสุดในผลล่าสุด
- โครงสร้างไม่หนักมาก เหมาะกับ real-time
- เข้าคู่กับ 108 engineered features ได้ดีมาก

**จุดอ่อน**
- frame-based เป็นหลัก อาจพึ่ง temporal context น้อยกว่า sequence models

### 2) Transformer
**จุดแข็ง**
- เก่งกับรูปแบบการเคลื่อนไหวต่อเนื่อง
- จัดการ dependency ข้ามเฟรมได้ดี

**จุดอ่อน**
- ซับซ้อนกว่า MLP
- tuning และ resource สูงกว่า

### 3) LSTM/GRU
**จุดแข็ง**
- เป็น baseline temporal ที่ดี
- เข้าใจจังหวะต่อเนื่องได้

**จุดอ่อน**
- ความแม่นด้อยกว่า Transformer/MLP ใน dataset นี้

### 4) SVM
**จุดแข็ง**
- ฝึกง่าย อธิบายง่าย
- เป็น baseline ที่ดีมากสำหรับเปรียบเทียบ

**จุดอ่อน**
- จำกัดความสามารถกับ pattern ซับซ้อนมาก ๆ

### 5) ST-GCN
**จุดแข็ง**
- แนวคิดเหมาะกับ skeleton graph โดยธรรมชาติ

**จุดอ่อน**
- ใน dataset และเงื่อนไขนี้ยังไม่คุ้มความซับซ้อน
- sensitivity ต่อ data condition สูงกว่า

---

## สรุปเชิงตัดสินใจสำหรับ Roblox

**Production Choice (ตอนนี้): MLP**
เหตุผล:
1. Accuracy สูงสุด (99.54%)
2. Runtime footprint เบา
3. integrate กับ pipeline ปัจจุบันง่าย
4. maintainability สูง

**R&D Choice (ต่อยอด): Transformer**
- เก็บไว้เป็นเส้นทางพัฒนา temporal intelligence รุ่นถัดไป

---

## Key message บนสไลด์

"โมเดลที่ดีที่สุดไม่จำเป็นต้องซับซ้อนที่สุด — ในงานนี้ MLP + feature engineering ที่ดี + split ที่ถูกต้อง ให้ทั้งความแม่นและความเร็วที่เหมาะกับเกม Roblox มากที่สุด"