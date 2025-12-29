<div align="center">

# 🚗 RoadGuard – AI Powered ADAS  
### Real-Time Road Hazard & Object Detection using Computer Vision

An end-to-end **Advanced Driver Assistance System (ADAS)** that intelligently detects  
**vehicles, pedestrians, and road hazards** and triggers **context-aware voice alerts**  
with automatic **evidence logging**.

</div>

---

## ✨ Highlights

- 🔍 **Real-Time Detection**
  - Pedestrians
  - Cars, Bikes, Buses, Trucks
  - Potholes, Debris, Speed Breakers

- 🧠 **Smart Decision Logic**
  - Front-zone danger filtering
  - Distance-based risk estimation
  - No alerts when vehicle is stationary (false-alert prevention)

- 🔊 **Voice Alerts**
  - Triggered only for real danger
  - Plays alongside live video feed

- 📸 **Evidence Collection**
  - Automatic screenshot capture
  - Structured JSON alert logs

- 🧪 **Demo-Ready & Extendable**
  - Works on recorded road / dashcam videos
  - Easily extendable to real-time camera feeds

---

## 🛠️ Tech Stack

| Category | Technology |
|--------|-----------|
| Language | Python |
| Computer Vision | OpenCV |
| Deep Learning | YOLOv8 (Ultralytics) |
| Audio Alerts | `winsound` |
| Logging | JSON |
| Training | Custom YOLOv8 Training |

---

## 🧠 Model Training Overview

- **Base Model:** YOLOv8 (Ultralytics)
- **Training Type:** Custom Object Detection
- **Hazard Classes Trained:**
  - Pothole
  - Debris
  - Speed Breaker

### Training Configuration
```bash
yolo detect train model=yolov8n.pt data=road.yaml epochs=50 imgsz=640
Epochs: 50

Image Size: 640 × 640

Datasets: Custom datasets + Roboflow

Result:
Reliable hazard detection in real-world road videos, integrated with
COCO-pretrained YOLOv8 for vehicles & pedestrians.

📁 Project Structure
text
Copy code
ai-model/
│
├── detect_adas.py              # Main ADAS detection script
├── road.mp4                    # Sample input video
│
├── assets/                     # Voice alert audio files
│   ├── person.wav
│   ├── vehicle.wav
│   └── hazard.wav
│
├── runs/
│   └── detect/train3/weights/
│       └── best.pt             # Trained YOLOv8 hazard model
│
├── outputs/
│   ├── screenshots/            # Evidence images
│   └── alerts.json             # Structured alert logs
│
└── README.md
▶️ How to Run
1️⃣ Clone Repository
bash
Copy code
git clone https://github.com/<your-username>/roadguard-adas.git
cd roadguard-adas/ai-model
2️⃣ Create & Activate Virtual Environment
bash
Copy code
python -m venv venv
venv\Scripts\activate
3️⃣ Install Dependencies
bash
Copy code
pip install ultralytics opencv-python
4️⃣ Run ADAS System
bash
Copy code
python detect_adas.py
📤 Output Samples
📸 Evidence Screenshots
Saved automatically during high-risk detections:

bash
Copy code
outputs/screenshots/
📄 JSON Alert Logs
json
Copy code
{
  "time": "2025-01-15_12-30-45",
  "type": "hazard",
  "confidence": 0.87,
  "distance": "NEAR",
  "speed": 30,
  "image": "hazard_20250115.jpg"
}
🎯 Use Cases
🚘 Smart Dashcam Systems

🛣️ Road Safety Monitoring

🤖 Autonomous / Semi-Autonomous Vehicles

📊 AI-Driven Traffic Analysis

🔬 Computer Vision Research Projects

🚀 Future Enhancements
GPS / OBD-based real vehicle speed integration

Lane detection & lane-aware danger zones

NVIDIA Jetson / Raspberry Pi deployment

Web dashboard for live monitoring

In-car display / Android Auto integration

👨‍💻 Author
Aryan Ubale
AI & Computer Vision Enthusiast
📍 India

🔗 Open to feedback, collaboration & opportunities

⭐ Acknowledgements
Ultralytics – YOLOv8

OpenCV Community

Open-source Computer Vision Datasets

Note:
This project focuses on practical AI deployment, not just model training.
Every alert is context-aware, evidence-backed, and demo-ready.
