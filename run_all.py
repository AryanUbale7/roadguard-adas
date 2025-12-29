import subprocess
import time
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_script(script_name):
    script_path = os.path.join(BASE_DIR, script_name)
    print(f"\n▶️ Running {script_name} ...\n")
    subprocess.run([sys.executable, script_path])

# ================== STEP 1: RUN DETECTION ==================
run_script("detect_pothole.py")

# ================== STEP 2: WAIT FOR JSON ==================
json_path = os.path.join(BASE_DIR, "outputs", "detections.json")

print("\n⏳ Waiting for detections.json...\n")

timeout = 30  # seconds
elapsed = 0

while not os.path.exists(json_path):
    time.sleep(1)
    elapsed += 1
    if elapsed > timeout:
        print("❌ detections.json not found. Detection failed.")
        sys.exit(1)

print("✅ detections.json found")

# ================== STEP 3: RUN ALERT SYSTEM ==================
run_script("check_alerts.py")

print("\n🏁 FULL PIPELINE EXECUTED SUCCESSFULLY")
