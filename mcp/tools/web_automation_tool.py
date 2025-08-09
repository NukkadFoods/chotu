#!/usr/bin/env python3
"""
🌐 CHOTU WEB AUTOMATION TOOL
===========================
Main web automation tool that integrates with Chotu's MCP architecture
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add project paths
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

try:
    from mcp.tools.web_automation.coordinator import WebAutomationCoordinator
except ImportError as e:
    print(f"⚠️ Web automation components not fully available: {e}")
    WebAutomationCoordinator = None

def web_automation_tool(command: str, headless: bool = False, context: Dict = None) -> Dict[str, Any]:
    """
    Main web automation function for Chotu
    
    Args:
        command: Natural language web automation command
        headless: Whether to run browser in headless mode
        context: Additional context for the task
        
    Returns:
        Dict: Result of web automation task
    """
    
    print(f"🌐 CHOTU WEB AUTOMATION")
    print(f"Command: {command}")
    print(f"Headless: {headless}")
    
    if not WebAutomationCoordinator:
        return {
            "success": False,
            "error": "Web automation components not available",
            "suggestion": "Install required dependencies: selenium, opencv-python, pytesseract"
        }
    
    try:
        # Initialize coordinator
        coordinator = WebAutomationCoordinator(headless=headless)
        
        # Execute the web command
        result = coordinator.handle_web_command(command, context)
        
        # Add Chotu-specific metadata
        result["tool"] = "web_automation"
        result["chotu_timestamp"] = datetime.now().isoformat()
        result["integration_version"] = "2.1"
        
        # Log the interaction
        _log_web_interaction(command, result)
        
        return result
        
    except Exception as e:
        error_result = {
            "success": False,
            "error": str(e),
            "tool": "web_automation",
            "command": command,
            "timestamp": datetime.now().isoformat()
        }
        
        _log_web_interaction(command, error_result)
        return error_result

def search_web(query: str, search_engine: str = "google") -> Dict[str, Any]:
    """
    Simplified web search function
    
    Args:
        query: Search query
        search_engine: Search engine to use (google, youtube, etc.)
        
    Returns:
        Dict: Search results and status
    """
    
    if search_engine.lower() == "google":
        command = f"Search Google for {query}"
    elif search_engine.lower() == "youtube":
        command = f"Search YouTube for {query}"
    else:
        command = f"Search {search_engine} for {query}"
    
    return web_automation_tool(command)

def extract_web_data(url: str, data_type: str = "text") -> Dict[str, Any]:
    """
    Extract data from a web page
    
    Args:
        url: URL to extract data from
        data_type: Type of data to extract (text, price, title, etc.)
        
    Returns:
        Dict: Extracted data and status
    """
    
    command = f"Go to {url} and extract {data_type}"
    return web_automation_tool(command)

def fill_web_form(url: str, form_data: Dict[str, str]) -> Dict[str, Any]:
    """
    Fill a web form
    
    Args:
        url: URL of the form
        form_data: Dictionary of field names and values
        
    Returns:
        Dict: Form filling result and status
    """
    
    form_description = ", ".join([f"{field}={value}" for field, value in form_data.items()])
    command = f"Go to {url} and fill form with {form_description}"
    
    context = {"form_data": form_data}
    return web_automation_tool(command, context=context)

def _log_web_interaction(command: str, result: Dict[str, Any]):
    """Log web automation interaction for learning"""
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "command": command,
        "success": result.get("success", False),
        "duration": result.get("duration_seconds", 0),
        "error": result.get("error"),
        "steps_completed": result.get("execution_details", {}).get("steps_completed", 0)
    }
    
    # Append to web automation log
    log_file = os.path.join(project_root, "logs", "web_automation.json")
    
    try:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(log_entry)
        
        # Keep only last 100 entries
        if len(logs) > 100:
            logs = logs[-100:]
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
            
    except Exception as e:
        print(f"⚠️ Failed to log web interaction: {e}")

def get_web_automation_status() -> Dict[str, Any]:
    """Get current web automation status and capabilities"""
    
    status = {
        "available": WebAutomationCoordinator is not None,
        "dependencies": {
            "selenium": False,
            "opencv": False,
            "tesseract": False
        },
        "capabilities": [],
        "known_sites": []
    }
    
    # Check dependencies
    try:
        import selenium
        status["dependencies"]["selenium"] = True
        status["capabilities"].append("browser_control")
    except ImportError:
        pass
    
    try:
        import cv2
        status["dependencies"]["opencv"] = True
        status["capabilities"].append("computer_vision")
    except ImportError:
        pass
    
    try:
        import pytesseract
        status["dependencies"]["tesseract"] = True
        status["capabilities"].append("ocr_text_detection")
    except ImportError:
        pass
    
    # Check known sites
    profiles_dir = os.path.join(project_root, "config", "web_profiles")
    if os.path.exists(profiles_dir):
        for file in os.listdir(profiles_dir):
            if file.endswith('.json'):
                status["known_sites"].append(file[:-5])
    
    return status

def install_web_automation_dependencies():
    """Install required dependencies for web automation"""
    
    print("📦 Installing web automation dependencies...")
    
    dependencies = [
        "selenium",
        "opencv-python",
        "pytesseract",
        "pillow"
    ]
    
    import subprocess
    
    for dep in dependencies:
        try:
            print(f"Installing {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ {dep} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {dep}: {e}")
    
    print("\n🔧 Additional setup required:")
    print("1. Install Chrome browser if not already installed")
    print("2. Install Tesseract OCR:")
    print("   macOS: brew install tesseract")
    print("   Windows: Download from github.com/UB-Mannheim/tesseract/wiki")
    print("3. Install ChromeDriver or use selenium manager")

# Example usage and testing
if __name__ == "__main__":
    print("🧪 Testing Chotu Web Automation...")
    
    # Check status
    status = get_web_automation_status()
    print(f"Status: {status}")
    
    if status["available"]:
        # Test basic search
        result = search_web("Python programming tutorials")
        print(f"Search result: {'SUCCESS' if result.get('success') else 'FAILED'}")
        
        if result.get('error'):
            print(f"Error: {result['error']}")
    else:
        print("⚠️ Web automation not available. Installing dependencies...")
        install_web_automation_dependencies()
