# mcp/tools/calendar.py
import subprocess
import json
from datetime import datetime, timedelta

def get_calendar_events(days_ahead=7):
    """Get calendar events for the next few days using macOS Calendar"""
    try:
        # Use AppleScript to get calendar events
        script = f'''
        tell application "Calendar"
            set startDate to current date
            set endDate to startDate + ({days_ahead} * days)
            set eventList to {{}}
            
            repeat with cal in calendars
                set calEvents to (every event of cal whose start date ≥ startDate and start date ≤ endDate)
                repeat with evt in calEvents
                    set eventInfo to (summary of evt as string) & " | " & (start date of evt as string)
                    set end of eventList to eventInfo
                end repeat
            end repeat
            
            return eventList
        end tell
        '''
        
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        if result.returncode == 0:
            events = result.stdout.strip().split(', ')
            return [event for event in events if event.strip()]
        else:
            return ["No calendar events found or Calendar app not accessible"]
            
    except Exception as e:
        return [f"Error accessing calendar: {str(e)}"]

def create_calendar_event(title, date_time, duration_minutes=60):
    """Create a new calendar event"""
    try:
        script = f'''
        tell application "Calendar"
            tell calendar "Work"
                make new event with properties {{summary:"{title}", start date:date "{date_time}", end date:date "{date_time}" + {duration_minutes} * minutes}}
            end tell
        end tell
        '''
        
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        return "Event created successfully" if result.returncode == 0 else "Failed to create event"
        
    except Exception as e:
        return f"Error creating event: {str(e)}"

def get_next_meeting():
    """Get the next upcoming meeting"""
    events = get_calendar_events(1)  # Next 1 day
    if events and events[0] != "No calendar events found or Calendar app not accessible":
        return f"Next meeting: {events[0]}"
    return "No upcoming meetings found"
