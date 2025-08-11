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
    from mcp.tools.enhanced_youtube_automation import enhanced_youtube_play, enhanced_youtube_stop, enhanced_youtube_status, enhanced_youtube_close
    ENHANCED_YOUTUBE_AVAILABLE = True
    print("✅ Enhanced YouTube automation loaded successfully")
except ImportError:
    try:
        # Try relative imports
        from .web_automation.coordinator import WebAutomationCoordinator
        from .enhanced_youtube_automation import enhanced_youtube_play, enhanced_youtube_stop, enhanced_youtube_status, enhanced_youtube_close
        ENHANCED_YOUTUBE_AVAILABLE = True
        print("✅ Enhanced YouTube automation loaded via relative import")
    except ImportError:
        try:
            # Try direct imports for coordinator and YouTube automation
            from web_automation.coordinator import WebAutomationCoordinator
            from enhanced_youtube_automation import enhanced_youtube_play, enhanced_youtube_stop, enhanced_youtube_status, enhanced_youtube_close
            ENHANCED_YOUTUBE_AVAILABLE = True
            print("✅ Web automation loaded via direct import")
        except ImportError:
            try:
                # YouTube only (fallback)
                from enhanced_youtube_automation import enhanced_youtube_play, enhanced_youtube_stop, enhanced_youtube_status, enhanced_youtube_close
                WebAutomationCoordinator = None
                ENHANCED_YOUTUBE_AVAILABLE = True
                print("✅ Enhanced YouTube automation loaded via direct import")
                print("ℹ️ General web automation coordinator not available")
            except ImportError:
                try:
                    # Add path and try enhanced YouTube automation again
                    import sys
                    import os
                    base_path = "/Users/mahendrabahubali/chotu"
                    if f"{base_path}/mcp/tools" not in sys.path:
                        sys.path.insert(0, f"{base_path}/mcp/tools")
                    from enhanced_youtube_automation import enhanced_youtube_play, enhanced_youtube_stop, enhanced_youtube_status, enhanced_youtube_close
                    WebAutomationCoordinator = None
                    ENHANCED_YOUTUBE_AVAILABLE = True
                    print("✅ Enhanced YouTube automation loaded via path fix")
                    print("ℹ️ General web automation coordinator not available")
                except ImportError:
                    print("ℹ️ Enhanced YouTube automation not available - using fallback methods")
                    WebAutomationCoordinator = None
                    ENHANCED_YOUTUBE_AVAILABLE = False

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
    
    # Check if this is a YouTube command and use enhanced automation
    command_lower = command.lower()
    youtube_triggers = [
        "youtube", "play", "song", "music", "video", 
        "search youtube", "open youtube", "stop video", "pause video"
    ]
    
    if any(trigger in command_lower for trigger in youtube_triggers):
        if ENHANCED_YOUTUBE_AVAILABLE:
            print("🎵 Using enhanced YouTube automation...")
            return _handle_youtube_command(command, context)
        else:
            print("⚠️ Enhanced YouTube automation not available, using standard automation...")
    
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

def _handle_youtube_command(command: str, context: Dict = None) -> Dict[str, Any]:
    """Handle YouTube-specific commands with enhanced automation"""
    
    command_lower = command.lower()
    
    # Stop/pause commands
    if any(word in command_lower for word in ["stop", "pause", "close"]):
        print("⏹️ Processing stop command...")
        result = enhanced_youtube_stop()
        result["tool"] = "enhanced_youtube"
        result["command"] = command
        return result
    
    # Play/search commands
    if any(word in command_lower for word in ["play", "search", "find", "open"]):
        print("▶️ Processing play command...")
        
        # Extract search query from command
        search_query = _extract_youtube_query(command)
        
        if search_query:
            # Check if we should stop current video
            stop_current = any(word in command_lower for word in ["stop", "different", "new", "change"])
            
            result = enhanced_youtube_play(search_query, stop_current=stop_current)
            result["tool"] = "enhanced_youtube"
            result["command"] = command
            result["extracted_query"] = search_query
            return result
        else:
            return {
                "success": False,
                "error": "Could not extract search query from command",
                "command": command,
                "tool": "enhanced_youtube"
            }
    
    # Status commands
    if any(word in command_lower for word in ["status", "check", "current"]):
        print("📊 Processing status command...")
        result = enhanced_youtube_status()
        result["tool"] = "enhanced_youtube"
        result["command"] = command
        return result
    
    # Default: treat as play command
    search_query = _extract_youtube_query(command)
    if search_query:
        result = enhanced_youtube_play(search_query, stop_current=True)
        result["tool"] = "enhanced_youtube"
        result["command"] = command
        result["extracted_query"] = search_query
        return result
    
    return {
        "success": False,
        "error": "Could not understand YouTube command",
        "command": command,
        "tool": "enhanced_youtube"
    }

