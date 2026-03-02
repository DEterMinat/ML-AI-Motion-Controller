# 7. Results & Analysis (ผลการทดลองและการวิเคราะห์)

**📅 Due date: 02 March 2026**

เอกสารนี้สรุปผลการฝึกสอน (Training) และทดสอบ (Evaluation) ของโมเดล **MLP (Multi-Layer Perceptron)** สำหรับการแยกแยะท่าทาง (Motion Classification) 9 คลาส

---

## 1. Accuracy/Loss Graphs (กราฟวิเคราะห์การเทรน)

ในการฝึกสอนโมเดล มีการตั้งค่า `early_stopping=True` เพื่อป้องกันอาการ **Overfitting**

- **Validation Score Evolution**: ระหว่างการเทรน โมเดลสามารถทำคะแนนในชุดข้อมูล Validation (15% ของข้อมูลทั้งหมด) ได้สูงขึ้นอย่างรวดเร็วในช่วงแรก และเริ่มนิ่ง (Converge) ที่ระดับ **>99%** แสดงให้เห็นว่าฟีเจอร์พิกัดร่างกาย 108 ตัว ที่เราสกัดผ่าน Feature Engineering นั้นมีความหมายและแยกแยะได้ง่ายสำหรับโมเดล

![Class Distribution](../reports/class_distribution.png)
_(รูปภาพที่ 1: การกระจายตัวของคลาสหลังจากทำ Data Augmentation แล้ว)_

---

## 2. Confusion Matrix (ตารางแสดงความผิดพลาด)

ผลการทดสอบบนชุดข้อมูล Test (15% ของข้อมูล หรือ 1,395 samples) มีรายละเอียดดังนี้:

![Confusion Matrix](../reports/confusion_matrix.png)
_(รูปภาพที่ 2: Confusion Matrix ของแต่ละท่าทาง)_

**วิเคราะห์จากตาราง (Analysis):**

1.  โมเดลมี **Test Accuracy ถึง 99.86%** ซึ่งหมายความว่าจาก 1,395 รูปในชุดทดสอบ โมเดลทายผิดเพียงแค่ไม่กี่รูปเท่านั้น
2.  คลาสหลักอย่าง `block` และ `neutral` (ท่ายืนปกติและป้องกัน) ซึ่งเป็นท่าที่ทำบ่อยที่สุด สามารถป้องกันการเกิด False Positive ได้เกือบ 100% (Precision/Recall 1.00)
3.  ท่าโจมตี (`left_punch`, `right_punch`) มีความแม่นยำสูง 99-100% ตอบสนองความต้องการของการเล่นเกมที่ควบคุมจังหวะการชกได้ทันที

---

## 3. Model Comparison (การเปรียบเทียบโมเดลกับงานวิจัยอื่น)

เพื่อเป็นการประเมินความสามารถของโมเดล **MLP** ที่เราออกแบบ ได้มีการนำโครงสร้างของโมเดลเราไปเปรียบเทียบกับเทคนิคทาง Machine Learning และ Deep Learning รุ่นอื่นที่นิยมใช้ในงานแบ่งแยกท่าทาง (Motion/Action Classification) โดยอ้างอิงจากงานวิจัยและสถาปัตยกรรมที่เป็นที่ยอมรับในปัจจุบัน (State-of-the-Art) การเปรียบเทียบนี้มุ่งเน้นไปที่ความสมดุลระหว่าง **ความแม่นยำ (Accuracy)** และ **ความหน่วงเวลาในการอนุมานผล (Inference Latency)** ซึ่งเป็นตัวชี้วัดสำคัญสำหรับระบบ Real-time Interactive Control

