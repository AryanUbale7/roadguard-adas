import json
import math
import time
import os
import cv2
import numpy as np
import pygame

# ================== AUDIO INIT (BACKGROUND VOICE) ==================
pygame.mixer.init()

def play_voice():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    audio_path = os.path.join(base_dir, "assets", "warning.wav")

    if not os.path.exists(audio_path):
        print("❌ Audio file not found:", audio_path)
        return

    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()

# ================== HAVERSINE DISTANCE ==================
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(dlambda / 2) ** 2

    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# ================== LOAD DETECTIONS ==================
json_path = os.path.join("outputs", "detections.json")

if not os.path.exists(json_path):
    print("❌ detections.json not found")
    exit()

with open(json_path, "r") as f:
    detections = json.load(f)

if not detections:
    print("❌ No potholes in detections")
    exit()

# ================== DEMO SETTINGS ==================
current_lat = 19.0750
current_lng = 72.8750

ALERT_DISTANCE = 500   # demo ke liye bada rakha hai
alerted_locations = set()

# ================== OPENCV WINDOW ==================
cv2.namedWindow("RoadGuard Alert", cv2.WINDOW_NORMAL)

print("🚗 Vehicle started...\n")
time.sleep(1)

# ================== MAIN LOOP ==================
for d in detections:
    lat = round(d["lat"], 6)
    lng = round(d["lng"], 6)
    severity = d.get("severity", "N/A")

    key = (lat, lng)
    distance = round(haversine(current_lat, current_lng, lat, lng), 2)

    frame = np.zeros((480, 800, 3), dtype=np.uint8)

    if distance <= ALERT_DISTANCE and key not in alerted_locations:
        print(f"⚠️ ALERT: Pothole ahead in {distance} meters")

        # 🔊 BACKGROUND VOICE (NO WINDOW)
        play_voice()

        # 🔴 VISUAL ALERT (FLASH)
        for _ in range(6):
            frame[:] = (0, 0, 0)

            cv2.putText(
                frame,
                "POTHOLE AHEAD!",
                (120, 200),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (0, 0, 255),
                5
            )

            cv2.putText(
                frame,
                f"Distance: {distance} m | Severity: {severity}",
                (90, 270),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                3
            )

            cv2.imshow("RoadGuard Alert", frame)
            cv2.waitKey(300)

        alerted_locations.add(key)

    else:
        cv2.putText(
            frame,
            "Driving...",
            (300, 240),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0, 255, 0),
            3
        )

        cv2.imshow("RoadGuard Alert", frame)
        cv2.waitKey(300)

    # 🚗 simulate movement (demo fast)
    current_lat += 0.0005
    current_lng += 0.0005

cv2.destroyAllWindows()
print("✅ ALERT + VOICE + VISUAL COMPLETE")
