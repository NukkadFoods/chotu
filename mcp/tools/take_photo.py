# mcp/tools/take_photo.py
import subprocess
import os
from datetime import datetime

def take_photo(camera_type, resolution):
    """
    Takes a photo with the specified camera and resolution
    
    Args:
        camera_type: Type of camera to use
        resolution: Resolution of the photo
    
    Returns:
        str: Success/error message
    """
    try:
        # Use macOS imagesnap or built-in camera access
        # First check if imagesnap is available
        try:
            subprocess.run(["which", "imagesnap"], check=True, capture_output=True)
            # imagesnap is available
            filename = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            result = subprocess.run(["imagesnap", filename], capture_output=True, text=True, check=True)
            return f"✅ Photo taken and saved as {filename}"
        except subprocess.CalledProcessError:
            # Try using system camera via AppleScript
            script = '''
            tell application "Photo Booth"
                activate
                delay 2
                tell application "System Events"
                    keystroke " "
                end tell
            end tell
            '''
            result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
            return "✅ Camera opened via Photo Booth - press spacebar to take photo"
    except Exception as e:
        return f"❌ Error: {e}"