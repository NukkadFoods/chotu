# utils/voice_input.py
import speech_recognition as sr

def listen_voice() -> str:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("👂 Chotu is listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    
    try:
        text = r.recognize_google(audio)
        print(f"🎙️ Heard: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
        return ""
    except sr.RequestError:
        print("⚠️  Speech recognition service down.")
        return ""
