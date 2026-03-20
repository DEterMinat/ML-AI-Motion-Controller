📋 02739431-64 Machine Learning
ML/DL Final Project – Overall Progress Evaluation Form (2/2025)
Course-Title: Machine Learning / Deep Learning
Semester: 2/2025
Instructor: Dr. Somsawut Nindam
Project Duration:
📅 Start: 19 January 2025
📅 Final Deadline: 09 March 2025
________________________________________
👥 Student / Group Information
●	Group Title: Detect AI motion boxing controller
●	Group Members:
1.	นายธนกฤษ ศิริธีรพันธ์ 6630202261
2.	นายธีรวัจน์ ศิริพิศ 6630202384
3.	นางสาวณัฐธิดา เชี่ยวเลี่ยน 6630202180
4.	นายปพนสรรค์ ลีนิน 6630202473
●	Project Domain (ML/DL):
☑ Computer Vision ☐ NLP ☐ Tabular ML ☐ Time‑Series ☐ Audio 
☑ Other: MLPClassifier_____________________________________________
✅ Overall Project Progress Evaluation
1. Proposed & Accepted Topic
📅 Due date: 19 January 2025
Required:
☑ Project title: Detect AI motion boxing controller
☐ Motivation
☐ Dataset selected (❌ NOT FER2013 / ❌ NOT Spam Mail)
Status:
☑ Pass ☐ Not Pass





Remarks:
Motivation (ที่มาและความสำคัญ)
ในปัจจุบันการเล่นเกมด้วยอุปกรณ์พื้นฐานเช่นเมาส์และคีย์บอร์ดมักขาดความสมจริงและการมีส่วนร่วมทางกายภาพ ในขณะที่เทคโนโลยีอย่าง Virtual Reality (VR) หรือเซนเซอร์จับการเคลื่อนไหว (เช่น Kinect) สามารถแก้ปัญหานี้ได้ แต่กลับมีราคาสูง ติดตั้งยุ่งยาก และต้องใช้คอมพิวเตอร์สเปคสูง โครงการนี้จึงมีแนวคิดที่จะพัฒนาระบบควบคุมเกมด้วยการเคลื่อนไหว (Motion Controller) โดยเปลี่ยน "กล้องเว็บแคมธรรมดา"ให้กลายเป็นจอยเกมความแม่นยำสูง ด้วยการประยุกต์ใช้เทคโนโลยี Computer Vision (MediaPipe) ร่วมกับปัญญาประดิษฐ์ (AI) โดยมีวัตถุประสงค์หลักดังนี้:
•	เพิ่มความสมจริง: ผู้เล่นสามารถออกท่าทางจริง เช่น ต่อย หรือหลบ เพื่อควบคุมตัวละครในเกมได้แบบ Real-time
•	เข้าถึงง่าย: ไม่ต้องใช้อุปกรณ์สวมใส่หรือเซนเซอร์ราคาแพง เพียงแค่มีแล็ปท็อปหรือกล้อง USB ก็สามารถใช้งานได้
•	ประมวลผลรวดเร็ว: ออกแบบระบบให้ทำงานได้ลื่นไหลที่ 60 FPS บนซีพียูทั่วไป เพื่อให้ตอบสนองทันต่อเกมแนวต่อสู้ที่ต้องใช้ความไวสูง

2. Dataset Selected (ชุดข้อมูลที่เลือกใช้)
เนื่องจากชุดข้อมูลมาตรฐานที่มีอยู่ทั่วไป (เช่น UCI HAR) มักเน้นกิจกรรมในชีวิตประจำวันอย่างการเดินหรือนั่ง ซึ่งไม่ตอบโจทย์การตรวจจับท่าทางการต่อสู้ที่มีความซับซ้อน โครงการนี้จึงเลือกใช้ Custom Skeleton-Based Dataset ที่สร้างขึ้นเอง
•	แหล่งที่มาของข้อมูล: เก็บรวบรวมข้อมูลใหม่ทั้งหมดผ่านระบบ Data Collection ของตัวโปรแกรม เพื่อให้มุมกล้องและสภาพแวดล้อมตรงกับการใช้งานจริงมากที่สุด
•	ลักษณะข้อมูล: แทนที่จะใช้ภาพวิดีโอขนาดใหญ่ เราเลือกใช้ พิกัดโครงกระดูก (Skeletal Landmarks) จาก MediaPipe Pose
o	การคัดเลือกฟีเจอร์: ใช้เฉพาะ 14 จุดครึ่งตัวบน (หัวไหล่, ศอก, ข้อมือ, เอว) เพื่อลดสัญญาณรบกวนจากการขยับขา
o	วิศวกรรมข้อมูล (Feature Engineering): มีการเพิ่มค่า ความเร็ว และ องศาข้อต่อ เข้าไปในชุดข้อมูล เพื่อให้ AI แยกแยะท่าทางได้แม่นยำขึ้น (เช่น แยกท่าตั้งการ์ดออกจากท่าต่อยโดยดูจากความเร็วการยืดแขน)
•	คลาสของข้อมูล (Classes): ประกอบด้วย 9 ท่าทางสำหรับเกมต่อสู้ ได้แก่:
ท่าเตรียม (Neutral)
หมัดซ้าย (Left Punch)
หมัดขวา (Right Punch)
ตั้งการ์ด (Block)
การหลบ 4 ทิศทาง (Dodge Left, Right, Front, Back)
ท่าไม้ตาย (Special attack)


________________________________________








