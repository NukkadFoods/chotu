# mcp/mcp_server.py - Enhanced MCP Server
from flask import Flask, request, jsonify
import subprocess
import os
from tools.apps import open_app, close_app
from tools.files import open_folder
from tools.browser import open_url
from tools.system import set_volume, set_brightness
from tools.gpt_planner import generate_and_run
from tools.calendar import get_calendar_events, create_calendar_event, get_next_meeting
from tools.weather import get_weather_info, get_weather_forecast
from tools.productivity import (take_screenshot, get_system_info, 
                               toggle_do_not_disturb, get_running_apps, create_reminder)

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_task():
    """Enhanced task execution with new capabilities"""
    ram = request.json
    intent = ram.get("interpreted_intent", "").lower()
    nlp_analysis = ram.get("nlp_analysis", {})
    
    try:
        # System Control
        if "volume" in intent:
            if "up" in intent or "increase" in intent:
                result = set_volume(80)
            elif "down" in intent or "decrease" in intent:
                result = set_volume(30)
            elif "mute" in intent:
                result = set_volume(0)
            else:
                result = "Volume command unclear"
                
        elif "brightness" in intent:
            if "up" in intent or "increase" in intent:
                result = set_brightness(100)
            elif "down" in intent or "decrease" in intent:
                result = set_brightness(50)
            else:
                result = "Brightness command unclear"
        
        # Application Control
        elif "open safari" in intent or "browse" in intent:
            result = open_url("https://www.google.com")
            result = "Safari opened"
            
        elif "open code" in intent or "vs code" in intent:
            result = open_app("Visual Studio Code")
            result = "VS Code opened"
            
        elif "open folder" in intent or "project" in intent:
            result = open_folder("/Users/mahendrabahubali/Documents")
            result = "Documents folder opened"
        
        # Calendar Operations
        elif "calendar" in intent or "meeting" in intent or "event" in intent:
            if "next" in intent:
                result = get_next_meeting()
            elif "create" in intent or "schedule" in intent:
                # Extract event details from NLP analysis
                entities = nlp_analysis.get('entities', {})
                title = "Meeting"  # Default
                # This would be enhanced with better entity extraction
                result = create_calendar_event(title, "today 2:00 PM")
            else:
                events = get_calendar_events(3)
                result = f"Upcoming events: {', '.join(events[:3])}"
        
        # Weather Information
        elif "weather" in intent:
            if "forecast" in intent:
                result = get_weather_forecast()
            else:
                result = get_weather_info()
        
        # Productivity Tools
        elif "screenshot" in intent or "capture screen" in intent:
            result = take_screenshot()
            
        elif "system info" in intent or "system status" in intent:
            result = get_system_info()
            
        elif "do not disturb" in intent or "dnd" in intent:
            result = toggle_do_not_disturb()
            
        elif "running apps" in intent or "open applications" in intent:
            result = get_running_apps()
            
        elif "reminder" in intent:
            # Extract reminder text from input
            reminder_text = ram.get("raw_input", "").replace("create reminder", "").strip()
            if not reminder_text:
                reminder_text = "Task reminder"
            result = create_reminder(reminder_text)
        
        # Smart Responses based on Intent
        elif nlp_analysis.get('intent') == 'information':
            if "time" in intent:
                import datetime
                result = f"Current time is {datetime.datetime.now().strftime('%I:%M %p')}"
            elif "date" in intent:
                import datetime
                result = f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}"
            else:
                result = generate_and_run(intent)
        
        # Conversation and Context
        elif any(word in intent for word in ['hello', 'hi', 'hey', 'greetings']):
            result = "Hello! I'm Chotu, your AI assistant. How can I help you today?"
            
        elif any(word in intent for word in ['thank', 'thanks']):
            result = "You're welcome! Is there anything else I can help you with?"
            
        elif any(word in intent for word in ['how are you', 'status']):
            result = "I'm functioning perfectly and ready to assist you!"
        
        # Default: Use GPT Planner for unknown tasks
        else:
            result = generate_and_run(intent)
            
        return jsonify({
            "output": result,
            "intent_processed": intent,
            "nlp_analysis": nlp_analysis.get('intent', 'unknown'),
            "timestamp": ram.get('timestamp'),
            "success": True
        })
        
    except Exception as e:
        error_msg = f"Execution failed: {str(e)}"
        return jsonify({
            "output": error_msg,
            "intent_processed": intent,
            "success": False,
            "error": str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Chotu MCP Server is running",
        "capabilities": [
            "system_control", "app_management", "file_operations",
            "calendar", "weather", "productivity", "information"
        ]
    })

@app.route('/capabilities', methods=['GET'])
def get_capabilities():
    """Return available capabilities"""
    capabilities = {
        "system_control": ["volume", "brightness", "screenshot", "system_info"],
        "app_management": ["open_app", "close_app", "list_apps"],
        "file_operations": ["open_folder", "file_search"],
        "web_browser": ["open_url", "search"],
        "calendar": ["get_events", "create_event", "next_meeting"],
        "weather": ["current_weather", "forecast"],
        "productivity": ["reminders", "do_not_disturb", "system_status"],
        "information": ["time", "date", "general_queries"]
    }
    return jsonify(capabilities)

if __name__ == '__main__':
    print("🚀 Starting Enhanced Chotu MCP Server...")
    print("🔧 Available capabilities: System, Apps, Calendar, Weather, Productivity")
    app.run(host='localhost', port=5000, debug=True)
