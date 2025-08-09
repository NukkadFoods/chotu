# mcp/tools/open_application.py
import subprocess
import os
from datetime import datetime

def open_application(app_name):
    """
    open new application
    
    Args:
        app_name: The name of the application to be opened
    
    Returns:
        str: Success/error message with ✅/❌ prefix
    """
    try:
        subprocess.run(['open', '-a', app_name], check=True)
        return "✅ Success: Application opened"
    except subprocess.CalledProcessError as e:
        return f"❌ Error: {e}"

def enable_bluetooth():
    """
    enable Bluetooth settings
    
    Returns:
        str: Success/error message with ✅/❌ prefix
    """
    try:
        subprocess.run(['sudo', 'systemsetup', '-setbluetoothpower', 'on'], check=True)
        return "✅ Success: Bluetooth enabled"
    except subprocess.CalledProcessError as e:
        return f"❌ Error: {e}"

# mcp/tools/open_application.py
import subprocess
import os
from datetime import datetime

def open_application(app_name):
    """
    Open new application
    
    Args:
        app_name: The name of the application to be opened
    
    Returns:
        str: Success/error message with ✅/❌ prefix
    """
    try:
        subprocess.run(['open', '-a', app_name], check=True)
        return f"✅ Success: {app_name} opened"
    except subprocess.CalledProcessError as e:
        return f"❌ Error opening {app_name}: {e}"

def enable_bluetooth():
    """
    Enable Bluetooth settings
    
    Returns:
        str: Success/error message with ✅/❌ prefix
    """
    try:
        subprocess.run(['blueutil', '--power', '1'], check=True)
        return "✅ Success: Bluetooth enabled"
    except subprocess.CalledProcessError as e:
        return f"❌ Error enabling Bluetooth: {e}"

def list_available_bluetooth_devices():
    """
    List available Bluetooth devices
    
    Returns:
        str: List of available Bluetooth devices or error message with ✅/❌ prefix
    """
    try:
        output = subprocess.check_output(['blueutil', '--paired']).decode('utf-8')
        if output.strip():
            return f"✅ Available Bluetooth devices:\n{output}"
        else:
            return "✅ No Bluetooth devices found"
    except subprocess.CalledProcessError as e:
        return f"❌ Error listing Bluetooth devices: {e}"