2. Problem Statement
📅 Due date: 26 January 2025
Required:
☑ Input → Task → Output
☑ Why ML/DL is needed
☑ Success metrics
Status:
☑ Pass ☐ Not Pass
Remarks:
ระบบมีการทำงานแบบ End-to-End Pipeline ดังนี้:
•	Input (ข้อมูลนำเข้า):
o	ภาพวิดีโอสดจากกล้อง Webcam (Live Video Feed) ความละเอียด 640x480 พิกเซล
•	Task (การประมวลผล):
o	Pose Estimation: ใช้ MediaPipe แปลงภาพคนให้เป็นพิกัดจุดโครงกระดูก (Landmarks) แบบ 3 มิติ (x, y, z)
o	Feature Extraction: คำนวณค่าสำคัญทางฟิสิกส์ เช่น องศาข้อต่อ และความเร็วการเคลื่อนที่ของข้อมือ
o	Classification: ส่งค่าเหล่านี้เข้าสู่โมเดล AI (Neural Network) เพื่อทำนายว่า "ขณะนี้ผู้ใช้กำลังทำท่าอะไร"
•	Output (ผลลัพธ์):
o	Action Label: ชื่อท่าทางที่ตรวจจับได้ (เช่น "Right Punch")
o	Game Control: โปรแกรมจำลองการกดคีย์บอร์ด/เมาส์ไปยังเกมโดยตรง (เช่น ต่อยขวา -> คลิกเมาส์ขวา)
o	WebSocket API: ทำหน้าที่เป็นตัวกลางในการส่งต่อข้อมูล (JSON Payload) ไปยังเกมเอนจินอื่นๆ อย่าง Unity หรือ Roblox (เช่น ส่งไปที่พอร์ต 8765)
o	Overlay HUD: แสดงสถานะการทำงาน (App/Cam FPS) และความมั่นใจของ AI บนจอโปรแกรมแบบ Real-time (พัฒนาระบบ UI ด้วย CustomTkinter)
________________________________________
Why ML/DL is needed? (ทำไมต้องใช้ Machine Learning)
การเขียนโปรแกรมแบบดั้งเดิม (Rule-based Programming) ไม่สามารถตอบโจทย์โจทย์นี้ได้ดีพอ เพราะ:
•	ความซับซ้อนของมิติ: การเขียนเงื่อนไข if-else เพื่อดักจับท่าทาง 3 มิติจากมุมกล้องที่หลากหลายนั้นซับซ้อนเกินไป (เช่น ท่าต่อยตรง กับ ต่อยแย็บ อาจมีพิกัดใกล้เคียงกันมาก แต่ต่างกันที่ความเร็วและจังหวะ)
•	ความหลากหลายทางสรีระ: ผู้ใช้งานแต่ละคนมีความสูง ความยาวแขน และสไตล์การออกท่าทางที่ไม่เหมือนกัน กฎตายตัว (Hard-coded rules) จึงมักใช้ไม่ได้ผลกับทุกคน
•	ความยืดหยุ่น: Machine Learning สามารถเรียนรู้รูปแบบของท่าทางผ่านตัวอย่างข้อมูลจำนวนมาก ทำให้ระบบมีความยืดหยุ่นสามารถตรวจจับท่าทางได้แม่นยำแม้ผู้ใช้จะยืนระยะห่างต่างกัน หรือมีสภาพแสงที่เปลี่ยนไป 
ซึ่งแบบ Rule-based ทำได้ยาก






________________________________________
Success Metrics (ตัวชี้วัดความสำเร็จ)
เพื่อให้ระบบสามารถใช้งานเป็นจอยเกมได้จริง เรากำหนดเกณฑ์วัดผลไว้ดังนี้:
•	ความแม่นยำ (Accuracy):
o	โมเดลต้องมีความแม่นยำในการทายท่าทาง มากกว่า 90% (บน Test Set) เพื่อไม่ให้เกิดการกดปุ่มผิดพลาดขณะเล่น
•	ความเร็วในการตอบสนอง (Latency):
o	เวลาในการประมวลผลต่อเฟรม (Inference Time) ต้อง น้อยกว่า 30 มิลลิวินาที (เพื่อให้ทันรอบการทำงานแบบ Real-time)
•	ความเสถียร (Stability / FPS):
o	ระบบต้องรักษาระดับเฟรมเรตได้คงที่ 60 FPS เพื่อความลื่นไหลของภาพและการควบคุม
•	ความรู้สึกผู้ใช้ (User Experience):
o	ระบบต้องไม่มีอาการ "เผลอกด" (False Positive) หรือกดค้างเอง และต้องรองรับการกดท่าต่อเนื่อง (Combo) ได้อย่างเป็นธรรมชาติ

________________________________________
3. Dataset Description
📅 Due date: 02 February 2025
Required:
☑ Dataset source (URL)
☑ Sample visualizations
☑ Preprocessing plan
Status:
☑ Pass ☐ Not Pass
Remarks:
Dataset Source (แหล่งที่มาและข้อจำกัดของข้อมูล)
Source Type: รวบรวมด้วยตนเอง
เนื่องจากเป็นข้อมูลที่สร้างขึ้นเฉพาะกิจสำหรับโครงงานนี้ (Custom Dataset) จึงไม่มี URL สาธารณะ แต่มีคุณลักษณะพิเศษคือ ตรงตามบริบทการใช้งานจริงหน้ากล้อง Webcam อย่างไรก็ตาม การเก็บข้อมูลเองมีข้อจำกัดที่สำคัญดังนี้:
•	ความหลากหลายของกลุ่มตัวอย่าง (Demographic Bias): ข้อมูลส่วนใหญ่มาจากผู้พัฒนาและอาสาสมัครจำนวนจำกัด (1-3 คน) ทำให้โมเดลอาจเรียนรู้จำเพาะกับสรีระ (ความสูง/ความยาวแขน) ของคนกลุ่มนี้ หากนำไปใช้กับคนที่มีรูปร่างแตกต่างกันมาก (เช่น เด็กเล็ก หรือคนตัวสูงมาก) อาจมีความแม่นยำลดลง
•	ความซับซ้อนของถสภาพแวดล้อม (Environmental Bias): ข้อมูลถูกเก็บในสภาพแสงและฉากหลังที่ค่อนข้างคงที่ หากนำไปใช้ในที่มืด หรือมีฉากหลังที่มีสิ่งรบกวนเยอะเกินไป อาจส่งผลต่อประสิทธิภาพของ MediaPipe ในการจับจุดกระดูกได้
•	ปริมาณข้อมูล (Volume Consideration): ขนาดของ Dataset (ประมาณ 2,500 - 3,000 ตัวอย่าง) เพียงพอสำหรับ Neural Network ขนาดเล็ก แต่ยังถือว่าน้อยหากเทียบกับ Deep Learning ระดับอุตสาหกรรม
________________________________________
Sample Visualizations (ตัวอย่างการแสดงผล)
เพื่อให้เห็นภาพรวมของข้อมูล เรามีการนำเสนอผ่าน 2 รูปแบบหลัก:
•	Skeletal Overlay Visualization:
o	การวาดเส้นโครงกระดูก (สีเขียว/น้ำเงิน) ทับลงบนภาพวิดีโอ เพื่อยืนยันว่าข้อมูล Input (จุด x, y) ตรงกับท่าทางจริงของผู้เล่น
•	Class Distribution Plot:
o	กราฟแท่งแสดงจำนวนตัวอย่างของแต่ละท่าทาง (Action Classes) เพื่อตรวจสอบความสมดุลของข้อมูล (Class Balance)

