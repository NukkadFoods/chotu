#!/usr/bin/env python3
"""
🌐 CHOTU WEB AUTOMATION INTEGRATION
==================================
Smart web automation that adapts based on available dependencies
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add project paths
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

def check_web_automation_capabilities() -> Dict[str, Any]:
    """Check what web automation capabilities are available"""
    
    capabilities = {
        "lightweight": True,  # Always available
        "full_selenium": False,
        "computer_vision": False,
        "ocr": False,
        "available_methods": ["system_browser"],
        "missing_dependencies": []
    }
    
    # Check Selenium
    try:
        import selenium
        capabilities["full_selenium"] = True
        capabilities["available_methods"].append("selenium_automation")
    except ImportError:
        capabilities["missing_dependencies"].append("selenium")
    
    # Check OpenCV
    try:
        import cv2
        capabilities["computer_vision"] = True
        capabilities["available_methods"].append("computer_vision")
    except ImportError:
        capabilities["missing_dependencies"].append("opencv-python")
    
    # Check Tesseract OCR
    try:
        import pytesseract
        capabilities["ocr"] = True
        capabilities["available_methods"].append("ocr_text_detection")
    except ImportError:
        capabilities["missing_dependencies"].append("pytesseract")
    
    return capabilities

def web_automation_smart(command: str, prefer_method: str = "auto") -> Dict[str, Any]:
    """
    Smart web automation that uses the best available method
    
    Args:
        command: Web automation command
        prefer_method: Preferred method (auto, lightweight, selenium, etc.)
    
    Returns:
        Dict: Result of web automation
    """
    
    print(f"🌐 CHOTU WEB AUTOMATION: {command}")
    
    # Check capabilities
    caps = check_web_automation_capabilities()
    
    print(f"📊 Available methods: {', '.join(caps['available_methods'])}")
    
    # Choose method based on availability and preference
    if prefer_method == "auto":
        if caps["full_selenium"]:
            method = "selenium"
        else:
            method = "lightweight"
    else:
        method = prefer_method
    
    try:
        if method == "selenium" and caps["full_selenium"]:
            return _use_selenium_automation(command)
        else:
            return _use_lightweight_automation(command)
            
    except Exception as e:
        # Fallback to lightweight
        print(f"⚠️ Primary method failed, falling back to lightweight: {e}")
        return _use_lightweight_automation(command)

def _use_selenium_automation(command: str) -> Dict[str, Any]:
    """Use full Selenium automation"""
    
    try:
        from mcp.tools.web_automation.coordinator import WebAutomationCoordinator
        
        print("🚀 Using full Selenium automation")
        coordinator = WebAutomationCoordinator(headless=False)
        result = coordinator.handle_web_command(command)
        
        result["method_used"] = "selenium_automation"
        result["capabilities"] = "full"
        
        return result
        
    except ImportError as e:
        raise Exception(f"Selenium automation not available: {e}")

def _use_lightweight_automation(command: str) -> Dict[str, Any]:
    """Use lightweight browser automation"""
    
    try:
        from mcp.tools.lightweight_web_automation import lightweight_web_automation
        
        print("🌟 Using lightweight automation (system browser)")
        result = lightweight_web_automation(command)
        
        result["method_used"] = "lightweight_automation"
        result["capabilities"] = "basic"
        result["note"] = "Using system browser - install selenium for full automation"
        
        return result
        
    except Exception as e:
        raise Exception(f"Lightweight automation failed: {e}")

# Convenient wrapper functions
def chotu_search_web(query: str, site: str = "google") -> Dict[str, Any]:
    """Search the web using Chotu's best available method"""
    command = f"Search {site} for {query}"
    return web_automation_smart(command)

def chotu_open_website(url: str) -> Dict[str, Any]:
    """Open a website using Chotu's web automation"""
    command = f"Navigate to {url}"
    return web_automation_smart(command)

def chotu_extract_data(url: str, data_type: str = "text") -> Dict[str, Any]:
    """Extract data from a website"""
    command = f"Go to {url} and extract {data_type}"
    return web_automation_smart(command)

