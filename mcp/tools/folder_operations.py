# mcp/tools/folder_operations.py
import os
import subprocess

def create_folder(folder_name, location=None):
    """
    Create a new folder/directory
    
    Args:
        folder_name: Name of the folder to create
        location: Path where to create the folder (default: Desktop)
    
    Returns:
        str: Success/error message
    """
    try:
        if not location:
            location = os.path.expanduser("~/Desktop")
        
        folder_path = os.path.join(location, folder_name)
        
        if os.path.exists(folder_path):
            return f"❌ Folder '{folder_name}' already exists at {location}"
        
        os.makedirs(folder_path)
        return f"✅ Created folder '{folder_name}' at {location}"
        
    except Exception as e:
        return f"❌ Failed to create folder: {e}"

def list_folders(location=None):
    """
    List all folders in a directory
    
    Args:
        location: Directory to list (default: Desktop)
    
    Returns:
        str: List of folders
    """
    try:
        if not location:
            location = os.path.expanduser("~/Desktop")
        
        folders = [item for item in os.listdir(location) 
                  if os.path.isdir(os.path.join(location, item))]
        
        if folders:
            return f"📁 Folders in {location}:\n" + "\n".join([f"  • {folder}" for folder in folders])
        else:
            return f"📁 No folders found in {location}"
            
    except Exception as e:
        return f"❌ Failed to list folders: {e}"

def delete_folder(folder_name, location=None):
    """
    Delete a folder (use with caution!)
    
    Args:
        folder_name: Name of the folder to delete
        location: Path where the folder is located (default: Desktop)
    
    Returns:
        str: Success/error message
    """
    try:
        if not location:
            location = os.path.expanduser("~/Desktop")
        
        folder_path = os.path.join(location, folder_name)
        
        if not os.path.exists(folder_path):
            return f"❌ Folder '{folder_name}' not found at {location}"
        
        if not os.path.isdir(folder_path):
            return f"❌ '{folder_name}' is not a folder"
        
        # Use rm -rf for better compatibility
        subprocess.run(["rm", "-rf", folder_path], check=True)
        return f"✅ Deleted folder '{folder_name}' from {location}"
        
    except Exception as e:
        return f"❌ Failed to delete folder: {e}"
