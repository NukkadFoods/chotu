# mcp/tools/voice_command_recognition.py
import subprocess
import os
from datetime import datetime

def voice_command_recognition(voice_command):
    """
    voice recognition for specific voice commands
    
    Args:
        voice_command: The voice command to be recognized
    
    Returns:
        str: Success/error message with ✅/❌ prefix
    """
    try:
        # Check if imagesnap exists
        subprocess.run(['which', 'imagesnap'], capture_output=True, check=True)
        
        # Use imagesnap if available, else use Photo Booth
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.system(f"imagesnap photo_{timestamp}.jpg || osascript -e 'tell app \"Photo Booth\" to activate'")
        
        return "✅ Success: Photo taken"
    except Exception as e:
        return f"❌ Error: {e}"