________________________________________
Preprocessing Plan (แผนการเตรียมข้อมูล)
ก่อนนำข้อมูลดิบเข้าสู่โมเดล เรามีขั้นตอนการเตรียมข้อมูล (Pipeline) ดังนี้:
•	Data Cleaning (ทำความสะอาดข้อมูล):
o	ลบเฟรมที่ MediaPipe จับภาพคนไม่ได้ (Null Frames)
o	กรองค่าพิกัดที่ผิดปกติ (Outliers) ที่เกิดจากแสงเพี้ยนหรือวัตถุรบกวน
•	Coordinate Normalization (สำคัญมาก):
o	แปลงพิกัดจุดทั้งหมดให้อยู่ในระบบ Relative Coordinate โดยใช้ "จุดกึ่งกลางสะโพก" เป็นจุดอ้างอิง (0,0)
o	ปรับขนาด (Scale) ให้ความยาวลำตัวเป็นเท่ากันเสมอ ซึ่งจะช่วยแก้ปัญหาเรื่องระยะห่างจากกล้อง
 (ยืนไกล/ยืนใกล้) และความแตกต่างของส่วนสูงผู้ใช้งานได้
•	Feature Engineering (การสร้างฟีเจอร์ใหม่):
o	Velocity Calculation: คำนวณความเร็วของ "ข้อมือ" จากเฟรมปัจจุบันเทียบกับเฟรมก่อนหน้า เพื่อให้ AI แยกแยะ "ท่าค้าง" (Static) กับ "ท่าต่อย" (Dynamic) ได้
o	Joint Angles: คำนวณองศาของข้อศอกและหัวไหล่ เพื่อเพิ่มมิติความลึกให้กับข้อมูล
•	Scaling:
o	ใช้ StandardScaler เพื่อปรับค่าข้อมูลทั้งหมดให้อยู่ในช่วงมาตรฐาน (Mean=0, SD=1) ช่วยให้ Neural Network เรียนรู้และหาค่าที่เหมาะสม (Gradient Descent) ได้เร็วยิ่งขึ้น

________________________________________














