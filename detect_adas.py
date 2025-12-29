from ultralytics import YOLO
import cv2, os, time, json, winsound
from datetime import datetime

# ================= PATHS =================
BASE = os.path.dirname(os.path.abspath(__file__))

VIDEO = os.path.join(BASE, "road.mp4")
HAZARD_MODEL = os.path.join(BASE, "runs/detect/train3/weights/best.pt")
COCO_MODEL = "yolov8n.pt"

VOICE = {
    "person": os.path.join(BASE, "assets/person.wav"),
    "vehicle": os.path.join(BASE, "assets/vehicle.wav"),
    "hazard": os.path.join(BASE, "assets/hazard.wav")
}

OUT = os.path.join(BASE, "outputs")
SHOT = os.path.join(OUT, "screenshots")
LOG = os.path.join(OUT, "alerts.json")

os.makedirs(SHOT, exist_ok=True)
os.makedirs(OUT, exist_ok=True)

# ================= LOAD MODELS =================
hazard_model = YOLO(HAZARD_MODEL)
coco_model = YOLO(COCO_MODEL)

# ================= SETTINGS =================
CONF_COCO = 0.45
CONF_HAZARD = 0.35

# 🔴 DEMO SPEED (LinkedIn demo ke liye)
VEHICLE_SPEED = 30        # km/h
STATIONARY_SPEED = 5

print("🚗 ROADGUARD ADAS (IMAGE SAVE FIXED) STARTED")

# ================= HELPERS =================
def play_voice(kind):
    if kind in VOICE and os.path.exists(VOICE[kind]):
        winsound.PlaySound(
            VOICE[kind],
            winsound.SND_FILENAME | winsound.SND_ASYNC
        )

def is_front(cx, by, w, h):
    return (w * 0.35 < cx < w * 0.65) and (by > h * 0.6)

def estimate_distance(area, frame_area):
    ratio = area / frame_area
    if ratio > 0.08:
        return "NEAR"
    elif ratio > 0.04:
        return "MEDIUM"
    return "FAR"

# ================= GUARANTEED SAVE =================
def save_evidence(kind, conf, dist, frame):
    if frame is None or frame.size == 0:
        print("❌ Frame empty – skipping save")
        return

    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    img_name = f"{kind}_{ts}.jpg"
    img_path = os.path.join(SHOT, img_name)

    ok = cv2.imwrite(img_path, frame)

    if not ok:
        print("❌ cv2.imwrite FAILED:", img_path)
        return
    else:
        print("✅ IMAGE SAVED:", img_path)

    entry = {
        "time": ts,
        "type": kind,
        "confidence": round(float(conf), 2),
        "distance": dist,
        "speed": VEHICLE_SPEED,
        "image": img_name
    }

    data = []
    if os.path.exists(LOG):
        try:
            with open(LOG, "r") as f:
                data = json.load(f)
        except:
            data = []

    data.append(entry)

    with open(LOG, "w") as f:
        json.dump(data, f, indent=2)

    print("📄 JSON UPDATED")

# ================= VIDEO =================
cap = cv2.VideoCapture(VIDEO)
if not cap.isOpened():
    print("❌ Video not opened")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    danger = None
    danger_conf = 0
    danger_dist = ""

    # ================= COCO (PERSON / VEHICLE) =================
    coco_res = coco_model(frame, conf=CONF_COCO, verbose=False)
    for r in coco_res:
        for box in r.boxes:
            label = coco_model.names[int(box.cls[0])]
            if label not in ["person", "car", "motorcycle", "bus", "truck"]:
                continue

            kind = "person" if label == "person" else "vehicle"
            conf = float(box.conf[0])

            x1,y1,x2,y2 = map(int, box.xyxy[0])
            cx, by = (x1+x2)//2, y2
            area = (x2-x1)*(y2-y1)

            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.putText(frame,label,(x1,y1-6),
                        cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0),2)

            if is_front(cx, by, w, h):
                dist = estimate_distance(area, h*w)
                if VEHICLE_SPEED > STATIONARY_SPEED and dist == "NEAR":
                    danger = kind
                    danger_conf = conf
                    danger_dist = dist

    # ================= HAZARDS =================
    haz_res = hazard_model(frame, conf=CONF_HAZARD, verbose=False)
    for r in haz_res:
        for box in r.boxes:
            label = hazard_model.names[int(box.cls[0])]
            if label not in ["pothole", "debris", "speed breaker", "speed-breaker"]:
                continue

            conf = float(box.conf[0])
            x1,y1,x2,y2 = map(int, box.xyxy[0])
            cx, by = (x1+x2)//2, y2
            area = (x2-x1)*(y2-y1)

            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),2)
            cv2.putText(frame,label,(x1,y1-6),
                        cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)

            if is_front(cx, by, w, h):
                dist = estimate_distance(area, h*w)
                if VEHICLE_SPEED > STATIONARY_SPEED and dist == "NEAR":
                    danger = "hazard"
                    danger_conf = conf
                    danger_dist = dist

    # ================= FORCE SAVE (DEBUG MODE) =================
    print("DEBUG:", danger, danger_dist, VEHICLE_SPEED)

    if danger:
        play_voice(danger)
        save_evidence(danger, danger_conf, danger_dist, frame)

        cv2.rectangle(frame,(0,0),(w,80),(0,0,255),-1)
        cv2.putText(frame,
                    f"⚠ WARNING: {danger.upper()} AHEAD",
                    (20,50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2,(255,255,255),3)

    cv2.imshow("RoadGuard | ADAS (IMAGE SAVE FIXED)", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

print("✅ ADAS RUN COMPLETE")
