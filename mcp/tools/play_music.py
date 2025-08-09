# mcp/tools/play_music.py
import subprocess
import os

def play_music(song_name):
    """
    Plays the specified song
    
    Args:
        song_name: The name of the song to play
    
    Returns:
        str: Success/error message
    """
    try:
        result = subprocess.run(["command"], capture_output=True, text=True, check=True)
        return f"✅ Success: {result.stdout.strip()}"
    except Exception as e:
        return f"❌ Error: {e}"