import subprocess
import os
from datetime import datetime

def launch_application(app_name):
    """
    Launching a specific application like Chrome
    
    Args:
        app_name: The name of the application to launch
    
    Returns:
        str: Success/error message with ✅/❌ prefix
    """
    try:
        if app_name not in ['Safari', 'Chrome', 'Firefox', 'Photo Booth', 'QuickTime Player', 'Finder', 'Terminal', 'System Preferences', 'Activity Monitor', 'Calculator', 'Calendar', 'Contacts', 'Mail', 'Messages', 'Music', 'Photos', 'Reminders', 'Notes', 'TextEdit', 'Preview']:
            return "❌ Error: Application not found"
        
        os.system(f"open -a '{app_name}'")
        return "✅ Success: Application opened"
    except Exception as e:
        return f"❌ Error: {str(e)}"