def _extract_youtube_query(command: str) -> str:
    """Extract search query from YouTube command"""
    
    command_lower = command.lower()
    
    # Remove common command words but keep important content words
    stop_words = [
        "can you", "please", "chotu", "on youtube", "in youtube", "from youtube", 
        "youtube", "video", "and play", "then play"
    ]
    
    # Clean the command - be more selective about word removal
    cleaned = command_lower
    for stop_word in stop_words:
        cleaned = cleaned.replace(stop_word, " ")
    
    # Remove extra spaces and get the query
    query = " ".join(cleaned.split()).strip()
    
    # If query is too short or still has command words, try pattern extraction
    if len(query) < 3 or any(word in query for word in ["play", "search", "find", "open"]):
        # Look for patterns like "play X songs" or "search for X"
        import re
        
        patterns = [
            r"play\s+(.+?)\s+(?:songs?|music|video|on)",
            r"search\s+(?:for\s+)?(.+?)\s+(?:on|in)",
            r"find\s+(.+?)\s+(?:on|in)",
            r"open\s+(.+?)\s+(?:on|in)",
            r"(?:play|search|find)\s+(.+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, command_lower)
            if match:
                extracted = match.group(1).strip()
                
                # Clean extracted query
                for stop_word in ["some", "for", "the"]:
                    if extracted.startswith(stop_word + " "):
                        extracted = extracted[len(stop_word):].strip()
                
                # Remove trailing words that are not part of the content
                trailing_words = ["on", "in", "from", "music", "songs", "video"]
                words = extracted.split()
                while words and words[-1] in trailing_words:
                    words.pop()
                
                if words:
                    query = " ".join(words)
                    break
    
    # Improve query for movie songs to get original versions
    if "movie" in query.lower() or "film" in query.lower():
        # Add keywords to prioritize original songs over remixes
        if "kasoor" in query.lower():
            query = query + " original songs bollywood soundtrack"
        elif any(movie in query.lower() for movie in ["movie", "film"]):
            query = query + " original songs soundtrack"
    
    # Filter out unwanted terms from user commands that leak into query
    unwanted_terms = ["stop this song", "stop current", "this song"]
    for term in unwanted_terms:
        query = query.replace(term, "").strip()
    
    # Clean up extra spaces
    query = " ".join(query.split())
    
    return query if len(query) >= 2 else command.strip()

def enhanced_stop_video() -> Dict[str, Any]:
    """
    Stop currently playing YouTube video
    
    Returns:
        Dict: Result of stop operation
    """
    
    if ENHANCED_YOUTUBE_AVAILABLE:
        return enhanced_youtube_stop()
    else:
        return {
            "success": False,
            "error": "Enhanced YouTube automation not available"
        }

def enhanced_play_video(query: str, stop_current: bool = True) -> Dict[str, Any]:
    """
    Play YouTube video with enhanced controls
    
    Args:
        query: Search query for the video
        stop_current: Whether to stop current video first
        
    Returns:
        Dict: Result of play operation
    """
    
    if ENHANCED_YOUTUBE_AVAILABLE:
        return enhanced_youtube_play(query, stop_current)
    else:
        return {
            "success": False,
            "error": "Enhanced YouTube automation not available"
        }

def get_youtube_session_status() -> Dict[str, Any]:
    """
    Get current YouTube session status
    
    Returns:
        Dict: Session status information
    """
    
    if ENHANCED_YOUTUBE_AVAILABLE:
        return enhanced_youtube_status()
    else:
        return {
            "session_active": False,
            "error": "Enhanced YouTube automation not available"
        }

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

def enhanced_stop_video() -> Dict[str, Any]:
    """
    Stop currently playing YouTube video
    
    Returns:
        Dict: Result of stop operation
    """
    
    if ENHANCED_YOUTUBE_AVAILABLE:
        return enhanced_youtube_stop()
    else:
        return {
            "success": False,
            "error": "Enhanced YouTube automation not available"
        }

def enhanced_play_video(query: str, stop_current: bool = True) -> Dict[str, Any]:
    """
    Play YouTube video with enhanced controls
    
    Args:
        query: Search query for the video
        stop_current: Whether to stop current video first
        
    Returns:
        Dict: Result of play operation
    """
    
    if ENHANCED_YOUTUBE_AVAILABLE:
        return enhanced_youtube_play(query, stop_current)
    else:
        return {
            "success": False,
            "error": "Enhanced YouTube automation not available"
        }

def get_youtube_session_status() -> Dict[str, Any]:
    """
    Get current YouTube session status
    
    Returns:
        Dict: Session status information
    """
    
    if ENHANCED_YOUTUBE_AVAILABLE:
        return enhanced_youtube_status()
    else:
        return {
            "session_active": False,
            "error": "Enhanced YouTube automation not available"
        }

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