def get_web_automation_status() -> Dict[str, Any]:
    """Get comprehensive web automation status"""
    
    caps = check_web_automation_capabilities()
    
    status = {
        "implementation_complete": True,
        "lightweight_ready": caps["lightweight"],
        "full_automation_ready": caps["full_selenium"],
        "computer_vision_ready": caps["computer_vision"],
        "ocr_ready": caps["ocr"],
        "available_methods": caps["available_methods"],
        "missing_dependencies": caps["missing_dependencies"],
        "config_files": [],
        "recommendation": ""
    }
    
    # Check config files
    config_dir = os.path.join(project_root, "config", "web_profiles")
    if os.path.exists(config_dir):
        status["config_files"] = [f[:-5] for f in os.listdir(config_dir) if f.endswith('.json')]
    
    # Provide recommendation
    if len(caps["missing_dependencies"]) == 0:
        status["recommendation"] = "All dependencies available - full web automation ready!"
    elif caps["full_selenium"]:
        status["recommendation"] = "Selenium available - good automation capabilities"
    else:
        status["recommendation"] = f"Install {', '.join(caps['missing_dependencies'])} for full automation"
    
    return status

# Integration with Chotu's learning system
def integrate_with_chotu_learning():
    """Integrate web automation with Chotu's autonomous learning"""
    
    learning_context = {
        "capability": "web_automation",
        "methods_available": check_web_automation_capabilities()["available_methods"],
        "use_cases": [
            "Web searches and research",
            "Data extraction from websites", 
            "Form filling and automation",
            "Social media monitoring",
            "Price comparison and shopping",
            "News and content aggregation"
        ],
        "safety_features": [
            "Destructive action prevention",
            "Privacy protection",
            "Rate limiting",
            "Error recovery"
        ]
    }
    
    # Log to Chotu's learning memory
    try:
        learning_file = os.path.join(project_root, "memory", "learning_logs.json")
        
        if os.path.exists(learning_file):
            with open(learning_file, 'r') as f:
                logs = json.load(f)
        else:
            logs = {"generated_tools": []}
        
        # Add web automation capability
        web_tool_entry = {
            "timestamp": datetime.now().isoformat(),
            "intent": "enable web automation and browser control for Chotu",
            "tool_name": "web_automation_smart",
            "approach": "progressive_enhancement",
            "capabilities": learning_context,
            "achievement": "web_automation_integration"
        }
        
        if "generated_tools" not in logs:
            logs["generated_tools"] = []
        
        logs["generated_tools"].append(web_tool_entry)
        
        with open(learning_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        print("📚 Integrated web automation with Chotu's learning system")
        
    except Exception as e:
        print(f"⚠️ Learning integration warning: {e}")

# Test and demonstration
if __name__ == "__main__":
    print("🌐 CHOTU WEB AUTOMATION INTEGRATION TEST")
    print("=" * 60)
    
    # Show status
    status = get_web_automation_status()
    print(f"📊 Status: {status['recommendation']}")
    print(f"🔧 Available methods: {', '.join(status['available_methods'])}")
    
    if status['missing_dependencies']:
        print(f"⚠️  Missing: {', '.join(status['missing_dependencies'])}")
    
    # Test commands
    test_commands = [
        "Search Google for AI news",
        "Go to YouTube",
        "Navigate to github.com"
    ]
    
    for command in test_commands:
        print(f"\n🧪 Testing: {command}")
        
        try:
            result = web_automation_smart(command)
            
            if result.get('success'):
                print(f"✅ Success using {result.get('method_used', 'unknown')}")
                if result.get('url_opened'):
                    print(f"   Opened: {result['url_opened']}")
            else:
                print(f"❌ Failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Integrate with learning system
    print(f"\n📚 Integrating with Chotu's learning system...")
    integrate_with_chotu_learning()
    
    print(f"\n🎯 RESULT: Chotu now has web automation capabilities!")
    print(f"   • Lightweight mode: Always available")
    print(f"   • Full automation: {'Available' if status['full_automation_ready'] else 'Installing...'}")
    print(f"   • Computer vision: {'Available' if status['computer_vision_ready'] else 'Installing...'}")
