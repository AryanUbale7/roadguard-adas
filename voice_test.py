import pyttsx3

engine = pyttsx3.init()

voices = engine.getProperty('voices')

# Force Windows voice
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

engine.say("This is a voice test. If you hear this, voice is working.")
engine.runAndWait()

print("Voice test finished")
