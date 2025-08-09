# mcp/tools/text_to_speech.py
import pyttsx3

def text_to_speech(text):
    """
    Converts text to speech
    
    Args:
        text: The text to be converted to speech
    
    Returns:
        str: Success/error message
    """
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        return "✅ Success: Text converted to speech"
    except Exception as e:
        return f"❌ Error: {e}"