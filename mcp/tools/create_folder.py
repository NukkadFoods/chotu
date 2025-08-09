# mcp/tools/create_folder.py
import subprocess
import os

def create_folder(folder_name):
    """
    Creates a folder with the specified name
    
    Args:
        folder_name: The name of the folder to be created
    
    Returns:
        str: Success/error message
    """
    try:
        os.mkdir(folder_name)
        return f"✅ Success: Folder '{folder_name}' created"
    except Exception as e:
        return f"❌ Error: {e}"