# mcp/tools/list_bluetooth_devices.py
import subprocess

def list_bluetooth_devices():
    """List paired and connected Bluetooth devices using blueutil"""
    try:
        # Get paired devices
        paired_result = subprocess.run(['blueutil', '--paired'], capture_output=True, text=True)
        connected_result = subprocess.run(['blueutil', '--connected'], capture_output=True, text=True)
        
        if paired_result.returncode != 0:
            return "❌ Failed to get Bluetooth device list. Make sure blueutil is installed: brew install blueutil"
        
        paired_devices = paired_result.stdout.strip()
        connected_devices = connected_result.stdout.strip()
        
        response = "📱 Bluetooth Devices:\n"
        
        if connected_devices:
            response += f"🟢 Connected:\n{connected_devices}\n\n"
        else:
            response += "🟢 Connected: None\n\n"
            
        if paired_devices:
            response += f"🔗 Paired:\n{paired_devices}"
        else:
            response += "🔗 Paired: None"
            
        return response
        
    except Exception as e:
        return f"❌ Error listing Bluetooth devices: {e}"