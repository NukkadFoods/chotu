# mcp/tools/productivity.py
import subprocess
import json
import os
from datetime import datetime

def take_screenshot(filename=None):
    """Take a screenshot using macOS built-in tools"""
    try:
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        # Use macOS screencapture command
        result = subprocess.run(['screencapture', '-x', filename], capture_output=True)
        
        if result.returncode == 0:
            return f"Screenshot saved as {filename}"
        else:
            return "Failed to take screenshot"
            
    except Exception as e:
        return f"Screenshot error: {str(e)}"

def get_system_info():
    """Get system information"""
    try:
        info = {}
        
        # Get system info using system_profiler
        commands = {
            'battery': "pmset -g batt | grep -o '[0-9]*%'",
            'memory': "top -l 1 -s 0 | grep PhysMem",
            'disk': "df -h / | tail -1 | awk '{print $5}'",
            'uptime': "uptime | awk '{print $3 $4}' | sed 's/,//'",
            'temperature': "sudo powermetrics --samplers smc -n 1 2>/dev/null | grep -i temp | head -1"
        }
        
        for key, cmd in commands.items():
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    info[key] = result.stdout.strip()
                else:
                    info[key] = "N/A"
            except:
                info[key] = "N/A"
        
        return f"Battery: {info.get('battery', 'N/A')}, Disk Usage: {info.get('disk', 'N/A')}, Uptime: {info.get('uptime', 'N/A')}"
        
    except Exception as e:
        return f"System info error: {str(e)}"

def toggle_do_not_disturb():
    """Toggle Do Not Disturb mode"""
    try:
        script = '''
        tell application "System Events"
            tell process "SystemUIServer"
                click menu bar item "Notification Center" of menu bar 1
                delay 0.5
                click button "Do Not Disturb" of group 1 of UI element 1 of scroll area 1 of group 1 of window "Notification Center"
            end tell
        end tell
        '''
        
        result = subprocess.run(['osascript', '-e', script], capture_output=True)
        return "Do Not Disturb toggled" if result.returncode == 0 else "Failed to toggle Do Not Disturb"
        
    except Exception as e:
        return f"DND toggle error: {str(e)}"

def get_running_apps():
    """Get list of currently running applications"""
    try:
        script = '''
        tell application "System Events"
            set appList to {}
            repeat with proc in (every process whose background only is false)
                set end of appList to name of proc
            end repeat
            return appList
        end tell
        '''
        
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        if result.returncode == 0:
            apps = result.stdout.strip().split(', ')
            return f"Running apps: {', '.join(apps[:10])}..."  # Show first 10
        else:
            return "Could not get running apps"
            
    except Exception as e:
        return f"Apps list error: {str(e)}"

def create_reminder(title, due_date=None):
    """Create a reminder in macOS Reminders app"""
    try:
        if due_date:
            script = f'''
            tell application "Reminders"
                make new reminder with properties {{name:"{title}", due date:date "{due_date}"}}
            end tell
            '''
        else:
            script = f'''
            tell application "Reminders"
                make new reminder with properties {{name:"{title}"}}
            end tell
            '''
        
        result = subprocess.run(['osascript', '-e', script], capture_output=True)
        return f"Reminder '{title}' created" if result.returncode == 0 else "Failed to create reminder"
        
    except Exception as e:
        return f"Reminder error: {str(e)}"
