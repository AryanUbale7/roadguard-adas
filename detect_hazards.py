from ultralytics import YOLO
import cv2
import os
import time
import json
from datetime import datetime

# ================= CONFIG =================
MODEL_PATH = "runs/detect/train3/weights/best.pt"
VIDEO_SOURCE = "road.mp4"   # webcam ke liye 0
CONF_THRES = 0.25                # pothole/speedbreaker ke liye thoda low
ALERT_COOLDOWN = 3               # seconds
VOICE_FILE = "assets/warning.wav"

EVIDENCE_IMG_DIR = "evidence/images"
LOG_FILE = "evidence/detections.json"
# =========================================

# Create folders
os.makedirs(EVIDENCE_IMG_DIR, exist_ok=True)
os.makedirs("evidence", exist_ok=True)

# Init JSON log if not exists
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        json.dump([], f)

# Load model
model = YOLO(MODEL_PATH)

# Video source
cap = cv2.VideoCapture(VIDEO_SOURCE)

# Alert timing tracker
last_alert_time = {}

def play_voice():
    """Safe voice play (no crash if missing)"""
    if os.path.exists(VOICE_FILE):
        try:
            os.startfile(VOICE_FILE)
        except Exception as e:
            print(f"🔇 Voice error: {e}")
    else:
        print("🔇 Voice file not found, skipping sound")

print("🚗 RoadGuard | Hazard Detection Started")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO inference
    results = model(frame, conf=CONF_THRES)
    annotated = results[0].plot()

    if results[0].boxes is not None:
        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            cls_name = model.names[cls_id]

            current_time = time.time()
            last_time = last_alert_time.get(cls_name, 0)

            # Cooldown check
            if current_time - last_time >= ALERT_COOLDOWN:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                print(f"⚠️ ALERT: {cls_name.upper()} detected (conf {conf:.2f})")

                # ---------- SAVE SCREENSHOT ----------
                img_name = f"{cls_name}_{timestamp}.jpg"
                img_path = os.path.join(EVIDENCE_IMG_DIR, img_name)
                cv2.imwrite(img_path, annotated)

                # ---------- SAVE JSON LOG ----------
                log_entry = {
                    "time": timestamp,
                    "hazard": cls_name,
                    "confidence": round(conf, 2),
                    "image": img_name
                }

                with open(LOG_FILE, "r+") as f:
                    data = json.load(f)
                    data.append(log_entry)
                    f.seek(0)
                    json.dump(data, f, indent=2)

                # ---------- VOICE ALERT ----------
                play_voice()

                last_alert_time[cls_name] = current_time

    # Show output
    cv2.imshow("RoadGuard | Hazard Detection", annotated)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

print("✅ Detection finished. Evidence saved in /evidence")
