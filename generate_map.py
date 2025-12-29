import json
import folium
import os

# ================== FILE PATHS ==================
json_file = "outputs/detections.json"
map_file = "outputs/potholes_map.html"

if not os.path.exists(json_file):
    print("❌ detections.json nahi mila")
    exit()

# ================== LOAD DATA ==================
with open(json_file, "r") as f:
    detections = json.load(f)

if len(detections) == 0:
    print("❌ JSON empty hai, map nahi ban sakta")
    exit()

# ================== MAP CENTER ==================
center_lat = detections[0]["lat"]
center_lng = detections[0]["lng"]

m = folium.Map(location=[center_lat, center_lng], zoom_start=15)

# ================== ADD MARKERS ==================
for d in detections:
    popup_text = (
        f"Type: {d['type']}<br>"
        f"Confidence: {d['confidence']}<br>"
        f"Time (sec): {d['video_time_sec']}"
    )

    folium.Marker(
        location=[d["lat"], d["lng"]],
        popup=popup_text,
        icon=folium.Icon(color="red", icon="warning-sign")
    ).add_to(m)

# ================== SAVE MAP ==================
m.save(map_file)

print("✅ STEP 4 COMPLETE – MAP GENERATED")
print(f"🗺️ Open this file in browser: {map_file}")