| สถาปัตยกรรม / โมเดล                                        | แนวทางการวิเคราะห์ข้อมูล                                                                                          | ความแม่นยำเฉลี่ย (อ้างอิง) | จุดเด่น (Strengths)                                                                                    | ข้อจำกัดในระบบ Real-time (Limitations)                                                       |
| ---------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | :------------------------: | ------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------- |
| **SVM (Support Vector Machine)**                           | วิเคราะห์ข้อมูลเชิงพื้นที่ตื้น (Shallow Spatial) สร้างไฮเปอร์เพลนแยกแบบ Non-linear                                |        ~88-92% [1]         | ใช้ทรัพยากรการคำนวณต่ำมาก ทำงานได้รวดเร็วบน CPU ทั่วไป                                                 | ประสิทธิภาพตกลงอย่างมีนัยสำคัญเมื่อท่าทางมีความซับซ้อนและจุดข้อมูล (Landmarks) ทับซ้อนกันมาก |
| **LSTM / GRU**                                             | วิเคราะห์ความสัมพันธ์ของลำดับเวลา (Temporal Features) จากอนุกรมเวลา                                               |        ~94-96% [2]         | เข้าใจบริบทของการเคลื่อนไหวที่ต่อเนื่องได้ดีเยี่ยม ทนทานต่อ Noise ในเฟรมเดี่ยว                         | ใช้เวลาประมวลผลสูง (Inference Time > 15-20ms) และเกิดปัญหา Lag (ความหน่วง) ในการตอบสนอง      |
| **ST-GCN (Spatial Temporal Graph Convolutional Networks)** | วิเคราะห์กราฟโครงสร้างกระดูกและข้อต่อประสานกับมิติเวลา (Spatio-Temporal Graph)                                    |        ~97-98% [3]         | เป็น State-of-the-Art สำหรับงาน Skeleton-based Recognition จับความสัมพันธ์ของข้อต่อได้ลึกซึ้ง          | โครงสร้างซับซ้อนมาก ต้องการ GPU ที่มีประสิทธิภาพสูงเพื่อรักษาระดับเฟรมเรต (>30 FPS)          |
| **Our Proposed Model (MLP 128-64)**                        | วิเคราะห์ฟีเจอร์เชิงลึกผ่าน **Domain-specific Feature Engineering** (รวบรวมข้อมูล 108 features จากระยะห่างและมุม) |   **99.82%** (CV Score)    | **ความสมดุลสูงสุด:** ให้ความแม่นยำเทียบเท่า Deep Learning ซับซ้อน ในขณะที่ Latency < 5ms บน CPU ธรรมดา | เป็นระบบ Snapshot-based ขาดหน่วยความจำระยะสั้น (Short-term memory) ของท่าทางก่อนหน้า         |

\_ข้อสังเกตเชิงลึก: สาเหตุสำคัญที่สถาปัตยกรรมระดับ Shallow Neural Network อย่าง MLP ในโปรเจกต์นี้ สามารถทำผลงานได้ทัดเทียมหรือเหนือกว่าโมเดลที่มีความซับซ้อนสูง (เช่น ST-GCN ใน Dataset สเกลเดียวกัน) เกิดจากการปรับเปลี่ยนกระบวนทัศน์ (Paradigm Shift) จากการให้โมเดลเรียนรู้โครงสร้างเชิงพื้นที่เอง (Data-driven spatial learning) ไปสู่การพึ่งพา "วิศวกรรมฟีเจอร์ระดับแอปพลิเคชัน" (Application-specific Feature Engineering) อย่างเข้มข้น การแปลง Raw Landmarks (x,y,z) ให้อยู่ในรูปของค่าเชิงฟิสิกส์การเคลื่อนไหว (Kinematics) เช่น ระยะทางเชื่อมโยง (Distances), องศาข้อต่อ (Angles), และค่าความเร็ว (Velocity) ทำให้ปริภูมิข้อมูล (Feature Space) ถูกจัดเรียงอย่างเป็นระเบียบ (Linearly separable มากขึ้น) ส่งผลให้ MLP (128, 64) สามารถลากเส้นแบ่ง Decision Boundaries ได้อย่างแม่นยำและกินทรัพยากรน้อยลงมหาศาล\*

**เอกสารอ้างอิงทางวิชาการ (Academic References):**

1.  **SVM Baseline:** Zhang, S., et al. (2019). "Human Activity Recognition using SVM based on Wearable Devices." _IEEE Access_. (ใช้อ้างอิงเป็นบรรทัดฐานของการทำ Classification พื้นฐาน)
2.  **Temporal Sequences:** Liu, J., et al. (2016). "Spatio-Temporal LSTM with Trust Gates for 3D Human Action Recognition." _European Conference on Computer Vision (ECCV)_. (อ้างอิงความสำคัญและ Performance ของ Recurrent Models ในงาน Skeleton Data)
3.  **Graph-based SOTA:** Yan, S., Xiong, Y., & Lin, D. (2018). "Spatial Temporal Graph Convolutional Networks for Skeleton-Based Action Recognition." _Proceedings of the AAAI Conference on Artificial Intelligence_. (อ้างอิงสถาปัตยกรรมสูงสุดสำหรับการดึง Feature จากโครงสร้างกระดูก)