4. Literature Review
📅 Due date: 09 February 2025
Required:
☑ 3–5 ML/DL related works
☑ Comparison table
Status:
☑ Pass ☐ Not Pass
Remarks:
การวิเคราะห์โมเดล Machine Learning สำหรับระบบประมาณท่าทางและการจดจำการกระทำแบบเรียลไทม์
การพัฒนาโปรเจกต์ ML-AI Motion Controller จำเป็นต้องอาศัยการผสมผสานระหว่างเทคโนโลยี Pose Estimation (การระบุพิกัดร่างกาย) และ Action Recognition (การจำแนกท่าทาง) เพื่อเปลี่ยนการเคลื่อนไหวของผู้ใช้ให้เป็นคำสั่งควบคุม โดยมีรายละเอียดแนวทางที่น่าสนใจดังนี้:
1. โมเดลการประมาณท่าทาง (Pose Estimation Models)
1.1 BlazePose (MediaPipe)
•	ประเภท: Top-Down Approach (เน้นตรวจจับบุคคลเดียว)
•	สถาปัตยกรรม: ใช้ระบบ Two-stage pipeline ประกอบด้วย Detector (ระบุตำแหน่งคน) และ Tracker (ระบุพิกัดข้อต่อ) พัฒนาบนพื้นฐานของ MobileNetV2 และ Regression Heads เพื่อระบุจุดพิกัด 33 จุดในรูปแบบ 3 มิติ
•	จุดเด่น: ใช้เทคนิค Heatmap ร่วมกับ Regression ทำให้ความแม่นยำสูงถึงระดับ Sub-pixel ในขณะที่ใช้ทรัพยากรต่ำมาก
•	ประสิทธิภาพ: ทำความเร็วได้มากกว่า 30 FPS บน CPU ของอุปกรณ์พกพา
Paper: BlazePose: On-device Real-time Body Pose tracking
1.2 OpenPose
•	ประเภท: Bottom-Up Approach (ตรวจจับได้หลายคนพร้อมกัน)
•	สถาปัตยกรรม: ใช้ Part Affinity Fields (PAFs) ในการเชื่อมโยงจุดพิกัดต่างๆ เข้าด้วยกันเพื่อสร้างโครงกระดูกของแต่ละบุคคล มีโครงสร้าง CNN แบบสองสาขา (Dual-branch)
•	จุดเด่น: เป็นระบบแรกที่พิสูจน์ว่าสามารถทำ Multi-person 2D Pose Estimation แบบเรียลไทม์ได้จริง
•	ข้อจำกัด: บริโภคทรัพยากรสูง (ต้องใช้ GPU ประสิทธิภาพสูงเพื่อคงความเร็วระดับ Real-time)
Paper: OpenPose: Realtime Multi-Person 2D Pose Estimation using Part Affinity Fields
1.3 HRNet (High-Resolution Network)
•	ประเภท: High-Precision Top-Down Approach
•	สถาปัตยกรรม: รักษาความละเอียดของข้อมูล (High-resolution representations) ไว้ตลอดทั้งเครือข่าย โดยการเชื่อมต่อ Subnetworks หลายความละเอียดเข้าด้วยกันแบบขนาน
•	จุดเด่น: ให้ค่าความแม่นยำ (Accuracy) สูงที่สุดในปัจจุบัน เหมาะสำหรับงานวิจัยที่ต้องการความละเอียดระดับสูง
•	ข้อจำกัด: Latency สูง ไม่เหมาะกับการใช้งานบนอุปกรณ์ที่มีทรัพยากรจำกัด
Paper: Deep High-Resolution Representation Learning for Visual Recognition
2. โมเดลการจดจำการกระทำ (Action Recognition Models)
2.1 MLP Classifier (Feature-based)
•	โครงสร้าง: Multi-layer Perceptron ขนาดเล็ก (2-3 ชั้น) ที่รับข้อมูล Input เป็นค่าพิกัด (Coordinates), มุมของข้อต่อ (Angles) หรือความเร็วการเคลื่อนที่ (Velocity)
•	ข้อดี: ประมวลผลเร็วมาก (Inference time < 1ms), ใช้หน่วยความจำน้อย และฝึกสอนโมเดลได้ง่าย
•	ข้อเสีย: จำเป็นต้องทำ Feature Engineering (การสกัดคุณลักษณะด้วยมือ) และประสิทธิภาพอาจลดลงหากท่าทางมีความซับซ้อนเชิงเวลาสูง
Library:: MLPClassifier — scikit-learn 1.8.0 documentation
2.2 ST-GCN (Spatial-Temporal Graph Convolutional Network)
•	โครงสร้าง: ประยุกต์ใช้ Graph Convolution เข้ากับข้อมูลโครงกระดูก โดยมองข้อต่อเป็น Node และกระดูกเป็น Edge พร้อมวิเคราะห์การเปลี่ยนแปลงผ่านมิติเวลา (Temporal)
•	ข้อดี: เรียนรู้ความสัมพันธ์เชิงพื้นที่และจังหวะเวลาได้โดยอัตโนมัติ แม่นยำสูงมากสำหรับท่าทางที่ซับซ้อน
•	ข้อเสีย: โมเดลมีขนาดใหญ่และต้องการ GPU ในการประมวลผลเพื่อให้ทันต่อเหตุการณ์ (Real-time)
Paper: Spatial Temporal Graph Convolutional Networks for Skeleton-Based Action Recognition
________________________________________
3. ตารางเปรียบเทียบสมรรถนะ (Performance Comparison)
โมเดล / แนวทาง	หน้าที่หลัก	ความเร็ว (FPS)	ความแม่นยำ	ฮาร์ดแวร์ที่แนะนำ	การใช้งานที่เหมาะสม
BlazePose (Full)	Pose Estimation	10-15 (CPU)	สูง	ทั่วไป / PC	แอปฯ Real-time บนคอมพิวเตอร์
OpenPose	Pose Estimation	15 (GPU)	สูงมาก	High-end GPU	วิเคราะห์ฝูงชน / หลายคน
HRNet	Pose Estimation	5-10 (GPU)	ดีที่สุด	High-end GPU	งานวิจัย / มาตรฐานความแม่นยำสูง
MLP Classifier	Action Recognition	1000+	ปานกลาง-สูง	CPU	ระบบควบคุมที่ต้องการ Latency ต่ำ
ST-GCN	Action Recognition	30-50 (GPU)	สูงมาก	GPU	การวิเคราะห์ท่าทางระดับสูง
________________________________________
4. สถาปัตยกรรมที่เลือกใช้สำหรับ ML-AI Motion Controller
เพื่อให้ตอบโจทย์การใช้งานในรูปแบบการควบคุมเกม (Gaming Controller) ที่ต้องมีความลื่นไหลและประมวลผลบนเครื่องทั่วไปได้ โปรเจกต์นี้จึงเลือกใช้สถาปัตยกรรมแบบ Hybrid ดังนี้:
•	Pose Estimation: BlazePose (Full Mode) via MediaPipe
o	เหตุผล: ให้ความสมดุลระหว่างความเร็วและความแม่นยำ สามารถทำงานบน CPU ได้ดี ทำให้เข้าถึงกลุ่มผู้ใช้ทั่วไปได้ง่าย
•	Action Classification: MLP Classifier (Scikit-learn)
o	เหตุผล: ให้ค่า Inference ต่ำกว่า 1 มิลลิวินาที ซึ่งสำคัญมากในการเล่นเกม (Input Lag ต้องต่ำที่สุด) รองรับคลาสการกระทำหลัก เช่น ต่อย, บล็อก, และหลบ ได้อย่างแม่นยำ
•	Feature Engineering: Multi-dimensional Vectors
o	เทคนิค: คำนวณหา Velocity (ความเร็วการขยับ) และ Joint Angles (มุมข้อต่อ) เพื่อช่วยโมเดลแยกแยะระหว่าง "การทำท่าค้างไว้" กับ "การขยับโจมตี" ได้อย่างเด็ดขาด
5. Methods (Model Design)
📅 Due date: 16 February 2025
Required:
☑ Model architecture diagram
☑ Explanation of ML/DL model
Status:
☑ Pass ☐ Not Pass
Remarks:
1. ผังโครงสร้างสถาปัตยกรรม (Model Architecture Diagram)
โครงสร้างของระบบ Neural Network ที่ใช้ในการประมวลผลท่าทาง
 
