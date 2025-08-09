# mcp/tools/show_system_notification.py
import subprocess
import os

def show_system_notification(notification_message, notification_type):
    """
    The ability to show system notifications
    
    Args:
        notification_message: Message to display in the notification
        notification_type: Type of the notification
    
    Returns:
        str: Success/error message with ✅/❌ prefix
    """
    try:
        osascript_command = f"osascript -e 'display notification \"{notification_message}\" with title \"{notification_type}\"'"
        subprocess.run(osascript_command, shell=True, check=True)
        return "✅ Success: Notification displayed"
    except subprocess.CalledProcessError as e:
        return f"❌ Error: {e}"
    except Exception as e:
        return f"❌ Error: {e}"