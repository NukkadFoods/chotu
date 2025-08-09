# utils/voice_output.py
import subprocess
import platform

def speak(text: str):
    print(f"🤖 Chotu: {text}")
    if platform.system() == "Darwin":  # macOS
        subprocess.run(["say", text])
    else:
        print(f"[TTS] {text}")
