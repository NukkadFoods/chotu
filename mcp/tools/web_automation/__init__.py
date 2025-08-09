"""
🌐 CHOTU WEB AUTOMATION PACKAGE
==============================
Web automation capabilities for Chotu AI
"""

from .browser import WebCommander
from .web_agent import WebTaskPlanner  
from .vision_engine import VisualFinder
from .coordinator import WebAutomationCoordinator

__version__ = "2.1.0"
__author__ = "Chotu AI Development Team"

# Package metadata
PACKAGE_INFO = {
    "name": "chotu_web_automation",
    "version": __version__,
    "description": "Advanced web automation capabilities for Chotu AI",
    "components": [
        "WebCommander - Browser control with safety mechanisms",
        "WebTaskPlanner - Intelligent task planning with GPT",
        "VisualFinder - Computer vision and OCR for element detection", 
        "WebAutomationCoordinator - Main coordination and execution"
    ],
    "capabilities": [
        "Automated web navigation",
        "Form filling and submission",
        "Data extraction from web pages",
        "Intelligent element detection",
        "Task planning and execution",
        "Safety validation and error recovery"
    ],
    "safety_features": [
        "Destructive action prevention",
        "Rate limiting and throttling",
        "Privacy protection (cookie clearing)",
        "Screenshot-based debugging",
        "Sandboxed execution environment"
    ]
}

def get_package_info():
    """Get package information"""
    return PACKAGE_INFO

def check_dependencies():
    """Check if all required dependencies are available"""
    
    deps = {
        "selenium": False,
        "opencv-python": False,
        "pytesseract": False,
        "pillow": False
    }
    
    try:
        import selenium
        deps["selenium"] = True
    except ImportError:
        pass
    
    try:
        import cv2
        deps["opencv-python"] = True
    except ImportError:
        pass
    
    try:
        import pytesseract
        deps["pytesseract"] = True
    except ImportError:
        pass
    
    try:
        from PIL import Image
        deps["pillow"] = True
    except ImportError:
        pass
    
    return deps

__all__ = [
    'WebCommander',
    'WebTaskPlanner', 
    'VisualFinder',
    'WebAutomationCoordinator',
    'get_package_info',
    'check_dependencies'
]
