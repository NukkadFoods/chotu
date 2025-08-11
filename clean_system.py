#!/usr/bin/env python3
"""
🧹 CHOTU SYSTEM CLEANER
======================
Clean up debug files, test files, and old versions to keep the system organized
"""

import os
import shutil
import glob
from pathlib import Path

def clean_system():
    """Clean up the Chotu system"""
    
    base_path = "/Users/mahendrabahubali/chotu"
    
    print("🧹 Starting Chotu System Cleanup")
    print("=" * 50)
    
    # Files and patterns to remove
    cleanup_patterns = [
        # Debug files
        "debug_*.py",
        "simple_*.py", 
        "quick_*.py",
        "*debug*.py",
        
        # Test files (keep essential ones)
        "test_*.py",
        "*_test.py",
        
        # Old/backup files
        "*.backup",
        "*.old",
        "*_backup.py",
        "*_old.py",
        
        # Temporary files
        "*.tmp",
        "*.temp",
        "demo.db",
        
        # Old YouTube files
        "chotu_youtube_*.py",
        "*youtube_vision*.png",
        
        # Old email senders
        "chotu_email_*.py",
        "chotu_send_*.py",
        "chotu_improved_*.py",
        
        # Old web automation
        "chotu_web_*.py",
        
        # Log files (keep directory but clean old logs)
        "logs/*.log",
        "mcp/logs/*.log",
        
        # Cache and temp directories
        "__pycache__",
        "*.pyc",
        ".DS_Store"
    ]
    
    # Essential files to keep (exceptions)
    keep_files = [
        "test_chotu_schema_learning.py",  # Our main schema test
        "test_system_monitoring.py",     # Current system test
        "enhanced_learning_controller.py", # Core system
        "schema_manager.py",             # Core system
        "macos_schema.json",             # Core schema
    ]
    
    files_removed = 0
    
    # Clean root directory
    print("\n📁 Cleaning root directory...")
    for pattern in cleanup_patterns:
        for file_path in glob.glob(os.path.join(base_path, pattern)):
            filename = os.path.basename(file_path)
            if filename not in keep_files:
                try:
                    if os.path.isdir(file_path) and "__pycache__" in file_path:
                        shutil.rmtree(file_path)
                        print(f"🗑️ Removed directory: {filename}")
                    elif os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"🗑️ Removed file: {filename}")
                    files_removed += 1
                except Exception as e:
                    print(f"⚠️ Could not remove {filename}: {e}")
    
    # Clean MCP tools directory
    print("\n📁 Cleaning MCP tools directory...")
    tools_path = os.path.join(base_path, "mcp", "tools")
    
    # Remove test files from tools directory
    test_files = [
        "test_*.py",
        "quick_*.py", 
        "verify_*.py",
        "*_test.py"
    ]
    
    for pattern in test_files:
        for file_path in glob.glob(os.path.join(tools_path, pattern)):
            filename = os.path.basename(file_path)
            try:
                os.remove(file_path)
                print(f"🗑️ Removed tool test: {filename}")
                files_removed += 1
            except Exception as e:
                print(f"⚠️ Could not remove {filename}: {e}")
    
    # Clean backup files in tools
    backup_files = glob.glob(os.path.join(tools_path, "*.backup"))
    for file_path in backup_files:
        filename = os.path.basename(file_path)
        try:
            os.remove(file_path)
            print(f"🗑️ Removed backup: {filename}")
            files_removed += 1
        except Exception as e:
            print(f"⚠️ Could not remove {filename}: {e}")
    
    # Clean old YouTube vision images
    vision_files = glob.glob(os.path.join(base_path, "mcp", "*youtube_vision*.png"))
    for file_path in vision_files:
        filename = os.path.basename(file_path)
        try:
            os.remove(file_path)
            print(f"🗑️ Removed vision file: {filename}")
            files_removed += 1
        except Exception as e:
            print(f"⚠️ Could not remove {filename}: {e}")
    
    # Clean auto-generated tools (keep recent ones)
    print("\n📁 Cleaning old auto-generated tools...")
    dynamic_tools_path = os.path.join(base_path, "mcp", "dynamic_tools")
    
    if os.path.exists(dynamic_tools_path):
        auto_tools = glob.glob(os.path.join(dynamic_tools_path, "auto_generated_tool_*.py"))
        
        # Keep only the latest 3 auto-generated tools
        auto_tools.sort(key=lambda x: os.path.getctime(x), reverse=True)
        
        tools_to_remove = auto_tools[3:]  # Remove all but the 3 most recent
        
        for file_path in tools_to_remove:
            filename = os.path.basename(file_path)
            try:
                os.remove(file_path)
                print(f"🗑️ Removed old auto-tool: {filename}")
                files_removed += 1
            except Exception as e:
                print(f"⚠️ Could not remove {filename}: {e}")
    
    # Clean cache directories
    print("\n📁 Cleaning cache directories...")
    cache_dirs = [
        os.path.join(base_path, "__pycache__"),
        os.path.join(base_path, "mcp", "__pycache__"),
        os.path.join(base_path, "mcp", "tools", "__pycache__"),
        os.path.join(base_path, "utils", "__pycache__"),
        os.path.join(base_path, "memory", "__pycache__")
    ]
    
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            try:
                shutil.rmtree(cache_dir)
                print(f"🗑️ Removed cache: {os.path.basename(cache_dir)}")
                files_removed += 1
            except Exception as e:
                print(f"⚠️ Could not remove cache {cache_dir}: {e}")
    
    return files_removed

def show_cleanup_summary():
    """Show what will be cleaned"""
    print("📋 Files that will be cleaned:")
    print("• Debug files (debug_*, simple_*, quick_*)")
    print("• Old test files (keeping essential schema tests)")
    print("• Backup files (*.backup, *_backup.py)")
    print("• Old YouTube automation files")
    print("• Old email sender files") 
    print("• Temporary files (*.tmp, demo.db)")
    print("• Cache directories (__pycache__)")
    print("• Old auto-generated tools (keeping latest 3)")
    print("• YouTube vision images")
    print("\n✅ Essential files will be preserved:")
    print("• enhanced_learning_controller.py")
    print("• schema_manager.py")
    print("• macos_schema.json")
    print("• test_chotu_schema_learning.py")
    print("• Core MCP tools")

if __name__ == "__main__":
    show_cleanup_summary()
    
    response = input("\n🤔 Proceed with cleanup? (y/N): ").strip().lower()
    
    if response == 'y' or response == 'yes':
        files_removed = clean_system()
        print(f"\n🎉 Cleanup complete! Removed {files_removed} files/directories")
        print("✨ Chotu system is now clean and organized!")
    else:
        print("❌ Cleanup cancelled.")
