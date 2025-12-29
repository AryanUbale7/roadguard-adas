import pyttsx3
import os

os.makedirs("assets", exist_ok=True)

engine = pyttsx3.init()

# Try to select female voice
voices = engine.getProperty("voices")
for v in voices:
    if "female" in v.name.lower() or "zira" in v.name.lower():
        engine.setProperty("voice", v.id)
        break

engine.setProperty("rate", 150)

engine.save_to_file(
    "सावधान! आगे सड़क पर खतरा है",
    "assets/warning.wav"
)

engine.runAndWait()
print("✅ Hindi female WAV generated")
