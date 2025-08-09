# mcp/tools/weather.py
import requests
import json
import subprocess
from datetime import datetime

def get_weather_info(city="San Francisco"):
    """Get current weather information"""
    try:
        # Using OpenWeatherMap API (you'd need to add API key to .env)
        # For demo, using a simple weather service
        
        # Fallback to system location services on macOS
        script = '''
        tell application "System Events"
            try
                set weatherInfo to do shell script "curl -s 'https://wttr.in/?format=3'"
                return weatherInfo
            on error
                return "Weather information unavailable"
            end try
        end tell
        '''
        
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return "Unable to fetch weather information"
            
    except Exception as e:
        return f"Weather service error: {str(e)}"

def get_weather_forecast(days=3):
    """Get weather forecast for next few days"""
    try:
        script = f'''
        tell application "System Events"
            try
                set forecast to do shell script "curl -s 'https://wttr.in/?format=%l:+%c+%t+%h+%w+%p+%P'"
                return forecast
            on error
                return "Forecast unavailable"
            end try
        end tell
        '''
        
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else "Forecast unavailable"
        
    except Exception as e:
        return f"Forecast error: {str(e)}"
