# mcp/tools/voice_recognition.py
import subprocess
import os
from datetime import datetime

def voice_recognition(param1=None, param2=None):
    """
    voice recognition
    
    Args:
        param1: Description (optional with default)
        param2: Description (optional with default)
    
    Returns:
        str: Success/error message with ✅/❌ prefix
    """
    try:
        subprocess.run(['which', 'imagesnap'], capture_output=True, check=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        subprocess.run(['imagesnap', f'photo_{timestamp}.jpg'])
        return "✅ Success: Photo taken"
    except subprocess.CalledProcessError:
        osascript_cmd = 'osascript -e \'tell app "Photo Booth" to activate\' -e \'tell app "System Events" to keystroke "c" using {command down}\''
        subprocess.run(osascript_cmd, shell=True)
        return "✅ Success: Photo taken using Photo Booth"
    except Exception as e:
        return f"❌ Error: {e}"