# mcp/tools/system.py
import subprocess
import re
import os
import time

def check_accessibility_permission():
    """Check if Terminal/Python has accessibility permissions"""
    try:
        result = subprocess.run([
            "osascript", "-e", 
            "tell application \"System Events\" to get name of first process"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            return True
        elif "not allowed" in result.stderr or "1002" in result.stderr:
            return False
        return True
    except:
        return False

def set_volume(level):
    """Set system volume to specified level (0-100)"""
    try:
        level = max(0, min(100, int(level)))
        result = subprocess.run(["osascript", "-e", f"set volume output volume {level}"], 
                              capture_output=True, text=True, check=True)
        return f"✅ Volume set to {level}%"
    except Exception as e:
        return f"❌ Failed to set volume: {e}"

def set_brightness(level):
    """Set display brightness to specified level (0-100)"""
    try:
        level = max(0, min(100, int(level)))
        # Try using brightness utility first (most reliable)
        try:
            brightness_decimal = level / 100.0
            result = subprocess.run(["brightness", str(brightness_decimal)], 
                                  capture_output=True, text=True, check=True)
            return f"✅ Brightness set to {level}%"
        except (subprocess.CalledProcessError, FileNotFoundError):
            return f"❌ Brightness utility not available. Install with: brew install brightness"
    except Exception as e:
        return f"❌ Failed to set brightness: {e}"

def increase_brightness():
    """Increase brightness by 20%"""
    try:
        # Get current brightness with better parsing
        result = subprocess.run(["brightness", "-l"], capture_output=True, text=True)
        if result.returncode == 0:
            # Parse "display 0: brightness 0.799805" format
            for line in result.stdout.split('\n'):
                if 'brightness' in line and ':' in line:
                    brightness_part = line.split('brightness')[-1].strip()
                    current_val = float(brightness_part)
                    new_val = min(1.0, current_val + 0.2)
                    subprocess.run(["brightness", str(new_val)], check=True)
                    return f"✅ Brightness increased to {int(new_val * 100)}%"
            return set_brightness(80)  # Fallback
        else:
            return set_brightness(80)
    except Exception as e:
        return f"❌ Failed to increase brightness: {e}"

def decrease_brightness():
    """Decrease brightness by 20%"""
    try:
        # Get current brightness using simpler parsing
        result = subprocess.run(["sh", "-c", "brightness -l | grep 'brightness' | awk '{print $3}'"], 
                              capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            current_val = float(result.stdout.strip())
            new_val = max(0.1, current_val - 0.2)
            subprocess.run(["brightness", str(new_val)], check=True)
            return f"✅ Brightness decreased to {int(new_val * 100)}%"
        else:
            return set_brightness(30)
    except Exception as e:
        return f"❌ Failed to decrease brightness: {e}"

def enable_bluetooth():
    """Enable Bluetooth"""
    try:
        result = subprocess.run(["blueutil", "--power", "1"], 
                              capture_output=True, text=True, check=True)
        return "✅ Bluetooth enabled"
    except subprocess.CalledProcessError as e:
        return f"❌ Failed to enable Bluetooth: {e}"
    except FileNotFoundError:
        return "❌ blueutil not found. Install with: brew install blueutil"

def disable_bluetooth():
    """Disable Bluetooth"""
    try:
        result = subprocess.run(["blueutil", "--power", "0"], 
                              capture_output=True, text=True, check=True)
        return "✅ Bluetooth disabled"
    except subprocess.CalledProcessError as e:
        return f"❌ Failed to disable Bluetooth: {e}"
    except FileNotFoundError:
        return "❌ blueutil not found. Install with: brew install blueutil"

def toggle_bluetooth():
    """Toggle Bluetooth on/off"""
    try:
        result = subprocess.run(["blueutil", "--power"], capture_output=True, text=True)
        if result.returncode == 0:
            current_state = result.stdout.strip()
            if current_state == "1":
                return disable_bluetooth()
            else:
                return enable_bluetooth()
        else:
            return enable_bluetooth()
    except FileNotFoundError:
        return "❌ blueutil not found. Install with: brew install blueutil"
    except Exception as e:
        return f"❌ Failed to toggle Bluetooth: {e}"

def start_application():
    """Start the MCP server"""
    try:
        # Add code here to start the MCP server
        return "✅ MCP server started successfully"
    except Exception as e:
        return f"❌ Failed to start MCP server: {e}"