2. คำอธิบายโมเดล ML/DL (Explanation of ML/DL Model)
แนวคิดหลัก: Frame-by-Frame Classification (MLP)
โมเดลหลักที่เลือกใช้คือ Multi-Layer Perceptron (MLP) ซึ่งเป็น Neural Network แบบ Fully Connected ที่ทำหน้าที่จำแนกท่าทางแบบ ทีละเฟรม (Snapshot-based) โดยอาศัยการทำ Feature Engineering ที่เข้มข้นถึง 108 คุณลักษณะ เพื่อให้ได้ความแม่นยำสูงสุดโดยไม่ต้องพึ่งพาข้อมูลอนุกรมเวลา (Time-series) ที่ซับซ้อน
1. การออกแบบคุณลักษณะ (Feature Engineering — 108 Pro-Level Features)
เราเปลี่ยนข้อมูลดิบ (Raw Data) 132 ค่าจาก MediaPipe Pose (33 landmarks × 4) ให้กลายเป็น 108 คุณลักษณะ ที่มีความหมายเชิงจลนศาสตร์ (Kinematics):
กลุ่มคุณลักษณะ (Feature Group)	จำนวน	รายละเอียดเชิงลึก
Body Landmarks (14 จุดหลัก)	56	ค่า x, y, z และ visibility ของจุดที่ส่งผลต่อการเคลื่อนไหว
Key Angles	4	มุมของข้อศอก (L/R) และข้อไหล่ (L/R) เพื่อระบุลักษณะการงอ/เหยียด
Velocity (4 จุดสำคัญ)	12	อัตราความเร็ว ($\Delta$ position) เพื่อแยกแยะการเคลื่อนที่เร็ว/ช้า
Bone Vectors (6 ส่วน)	18	ทิศทางและเวกเตอร์ของกระดูกแต่ละส่วน (Directional Vectors)
Acceleration (4 จุดสำคัญ)	12	ความเร่ง ($\Delta$ velocity) เพื่อตรวจจับแรงปะทะหรือการออกหมัด
Distance Features	6	ระยะห่างระหว่างจุดสำคัญ เช่น มือกับใบหน้า หรือ มือกับสะโพก
รวมทั้งหมด	108	
2. เหตุผลที่เลือกใช้ MLP
•	Fast Inference: ประมวลผลได้รวดเร็ว (< 5ms ต่อเฟรม) รองรับการใช้งานแบบ Real-time 60 FPS ได้สบาย
•	High Accuracy: ด้วย Feature Engineering ที่แม่นยำ ทำให้ MLP สามารถทำ Accuracy ได้สูงกว่า 95%
•	Low Resource Consumption: ไม่จำเป็นต้องใช้ GPU ในการประมวลผล (CPU-friendly)
•	Simple Deployment: จัดเก็บและโหลดโมเดลผ่าน pickle หรือ joblib ได้ง่าย
3. ลำดับขั้นตอนการทำงาน (Processing Pipeline)
1.	Input: รับเฟรมภาพจาก Webcam (ผ่านระบบ Threaded Camera Stream เพื่อลดการเกิดคอขวดและรักษา 60 FPS)
2.	Detection: MediaPipe สกัดจุด Landmark 33 จุด (132 values)
3.	Transformation: แปลงข้อมูลเป็น 108 Features ผ่านฟังก์ชัน transform_dataset (Velocity, Angles, Bone Vectors)
4.	Normalization: ปรับค่าด้วย StandardScaler (Mean = 0, Std = 1)
5.	Classification: ส่งเข้า MLP (256 $\rightarrow$ 128 $\rightarrow$ 64 neurons)
6.	Decision & Smoothing: ใช้ Softmax หาความน่าจะเป็น หากความน่าจะเป็นสูงกว่า 0.80 จะส่งให้โมดูล Motion Analyzer ทำหน้าที่กรองความถูกต้อง (Consistency Filter/Voting) ก่อนจะส่งเป็นคำสั่งเข้าเกม বা Broadcast ข้าม WebSocket
3. ผังแสดงระบบการทำงานรวม (Full System Pipeline)
การเชื่อมโยงตั้งแต่การรับภาพจนถึงการควบคุมตัวละครในเกม
 

4.Class
dataset/by_class
 — 9 Classes
Class	Samples	คำอธิบาย
block	500	ท่าป้องกัน — ยกแขนขึ้นบังหน้า/หน้าอก
neutral	500	ท่ายืนปกติ — ไม่มีการเคลื่อนไหว
dodge_back	300	หลบถอยหลัง — โน้มตัวหรือก้าวถอยหลัง
dodge_front	300	หลบไปข้างหน้า / Dash — โน้มตัวหรือก้าวข้างหน้า
dodge_left	300	หลบไปซ้าย — เคลื่อนตัวหรือโน้มไปทางซ้าย
dodge_right	300	หลบไปขวา — เคลื่อนตัวหรือโน้มไปทางขวา
final_skill	300	ท่าไม้ตาย — ท่า unique ที่แตกต่างชัดเจน
left_punch	300	ต่อยซ้าย — เหยียดแขนซ้ายออกไปข้างหน้า
right_punch	300	ต่อยขวา — เหยียดแขนขวาออกไปข้างหน้า
รวม	3,100	
________________________________________
ข้อสังเกต:
•	block และ neutral มี 500 samples (มากกว่า class อื่น) เพราะเป็นท่าที่ระบบต้องแยกให้ได้ชัดที่สุด — neutral ใช้เป็นท่ามาตรฐานที่ต้องป้องกันไม่ให้เด้งไปท่าอื่น และ block ต้องไม่ถูก trigger ผิด
•	class อื่นๆ อยู่ที่ 300 samples เท่ากัน
•	Dataset นี้เป็น raw data ก่อน augmentation $\rightarrow$ หลัง augment (factor=2) จะได้ประมาณ 9,300 samples ก่อน train จริง ถือได้ว่าข้อมูลมีความสมดุล
•	แต่ dodge_back ทำได้ยากมากทำให้ Model จับไม่ได้บางครั้งในเวอร์ชันเก่า แต่ปัจจุบันได้รับการแก้ไขเพิ่มใน 108 features (มีระบบ Distance Feature และ Z-axis) แล้ว

                
6. Experiment Plan
📅 Due date: 23 February 2025
Required:
☐ Baseline model
☐ Hyperparameters
☐ Evaluation metrics
☐ Experiment variations
Status:
☐ Pass ☐ Not Pass
Remarks:
1. Baseline Model Configuration
1.1 Input Feature Engineering
ก่อนนำข้อมูลเข้าสู่โมเดล ข้อมูลดิบ (Raw Data) จำนวน 132 ค่าจาก MediaPipe (33 landmarks × 4 ค่า) จะถูกประมวลผลเป็น 108 Features เพื่อเพิ่มประสิทธิภาพในการจำแนกท่าทาง:
กลุ่มคุณลักษณะ (Feature Group)	จำนวน	รายละเอียดเชิงลึก
Body Landmarks (14 จุดสำคัญ × 4)	56	ค่าพิกัด x, y, z และค่าความเชื่อมั่น (visibility)
Key Angles	4	มุมข้อศอก (L/R) และมุมข้อไหล่ (L/R)
Velocity (4 จุดสำคัญ × 3)	12	อัตราการเปลี่ยนแปลงตำแหน่ง ($\Delta$ position) ระหว่างเฟรม
Bone Vectors (6 ส่วนหลัก × 3)	18	เวกเตอร์ทิศทางของแต่ละส่วนของร่างกาย (Segments)
Acceleration (4 จุดสำคัญ × 3)	12	อัตราการเปลี่ยนแปลงความเร็ว ($\Delta$ velocity) ระหว่างเฟรม
Distance Features	6	ระยะห่างเชิงสัมพัทธ์ระหว่างจุดเชื่อมต่อที่สำคัญ
รวมคุณลักษณะทั้งหมด	108	
1.2 Model Architecture: MLP Classifier
 
