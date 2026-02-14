# งานวิจัยที่เกี่ยวข้อง: แนวทาง ML/DL สำหรับการควบคุมเกมด้วยการเคลื่อนไหว

บทนี้ทบทวนแนวทาง Machine Learning และ Deep Learning ที่มีอยู่สำหรับการประมาณท่าทางมนุษย์แบบเรียลไทม์ (Real-time Human Pose Estimation) และการจดจำการกระทำ (Action Recognition) ซึ่งเป็นพื้นฐานของโปรเจกต์ ML-AI Motion Controller

---

## 1. โมเดลการประมาณท่าทาง (Pose Estimation Models)

### 1.1 BlazePose (MediaPipe)

- **ประเภท:** CNN น้ำหนักเบา (Top-Down, คนเดียว)
- **สถาปัตยกรรม:** ไปป์ไลน์สองขั้นตอน: Detector + Tracker ใช้ MobileNetV2 ที่ปรับแต่งเป็น Backbone พร้อม Regression Heads สำหรับ 33 จุดพิกัด 3 มิติ
- **นวัตกรรมสำคัญ:** ใช้วิธี Heatmap + Offset + Regression เพื่อความแม่นยำระดับ Sub-pixel ด้วยการคำนวณที่น้อยที่สุด
- **ประสิทธิภาพ:** 30+ FPS บน CPU มือถือ
- **อ้างอิง:** Bazarevsky, V., et al. (2020). _BlazePose: On-device Real-time Body Pose tracking._ [arXiv:2006.10204](https://arxiv.org/abs/2006.10204)

### 1.2 OpenPose

- **ประเภท:** CNN หนัก (Bottom-Up, หลายคน)
- **สถาปัตยกรรม:** ใช้ Part Affinity Fields (PAFs) เพื่อเชื่อมต่อจุดพิกัดที่ตรวจจับได้ข้ามหลายคน CNN สองสาขา: สาขาหนึ่งสำหรับตรวจจับจุด อีกสาขาสำหรับ Affinity Vectors
- **นวัตกรรมสำคัญ:** ระบบแรกที่ทำ Multi-person 2D Pose Estimation แบบเรียลไทม์ได้
- **ประสิทธิภาพ:** ~0.4 FPS บน CPU (ต้องใช้ GPU สำหรับเรียลไทม์)
- **อ้างอิง:** Cao, Z., et al. (2017). _Realtime Multi-Person 2D Pose Estimation using Part Affinity Fields._ [arXiv:1611.08050](https://arxiv.org/abs/1611.08050)

### 1.3 HRNet (High-Resolution Network)

- **ประเภท:** CNN ความแม่นยำสูง (Top-Down)
- **สถาปัตยกรรม:** รักษาความละเอียดสูงตลอดทั้งเครือข่าย แทนที่จะกู้คืนจากความละเอียดต่ำ ใช้ Subnetworks หลายความละเอียดแบบขนานพร้อมการแลกเปลี่ยนข้อมูลซ้ำ
- **นวัตกรรมสำคัญ:** ความแม่นยำที่เหนือกว่าสำหรับการระบุตำแหน่งจุดพิกัดละเอียด
- **ประสิทธิภาพ:** แม่นยำที่สุด แต่ใช้ทรัพยากรคอมพิวเตอร์สูง
- **อ้างอิง:** Sun, K., et al. (2019). _Deep High-Resolution Representation Learning for Visual Recognition._ [arXiv:1908.07919](https://arxiv.org/abs/1908.07919)

---

## 2. โมเดลการจดจำการกระทำ (Action Recognition Models)

### 2.1 MLP Classifier (ใช้ข้อมูลท่าทาง)

- **ประเภท:** Neural Network ตื้น
- **อินพุต:** Features โครงกระดูกที่แยกออกมา (จุดพิกัด, มุม, ความเร็ว) จาก Pose Estimator
- **สถาปัตยกรรม:** โดยทั่วไป 2-3 ชั้น Fully Connected พร้อม ReLU Activation
- **ข้อดี:** Inference เร็วมาก (<1ms), ฝึกง่าย, Features ตีความได้
- **ข้อเสีย:** ต้องทำ Feature Engineering ด้วยมือ; การจำลองเวลาจำกัด
- **อ้างอิง:** Weng, C., et al. (2003). _Real-time hand gesture recognition using skin color segmentation and neural networks._ [ResearchGate](https://www.researchgate.net/publication/221063628)

### 2.2 ST-GCN (Spatial-Temporal Graph Convolutional Network)

- **ประเภท:** Deep Learning (Graph Neural Network)
- **อินพุต:** ลำดับโครงกระดูกที่แสดงเป็น Spatio-temporal Graphs
- **สถาปัตยกรรม:** ใช้ Graph Convolutions บนโครงสร้างโครงกระดูก และ Temporal Convolutions ข้ามเฟรม
- **ข้อดี:** เรียนรู้ความสัมพันธ์เชิงพื้นที่ระหว่างข้อต่ออัตโนมัติ; จับพลวัตเวลาได้
- **ข้อเสีย:** Latency สูงกว่า; ต้องใช้ GPU สำหรับเรียลไทม์
- **อ้างอิง:** Yan, S., et al. (2018). _Spatial Temporal Graph Convolutional Networks for Skeleton-Based Action Recognition._ [arXiv:1801.07455](https://arxiv.org/abs/1801.07455)

---

## 3. ตารางเปรียบเทียบ (Comparison Table)

| โมเดล / แนวทาง       | ประเภท             | ความเร็ว (FPS)       | ความแม่นยำ           | ความต้องการฮาร์ดแวร์ | เหมาะสำหรับ           |
| -------------------- | ------------------ | -------------------- | -------------------- | -------------------- | --------------------- |
| **BlazePose (Lite)** | Pose Estimation    | 30+                  | ปานกลาง              | CPU                  | มือถือ / เกมเรียลไทม์ |
| **BlazePose (Full)** | Pose Estimation    | 10-15                | สูง                  | CPU                  | แอปเรียลไทม์บน PC     |
| **OpenPose**         | Pose Estimation    | 0.4 (CPU) / 15 (GPU) | สูงมาก               | แนะนำ GPU            | วิเคราะห์หลายคน       |
| **HRNet**            | Pose Estimation    | 5-10 (GPU)           | ดีที่สุด             | ต้องใช้ GPU          | Benchmark / งานวิจัย  |
| **MLP Classifier**   | Action Recognition | 1000+                | ดี (สำหรับท่าชัดเจน) | CPU                  | ควบคุม Latency ต่ำ    |
| **ST-GCN**           | Action Recognition | 30-50 (GPU)          | สูงมาก               | แนะนำ GPU            | จดจำท่าทางซับซ้อน     |

---

## 4. เหตุผลในการเลือกสถาปัตยกรรมของเรา

จากการวิเคราะห์ข้างต้น โปรเจกต์ **ML-AI Motion Controller** เลือกใช้สถาปัตยกรรมดังนี้:

| ส่วนประกอบ                | ตัวเลือก                        | เหตุผล                                                                                           |
| ------------------------- | ------------------------------- | ------------------------------------------------------------------------------------------------ |
| **Pose Estimation**       | BlazePose (Full) ผ่าน MediaPipe | สมดุลที่ดีที่สุดระหว่างความเร็ว (10-15 FPS) และความแม่นยำสำหรับเกม PC ผู้เล่นคนเดียว ทำงานบน CPU |
| **Action Classification** | MLPClassifier (sklearn)         | Inference ต่ำกว่า 1 มิลลิวินาที เพียงพอสำหรับ 5-9 คลาสการกระทำที่ชัดเจน (ต่อย, บล็อก, หลบ)       |
| **Feature Engineering**   | Velocity + Joint Angles         | จับการเคลื่อนไหวแบบไดนามิกแทนท่าทางนิ่ง สำคัญสำหรับแยก "ต่อย" กับ "ยกมือค้าง"                    |

การผสมผสานนี้ทำให้ระบบทำงานแบบเรียลไทม์บนฮาร์ดแวร์ผู้บริโภคโดยไม่ต้องใช้ GPU เฉพาะ ทำให้เข้าถึงผู้ใช้ได้กว้างขึ้น

---

## สรุปเอกสารอ้างอิง

1. Bazarevsky, V., et al. (2020). _BlazePose: On-device Real-time Body Pose tracking._ arXiv:2006.10204
2. Cao, Z., et al. (2017). _Realtime Multi-Person 2D Pose Estimation using Part Affinity Fields._ arXiv:1611.08050
3. Sun, K., et al. (2019). _Deep High-Resolution Representation Learning for Visual Recognition._ arXiv:1908.07919
4. Weng, C., et al. (2003). _Real-time hand gesture recognition using skin color segmentation and neural networks._ ResearchGate
5. Yan, S., et al. (2018). _Spatial Temporal Graph Convolutional Networks for Skeleton-Based Action Recognition._ arXiv:1801.07455
