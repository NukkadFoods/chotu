# mcp/tools/execute_custom_command.py
import subprocess
import os
from datetime import datetime

def execute_custom_command(command):
    """
    Execute a custom command
    
    Args:
        command: Custom command to be executed
    
    Returns:
        str: Success/error message with ✅/❌ prefix
    """
    try:
        # Execute the custom command
        subprocess.run(command, shell=True, check=True)
        return "✅ Success: Command executed successfully"
    except subprocess.CalledProcessError as e:
        return f"❌ Error: {e}"
    except Exception as e:
        return f"❌ Error: {e}"