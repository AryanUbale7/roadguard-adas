🚗 RoadGuard – AI Powered ADAS System

An AI-based Advanced Driver Assistance System (ADAS) that performs real-time detection of pedestrians, vehicles, and road hazards using Computer Vision and Deep Learning.
The system intelligently triggers voice alerts only for real danger scenarios and automatically stores evidence screenshots and structured logs.

📌 Key Features

👁️ Real-time Detection

Pedestrians

Cars, bikes, buses, trucks

Road hazards: potholes, debris, speed breakers

🧠 Context-Aware Intelligence

Front-zone danger filtering

Distance-based risk estimation (Near / Medium / Far)

No alerts when vehicle is stationary (false alert prevention)

🔊 Voice Alerts

Automatic voice warning for real danger only

Alerts play alongside live video (no external audio window)

📸 Evidence Collection

Automatic screenshot capture during high-risk events

JSON-based structured logging for every alert

🧪 Demo-Ready

Works on recorded dashcam / road videos

Can be extended to real-time camera feed or embedded systems

🛠️ Tech Stack

Programming Language: Python

Computer Vision: OpenCV

Deep Learning: YOLOv8 (Ultralytics)

Audio Alerts: Windows winsound

Model Training: Custom YOLOv8 training

Logging: JSON-based event logs

🧠 Model Training Details

Base Model: YOLOv8

Training Type: Custom object detection

Hazard Classes Trained:

Pothole

Debris

Speed Breaker

Training Configuration:

Epochs: 50

Image Size: 640 × 640

Dataset: Custom + Roboflow datasets

Training Command:

yolo detect train model=yolov8n.pt data=road.yaml epochs=50 imgsz=640


Training Outcome:

Model successfully detects hazards in real-world road videos

Integrated with COCO-pretrained YOLOv8 for vehicles and pedestrians

📁 Project Structure
ai-model/
│
├── detect_adas.py          # Main ADAS detection script
├── road.mp4                # Sample input video
│
├── assets/                 # Voice alert audio files
│   ├── person.wav
│   ├── vehicle.wav
│   └── hazard.wav
│
├── runs/
│   └── detect/train3/weights/best.pt   # Trained YOLOv8 hazard model
│
├── outputs/
│   ├── screenshots/        # Evidence images
│   └── alerts.json         # Alert logs
│
└── README.md

▶️ How to Run the Project
1️⃣ Clone the Repository
git clone https://github.com/<your-username>/roadguard-adas.git
cd roadguard-adas/ai-model

2️⃣ Create & Activate Virtual Environment
python -m venv venv
venv\Scripts\activate

3️⃣ Install Dependencies
pip install ultralytics opencv-python

4️⃣ Run ADAS System
python detect_adas.py

📤 Output Generated
📸 Evidence Screenshots

Saved automatically when a real danger is detected:

outputs/screenshots/

📄 JSON Alert Logs

Structured alert data:

{
  "time": "2025-01-15_12-30-45",
  "type": "hazard",
  "confidence": 0.87,
  "distance": "NEAR",
  "speed": 30,
  "image": "hazard_20250115.jpg"
}

🎯 Real-World Use Cases

Smart Dashcam Systems

Driver Assistance & Safety Applications

Road Condition Monitoring

Autonomous & Semi-Autonomous Vehicles

AI-based Traffic Safety Research

🚀 Future Improvements

GPS / OBD-based real vehicle speed integration

Lane detection and lane-based risk filtering

Jetson / Raspberry Pi deployment

Web dashboard for live monitoring

Android Auto / in-car display integration

👨‍💻 Author

Aryan Ubale
AI & Computer Vision Enthusiast
📍 India

Feel free to connect and share feedback on LinkedIn 🚀

⭐ Acknowledgements

Ultralytics YOLOv8

OpenCV Community

Open-source Computer Vision datasets

🏁 Final Note

This project focuses on practical AI deployment, not just model training.
Every alert is context-aware, evidence-backed, and demo-ready.