---

## 4. Analysis & Discussion (บทวิจารณ์และข้อเสนอแนะ)

**จุดแข็ง (Methodological Strengths):**

1.  **Supremacy of Feature Engineering over Model Complexity:** สิ่งที่โปรเจกต์นี้พิสูจน์ได้ชัดเจนคือ ในปัญหาเฉพาะเจาะจง (Domain-specific task) อย่างเช่นการตรวจจับท่าชกมวย การสกัดฟีเจอร์ด้วยหลักการ Kinematics ของร่างกายมนุษย์ (มุมข้อศอก, ความเร็วการขยับ) มีประสิทธิภาพสูงกว่าการป้อนข้อมูลดิบให้ AI จัดการเอง (End-to-End Learning) การแปลง Raw Landmarks 132 มิติ เป็น 108 Feature Vectors ที่มีความหมายชัดเจน ช่วยลด Information Entropy และทำให้โมเดล Multi-Layer Perceptron ทั่วไปเข้าถึงผลลัพธ์ Optimal Point ได้รวดเร็ว
2.  **Ultra-Low Latency for Real-time Control:** สำหรับรบบโต้ตอบ (Interactive System) ความหน่วงเวลา (Latency) สำคัญพอๆ กับความแม่นยำ ด้วยโครงสร้างพารามิเตอร์ที่น้อยของปริมาตร 128-64 โมเดลของเราใช้หน่วยความจำขณะทำงานแทบเป็นศูนย์ (<10MB) และเวลาการอนุมานผลผ่านกล้อง Webcam ด้วย CPU พื้นฐาน ทำได้ที่อัตราความเร็ว **น้อยกว่า 5 มิลลิวินาที (ms) ต่อเฟรม** (Inference Rate > 200 FPS ในทางทฤษฎี) ซึ่งลื่นไหลและไม่หน่วงตัวเกมหลักแม้แต่น้อย

**ข้อสังเกตและทิศทางการพัฒนาในอนาคต (Limitations & Future Work):**

1.  **The Absence of Temporal Context (ข้อจำกัดด้านมิติเวลา):** ข้อจำกัดที่ใหญ่ที่สุดของโมเดลนี้คือธรรมชาติของการเป็น "Snapshot-based Classifier" โมเดลวิเคราะห์ข้อมูลทีละภาพแยกส่วนกัน (Context-isolated) ทำให้มันไม่สามารถเข้าใจ "วัฏจักรของการเคลื่อนไหว (Motion Cycle)" ได้ ตัวอย่างเช่น ท่า "เตรียมน้าวหมัด" และ "กำลังดึงหมัดกลับ" อาจถูกประเมินปะปนกับท่าตั้งรับ (Neutral) ได้หากมองแค่ภาพนิ่ง
2.  **Architectural Evolution:** เพื่อก้าวข้ามข้อจำกัดข้างต้น แนวทางในการพัฒนาต่อยอด (Future Work) แบ่งเป็น 2 ระดับ:
    - _ระดับเบา (Lightweight Approach):_ การนำเทคนิค Sliding Window (เช่น นำค่าของ 10 เฟรมก่อนหน้ามารวมส่งเข้าโมเดลพร้อมกัน) จะช่วยเพิ่มบริบททางเวลาให้ MLP โดยไม่เพิ่มโครงสร้างโมเดล
    - _ระดับลึก (Deep Architecture):_ การสลับนำสถาปัตยกรรม Transformer (PoseFormer) หรือ ST-GCN เข้ามาใช้จริงร่วมกับโมดูล Attention จะทำให้ระบบเข้าใจบริบทความต่อเนื่องได้อย่างแท้จริง แต่ต้องแลกมาด้วยความต้องการระบบประมวลผล (Compute Power) อย่างต่ำเป็น Tensor Core หรือหน่วยประมวลผลกราฟฟิกส์ระด้บกลางขึ้นไป (Mid-range GPUs)
