# mcp/tools/files.py
import subprocess
import os

def open_folder(path):
    if os.path.exists(path):
        subprocess.run(["open", path])
    else:
        print(f"Path not found: {path}")