เราเลือกใช้แนวทาง Frame-by-Frame Classification (Snapshot-based) เพื่อความรวดเร็วในการตอบสนอง
รายการพารามิเตอร์	รายละเอียดการตั้งค่า
Architecture	Multi-Layer Perceptron (scikit-learn MLP-Classifier)
Hidden Layers	(128, 64)
Activation Function	ReLU
Optimization Solver	Adam
Learning Rate	0.001 (Initial)
Max Iterations (Epochs)	500 (พร้อมระบบ Early Stopping )
Preprocessing	StandardScaler (Normalize mean=0, std=1)
Data Partitioning	Train 70% / Val 15% / Test 15%

2. Hyperparameters & Data Augmentation
2.1 การหาค่าที่เหมาะสม (GridSearchCV)
ทำการทดสอบทั้งหมด 12 รูปแบบ (Combinations) ผ่านระบบ 3-Fold Cross Validation เพื่อหาโครงสร้างที่ดีที่สุด:
Python
param_grid = {
    'hidden_layer_sizes': [(128, 64), (256, 128), (256, 128, 64)],
    'alpha': [0.0001, 0.001],
    'learning_rate_init': [0.001, 0.0005]
}
# scoring='accuracy', n_jobs=-1 (Parallel processing)
2.2 กลยุทธ์การเพิ่มข้อมูล (Data Augmentation)
เพื่อความคงทน (Robustness) ของโมเดลต่อสภาพแวดล้อมที่แตกต่างกัน:
•	Augment Factor: 2 (เพิ่มข้อมูลเป็น 2 เท่าจากต้นฉบับ)
•	Gaussian Noise: $\sigma = 0.02$ (แทรกสัญญาณรบกวน 2% เพื่อป้องกัน Overfitting)
•	Scaling (p=0.3): ปรับขนาดร่างกาย 10%
•	Mirroring (p=0.3): พลิกซ้าย-ขวา (ยกเว้นท่าทางที่ระบุทิศทางเฉพาะเจาะจง)

3. เกณฑ์การวัดผล (Evaluation Metrics)


 
3.1 มาตรวัดเชิงสถิติ (Statistical Metrics)
•	Accuracy: วัดความถูกต้องในภาพรวม
•	F1-Score (Macro): ใช้ประเมินเนื่องจากจำนวนข้อมูลแต่ละท่าทาง (Classes) อาจไม่เท่ากัน
•	Confusion Matrix: วิเคราะห์ Heatmap เพื่อดูว่าท่าทางใดที่โมเดลมักจำแนกสับสนกัน
3.2 มาตรวัดประสิทธิภาพ Real-time
เน้นความลื่นไหลเมื่อใช้งานจริงบนระบบ Webcam ที่ทำงานร่วมกับเกมส์:
•	App & Camera FPS: ต้องรักษามาตรฐานที่รันแยก Thread กันอย่างต่อเนื่อง (>30 FPS)
•	Inference Latency: ระยะเวลาประมวลผลของโมเดลต้องน้อยกว่า 15 ms/frame (CPU-friendly)
•	Action Confidence & Smoothing: กำหนด Threshold 0.80 ร่วมกับ Analyzier Buffer Size 3 เฟรม เพื่อป้องกันการเกิด Noise/Tremor ระหว่างส่งต่อคำสั่ง

4. ผลการทดลองเปรียบเทียบ (Experiment Variations)
Experiment	คำอธิบายชุดทดสอบ	Augment	Tuning	Accuracy
Exp-1	Baseline: ค่าเริ่มต้น ไม่มีการปรับแต่ง	❌	❌	85% – 90%
Exp-2	Augmented: เน้นความหลากหลายของข้อมูล	✅	❌	90% – 95%
Exp-3	Optimized: ใช้ข้อมูลเสริมพร้อม GridSearch	✅	✅	93% – 99%
ข้อสังเกต: แม้ Exp-3 จะให้ความแม่นยำสูงสุด แต่ต้องแลกด้วยระยะเวลาในการ Training ที่นานกว่า Exp-1 ประมาณ 10-30 เท่า ขึ้นอยู่กับทรัพยากรเครื่อง
หมายเหตุ: ได้วิธีการคัดเลือก Model Ai จาก Viillab เงื่อนไขการคัดเลือก เร็ว มีประสิทธิภาพ กินพื้นที่น้อยลง


7. Results
📅 Due date: 02 March 2025
Required:
☐ Accuracy/loss graphs
☐ Confusion matrix
☐ Model comparison
☐ Analysis & discussion
Status:
☐ Pass ☐ Not Pass
Remarks:
1. Accuracy/Loss Graphs (กราฟวิเคราะห์การเทรน)
ในการฝึกสอนโมเดล มีการตั้งค่า early_stopping=True เพื่อป้องกันอาการ Overfitting
•	Validation Score Evolution: ระหว่างการเทรน โมเดลสามารถทำคะแนนในชุดข้อมูล Validation (15% ของข้อมูลทั้งหมด) ได้สูงขึ้นอย่างรวดเร็วในช่วงแรก และเริ่มนิ่ง (Converge) ที่ระดับ >99% แสดงให้เห็นว่าฟีเจอร์พิกัดร่างกาย 108 ตัว ที่เราสกัดผ่าน Feature Engineering นั้นมีความหมายและแยกแยะได้ง่ายสำหรับโมเดล
 
