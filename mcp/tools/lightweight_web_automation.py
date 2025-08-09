#!/usr/bin/env python3
"""
🌐 CHOTU LIGHTWEIGHT WEB AUTOMATION
==================================
Simplified web automation that works without heavy dependencies
"""

import os
import sys
import json
import subprocess
import webbrowser
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add project paths
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from utils.gpt_interface import call_gpt_system

class LightweightWebAutomation:
    """Lightweight web automation using system browser and URL manipulation"""
    
    def __init__(self):
        self.web_profiles = self._load_web_profiles()
        self.session_history = []
        
        print("🌐 LightweightWebAutomation initialized")
        print(f"   Known sites: {len(self.web_profiles)}")
        print("   Mode: System browser integration")
    
    def _load_web_profiles(self) -> Dict:
        """Load site-specific configuration profiles"""
        profiles = {}
        profiles_dir = os.path.join(project_root, "config", "web_profiles")
        
        if os.path.exists(profiles_dir):
            for file in os.listdir(profiles_dir):
                if file.endswith('.json'):
                    site_name = file[:-5]
                    try:
                        with open(os.path.join(profiles_dir, file), 'r') as f:
                            profiles[site_name] = json.load(f)
                    except Exception as e:
                        print(f"⚠️ Failed to load profile {site_name}: {e}")
        
        return profiles
    
    def handle_web_command(self, command: str) -> Dict[str, Any]:
        """
        Handle web automation command using lightweight methods
        """
        
        print(f"🌐 Handling: {command}")
        
        try:
            # Parse the command using GPT
            plan = self._plan_web_task(command)
            
            if not plan:
                return {
                    "success": False,
                    "error": "Could not understand web command",
                    "command": command
                }
            
            # Execute based on task type
            task_type = plan.get('task_type', 'unknown')
            
            if task_type == 'search':
                return self._handle_search_task(plan, command)
            elif task_type == 'navigation':
                return self._handle_navigation_task(plan, command)
            elif task_type == 'extraction':
                return self._handle_extraction_task(plan, command)
            else:
                return self._handle_generic_task(plan, command)
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "command": command,
                "timestamp": datetime.now().isoformat()
            }
    
    def _plan_web_task(self, command: str) -> Optional[Dict]:
        """Plan web task using GPT"""
        
        prompt = f"""
Analyze this web automation command and create a simple execution plan.

COMMAND: "{command}"

AVAILABLE SITES: {list(self.web_profiles.keys())}

Create a JSON plan:
{{
    "task_type": "search|navigation|extraction|form_filling",
    "target_site": "website domain",
    "search_query": "query if searching",
    "target_url": "full URL to open",
    "lightweight_approach": "how to handle this with system browser",
    "expected_result": "what should happen"
}}

Focus on what can be done by opening URLs in the system browser.
"""
        
        try:
            response = call_gpt_system(prompt)
            
            # Clean and parse response
            response = response.strip()
            if response.startswith('```json'):
                response = response[7:]
            if response.endswith('```'):
                response = response[:-3]
            
            return json.loads(response.strip())
            
        except Exception as e:
            print(f"❌ Planning failed: {e}")
            return None
    
    def _handle_search_task(self, plan: Dict, command: str) -> Dict[str, Any]:
        """Handle search tasks"""
        
        target_site = plan.get('target_site', '').lower()
        query = plan.get('search_query', '')
        
        if 'google' in target_site:
            search_url = f"https://google.com/search?q={query.replace(' ', '+')}"
        elif 'youtube' in target_site:
            search_url = f"https://youtube.com/results?search_query={query.replace(' ', '+')}"
        elif 'github' in target_site:
            search_url = f"https://github.com/search?q={query.replace(' ', '+')}"
        else:
            search_url = f"https://google.com/search?q={query.replace(' ', '+')}+site:{target_site}"
        
        return self._open_url(search_url, f"Search for '{query}' on {target_site}")
    
    def _handle_navigation_task(self, plan: Dict, command: str) -> Dict[str, Any]:
        """Handle navigation tasks"""
        
        target_url = plan.get('target_url', '')
        
        if not target_url:
            target_site = plan.get('target_site', '')
            if target_site:
                if not target_site.startswith('http'):
                    target_url = f"https://{target_site}"
                else:
                    target_url = target_site
        
        if target_url:
            return self._open_url(target_url, f"Navigate to {target_url}")
        else:
            return {
                "success": False,
                "error": "Could not determine target URL",
                "command": command
            }
    
    def _handle_extraction_task(self, plan: Dict, command: str) -> Dict[str, Any]:
        """Handle data extraction tasks"""
        
        target_url = plan.get('target_url', '')
        
        if target_url:
            # Open the page and provide guidance
            result = self._open_url(target_url, f"Extract data from {target_url}")
            
            if result.get('success'):
                result['extraction_guidance'] = "Page opened in browser. Look for the data you need."
                result['lightweight_note'] = "Full automation requires selenium installation"
            
            return result
        else:
            return {
                "success": False,
                "error": "Need target URL for data extraction",
                "command": command
            }
    
    def _handle_generic_task(self, plan: Dict, command: str) -> Dict[str, Any]:
        """Handle generic web tasks"""
        
        target_url = plan.get('target_url', '')
        approach = plan.get('lightweight_approach', '')
        
        if target_url:
            return self._open_url(target_url, approach or command)
        else:
            return {
                "success": False,
                "error": f"Cannot handle task type: {plan.get('task_type', 'unknown')}",
                "command": command,
                "suggestion": "Install selenium for full automation"
            }
    
    def _open_url(self, url: str, description: str) -> Dict[str, Any]:
        """Open URL in system browser"""
        
        try:
            print(f"🌐 Opening: {url}")
            print(f"   Purpose: {description}")
            
            # Open in default browser
            webbrowser.open(url)
            
            # Log the action
            action_record = {
                "timestamp": datetime.now().isoformat(),
                "url": url,
                "description": description,
                "method": "system_browser"
            }
            
            self.session_history.append(action_record)
            
            return {
                "success": True,
                "url_opened": url,
                "description": description,
                "method": "system_browser",
                "note": "Page opened in your default browser",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to open URL: {e}",
                "url": url
            }
    
    def get_session_history(self) -> List[Dict]:
        """Get current session history"""
        return self.session_history
    
    def clear_session_history(self):
        """Clear session history"""
        self.session_history = []
        print("🗑️ Session history cleared")

def lightweight_web_automation(command: str) -> Dict[str, Any]:
    """
    Main function for lightweight web automation
    """
    
    automation = LightweightWebAutomation()
    return automation.handle_web_command(command)

def search_web_lightweight(query: str, site: str = "google") -> Dict[str, Any]:
    """Simplified search function"""
    
    command = f"Search {site} for {query}"
    return lightweight_web_automation(command)

def open_website(url: str) -> Dict[str, Any]:
    """Open a website in the browser"""
    
    command = f"Navigate to {url}"
    return lightweight_web_automation(command)

# Test the lightweight automation
if __name__ == "__main__":
    print("🧪 Testing Lightweight Web Automation...")
    
    test_commands = [
        "Search Google for Python tutorials",
        "Go to YouTube",
        "Search YouTube for machine learning",
        "Navigate to github.com"
    ]
    
    automation = LightweightWebAutomation()
    
    for command in test_commands:
        print(f"\n🧪 Testing: {command}")
        result = automation.handle_web_command(command)
        
        if result.get('success'):
            print(f"✅ Success: {result.get('description', 'Command executed')}")
        else:
            print(f"❌ Failed: {result.get('error', 'Unknown error')}")
        
        print(f"   URL: {result.get('url_opened', 'N/A')}")