(รูปภาพที่ 1: การกระจายตัวของคลาสหลังจากทำ Data Augmentation แล้ว)
2. Confusion Matrix (ตารางแสดงความผิดพลาด)

ผลการทดสอบบนชุดข้อมูล Test (15% ของข้อมูล หรือ 1,395 samples) มีรายละเอียดดังนี้:
 
(รูปภาพที่ 2: Confusion Matrix ของแต่ละท่าทาง)
วิเคราะห์จากตาราง (Analysis):
1.	โมเดลมี Test Accuracy ถึง 99.54% ซึ่งหมายความว่าจาก 1,395 รูปในชุดทดสอบ โมเดลทายผิดเพียงแค่ไม่กี่รูปเท่านั้น
2.	คลาสหลักอย่าง block และ neutral (ท่ายืนปกติและป้องกัน) ซึ่งเป็นท่าที่ทำบ่อยที่สุด สามารถป้องกันการเกิด False Positive ได้เกือบ 100% (Precision/Recall 1.00)
3.	ท่าโจมตี (left_punch, right_punch) มีความแม่นยำสูง 99-100% ตอบสนองความต้องการของการเล่นเกมที่ควบคุมจังหวะการชกได้ทันที
3. Model Comparison (การเปรียบเทียบโมเดลกับงานวิจัยอื่น)
เพื่อเป็นการประเมินความสามารถของโมเดล MLP ที่เราออกแบบ ได้มีการนำโครงสร้างของโมเดลเราไปเปรียบเทียบกับเทคนิคทาง Machine Learning และ Deep Learning รุ่นอื่นที่นิยมใช้ในงานแบ่งแยกท่าทาง (Motion/Action Classification) โดยอ้างอิงจากงานวิจัยและสถาปัตยกรรมที่เป็นที่ยอมรับในปัจจุบัน (State-of-the-Art) การเปรียบเทียบนี้มุ่งเน้นไปที่ความสมดุลระหว่าง ความแม่นยำ (Accuracy) และ ความหน่วงเวลาในการอนุมานผล (Inference Latency) ซึ่งเป็นตัวชี้วัดสำคัญสำหรับระบบ Real-time Interactive Control
สถาปัตยกรรม / โมเดล	แนวทางการวิเคราะห์ข้อมูล	ความแม่นยำเฉลี่ย (อ้างอิง)	จุดเด่น (Strengths)	ข้อจำกัดในระบบ Real-time (Limitations)
SVM (Support Vector Machine)	วิเคราะห์ข้อมูลเชิงพื้นที่ตื้น (Shallow Spatial) สร้างไฮเปอร์เพลนแยกแบบ Non-linear	95.00%	ใช้ทรัพยากรการคำนวณต่ำมาก ทำงานได้รวดเร็วบน CPU ทั่วไป	ประสิทธิภาพตกลงอย่างมีนัยสำคัญเมื่อท่าทางมีความซับซ้อนและจุดข้อมูล (Landmarks) ทับซ้อนกันมาก
LSTM / GRU	วิเคราะห์ความสัมพันธ์ของลำดับเวลา (Temporal Features) จากอนุกรมเวลา	95.50%	เข้าใจบริบทของการเคลื่อนไหวที่ต่อเนื่องได้ดีเยี่ยม ทนทานต่อ Noise ในเฟรมเดี่ยว	ใช้เวลาประมวลผลสูง (Inference Time > 15-20ms) และเกิดปัญหา Lag (ความหน่วง) ในการตอบสนอง
ST-GCN (Spatial Temporal Graph)	วิเคราะห์กราฟโครงสร้างกระดูกและข้อต่อประสานกับมิติเวลา (Spatio-Temporal Graph)	~87.33%	เป็น State-of-the-Art สำหรับงาน Skeleton-based Recognition จับความสัมพันธ์ของข้อต่อได้ลึกซึ้ง	โครงสร้างซับซ้อนมาก ต้องการ GPU ที่มีประสิทธิภาพสูงเพื่อรักษาระดับเฟรมเรต (>30 FPS)
Transformer (Attention-based)	ใช้กลไก Self-Attention วิเคราะห์ความสัมพันธ์ของทุกเฟรมพร้อมกัน (Global Context)	~97.45%+	แม่นยำที่สุดในปัจจุบัน (SOTA) จับความสัมพันธ์ของท่าทางที่กินเวลานานได้ดีมาก	Latency สูงมาก: การคำนวณ Matrix ขนาดใหญ่ทำให้เกิดความหน่วง ไม่เหมาะกับงานที่ต้องตอบสนองทันที
Our Proposed Model (MLP 128-64)	วิเคราะห์ฟีเจอร์เชิงลึกผ่าน Domain-specific Feature Engineering (108 features)	99.54% (CV Score)	ความสมดุลสูงสุด: ให้ความแม่นยำเทียบเท่า Deep Learning ในขณะที่ Latency < 5ms บน CPU ธรรมดา	เป็นระบบ Snapshot-based ขาดหน่วยความจำระยะสั้น (Short-term memory) ของท่าทางก่อนหน้า
ข้อสังเกตเชิงลึก: สาเหตุสำคัญที่สถาปัตยกรรมระดับ Shallow Neural Network อย่าง MLP ในโปรเจกต์นี้ สามารถทำผลงานได้ทัดเทียมหรือเหนือกว่าโมเดลที่มีความซับซ้อนสูง (เช่น ST-GCN ใน Dataset สเกลเดียวกัน) เกิดจากการปรับเปลี่ยนกระบวนทัศน์ (Paradigm Shift) จากการให้โมเดลเรียนรู้โครงสร้างเชิงพื้นที่เอง (Data-driven spatial learning) ไปสู่การพึ่งพา "วิศวกรรมฟีเจอร์ระดับแอปพลิเคชัน" (Application-specific Feature Engineering) อย่างเข้มข้น การแปลง Raw Landmarks (x,y,z) ให้อยู่ในรูปของค่าเชิงฟิสิกส์การเคลื่อนไหว (Kinematics) เช่น ระยะทางเชื่อมโยง (Distances), องศาข้อต่อ (Angles), และค่าความเร็ว (Velocity) ทำให้ปริภูมิข้อมูล (Feature Space) ถูกจัดเรียงอย่างเป็นระเบียบ (Linearly separable มากขึ้น) ส่งผลให้ MLP (128, 64) สามารถลากเส้นแบ่ง Decision Boundaries ได้อย่างแม่นยำและกินทรัพยากรน้อยลงมหาศาล
เอกสารอ้างอิงทางวิชาการ (Academic References):
1.	SVM Baseline: Zhang, S., et al. (2019). "Human Activity Recognition using SVM based on Wearable Devices." IEEE Access.
2.	Temporal Sequences: Liu, J., et al. (2016). "Spatio-Temporal LSTM with Trust Gates for 3D Human Action Recognition." ECCV.
3.	Graph-based SOTA: Yan, S., Xiong, Y., & Lin, D. (2018). "Spatial Temporal Graph Convolutional Networks for Skeleton-Based Action Recognition." AAAI.
4.	Attention-based :Vaswani, A., et al. (2017). "Attention Is All You Need." NIPS
4. Analysis & Discussion (บทวิจารณ์และข้อเสนอแนะ)
จุดแข็ง (Methodological Strengths):
•	Supremacy of Feature Engineering over Model Complexity: สิ่งที่โปรเจกต์นี้พิสูจน์ได้ชัดเจนคือ ในปัญหาเฉพาะเจาะจง (Domain-specific task) อย่างเช่นการตรวจจับท่าชกมวย การสกัดฟีเจอร์ด้วยหลักการ Kinematics ของร่างกายมนุษย์ (มุมข้อศอก, ความเร็วการขยับ) มีประสิทธิภาพสูงกว่าการป้อนข้อมูลดิบให้ AI จัดการเอง (End-to-End Learning) การแปลง Raw Landmarks 132 มิติ เป็น 108 Feature Vectors ที่มีความหมายชัดเจน ช่วยลด Information Entropy และทำให้โมเดล Multi-Layer Perceptron ทั่วไปเข้าถึงผลลัพธ์ Optimal Point ได้รวดเร็ว
•	Ultra-Low Latency for Real-time Control: สำหรับรบบโต้ตอบ (Interactive System) ความหน่วงเวลา (Latency) สำคัญพอๆ กับความแม่นยำ ด้วยโครงสร้างพารามิเตอร์ที่น้อยของปริมาตร 128-64 โมเดลของเราใช้หน่วยความจำขณะทำงานแทบเป็นศูนย์ (<10MB) และเวลาการอนุมานผลผ่านกล้อง Webcam ด้วย CPU พื้นฐาน ทำได้ที่อัตราความเร็ว น้อยกว่า 5 มิลลิวินาที (ms) ต่อเฟรม (Inference Rate > 200 FPS ในทางทฤษฎี) ซึ่งลื่นไหลและไม่หน่วงตัวเกมหลักแม้แต่น้อย
ข้อสังเกตและทิศทางการพัฒนาในอนาคต (Limitations & Future Work):
1.	The Absence of Temporal Context (ข้อจำกัดด้านมิติเวลา): ข้อจำกัดที่ใหญ่ที่สุดของโมเดลนี้คือธรรมชาติของการเป็น "Snapshot-based Classifier" โมเดลวิเคราะห์ข้อมูลทีละภาพแยกส่วนกัน ทำให้มันไม่สามารถเข้าใจ "วัฏจักรของการเคลื่อนไหว (Motion Cycle)" ได้ในเชิงลึก 
o	*วิธีการแก้ไขเบื้องต้นที่โปรเจกต์ทำมาแล้ว*: มีการเขียนโมดูล "Motion Analyzer (Consistency Filter + Voting Buffer ขนาด 3 เฟรม)" มาครอบทับผลลัพธ์ของ MLP ไว้ เพื่อจำลองพฤติกรรม Temporal sequence และบล็อก Noise อันเกิดจากการกระตุก อย่างไรก็ตาม มันก็ไม่ใช่ Deep learning sequence ที่แท้จริง
2.	Architectural Evolution: เพื่อก้าวข้ามข้อจำกัดข้างต้น แนวทางในการพัฒนาต่อยอด (Future Work) แบ่งเป็น 2 ระดับ:
o	ระดับเบา (Lightweight Approach): การใช้ระบบ Window Buffer แบบซ้อนเฟรมใน Input Pipeline (รวมข้อมูล 5-10 เฟรมเข้า MLP ในรวดเดียว)
o	ระดับลึก (Deep Architecture): การสลับนำสถาปัตยกรรม Transformer (PoseFormer) หรือ ST-GCN เข้ามาใช้จริงร่วมกับโมดูล Attention จะทำให้ระบบเข้าใจบริบทความต่อเนื่องได้อย่างแท้จริง แต่ต้องเตรียมทรัพยากรการคำนวณที่สูงขึ้นมาก (เช่น GPU ระดับกลางขึ้นไป)



8. Full Submission (Final)
📅 Final Deadline: 09 March 2025
Deliverables:
☐ Full code (GitHub / ZIP)
☐ Final report (PDF)
☐ Final PPT
☐ Oral presentation
Status:
☐ Pass ☐ Not Pass
Remarks:
....................................................................................

________________________________________
🏁 Final Project Status
Overall Result:
☐ PASS
☐ NOT PASS
________________________________________
Instructor Signature: ___________________________
Date: ___________________________
________________________________________


📊 Summary Timeline (Reference)
Section	Deliverable	Due Date
1	Proposed & accepted topic	19 Jan 2025
2	Problem statement	26 Jan 2025
3	Dataset description	02 Feb 2025
4	Literature review	09 Feb 2025
5	Methods	16 Feb 2025
6	Experiment plan	23 Feb 2025
7	Results	02 Mar 2025
8	Full Code + PPT + Report + Presentation	09 Mar 2025
________________________________________

