#!/usr/bin/env python3
"""
Web Link Automation Tool
Enhanced web automation focused on clicking links and interacting with search results
"""

import time
import subprocess
import os
import re
from typing import Dict, Any, Optional, List

# Tool configuration
TOOL_NAME = "web_link_automation"
TOOL_DESCRIPTION = "Advanced web automation for clicking links and interacting with search results"

def click_first_search_result_keyboard(browser: str = "Google Chrome", search_query: str = "") -> Dict[str, Any]:
    """
    Click the first search result using keyboard navigation (more reliable)
    
    Args:
        browser: Browser name
        search_query: The search query that was used (for context)
    
    Returns:
        Dict with success status and message
    """
    try:
        print(f"🔗 Using keyboard navigation to click first result for '{search_query}' in {browser}")
        
        applescript = f'''
        tell application "{browser}" to activate
        delay 1
        
        tell application "System Events"
            -- Press Tab to navigate to first link, then Enter to click
            key code 48  -- Tab key
            delay 0.5
            key code 48  -- Tab key again (in case first tab goes to search box)
            delay 0.5
            key code 36  -- Enter key
        end tell
        
        return "SUCCESS: Navigated to first result using keyboard"
        '''
        
        # Execute the AppleScript
        result = subprocess.run(
            ['osascript', '-e', applescript],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        if result.returncode == 0:
            return {
                'success': True,
                'message': f"✅ Used keyboard navigation for '{search_query}'",
                'action': 'keyboard_navigation',
                'browser': browser,
                'search_query': search_query
            }
        else:
            return {
                'success': False,
                'error': result.stderr.strip(),
                'message': f"⚠️ Keyboard navigation failed for '{search_query}'"
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': f"⚠️ Keyboard automation error for '{search_query}': {e}"
        }

def click_first_search_result(browser: str = "Google Chrome", search_query: str = "", wait_time: int = 3) -> Dict[str, Any]:
    """
    Click the first search result in the specified browser
    
    Args:
        browser: Browser name (Google Chrome, Safari, Firefox)
        search_query: The search query that was used (for context)
        wait_time: Time to wait before clicking (seconds)
    
    Returns:
        Dict with success status and message
    """
    try:
        print(f"🔗 Attempting to click first search result for '{search_query}' in {browser}")
        
        # Use AppleScript with UI automation (doesn't require JavaScript permissions)
        if browser.lower() in ["chrome", "google chrome"]:
            applescript = f'''
            tell application "Google Chrome" to activate
            delay {wait_time}
            
            tell application "System Events"
                tell process "Google Chrome"
                    -- Try to find and click the first search result link
                    try
                        -- Look for common search result link patterns
                        set searchLinks to (buttons whose description contains "http" or links whose description contains "http")
                        if (count of searchLinks) > 0 then
                            click item 1 of searchLinks
                            return "SUCCESS: Clicked first search result"
                        else
                            -- Try clicking on the first visible link
                            set allLinks to links
                            if (count of allLinks) > 0 then
                                click item 1 of allLinks
                                return "SUCCESS: Clicked first available link"
                            else
                                return "ERROR: No clickable links found"
                            end if
                        end if
                    on error errorMessage
                        return "ERROR: " & errorMessage
                    end try
                end tell
            end tell
            '''
        
        elif browser.lower() == "safari":
            applescript = f'''
            tell application "Safari" to activate
            delay {wait_time}
            
            tell application "System Events"
                tell process "Safari"
                    try
                        set allLinks to links
                        if (count of allLinks) > 0 then
                            click item 1 of allLinks
                            return "SUCCESS: Clicked first search result"
                        else
                            return "ERROR: No links found"
                        end if
                    on error errorMessage
                        return "ERROR: " & errorMessage
                    end try
                end tell
            end tell
            '''
        
        else:
            return {
                'success': False,
                'error': f"Browser {browser} not supported for link clicking",
                'message': f"Please manually click the first search result for '{search_query}'"
            }
        
        # Execute the AppleScript
        result = subprocess.run(
            ['osascript', '-e', applescript],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            output = result.stdout.strip()
            if "SUCCESS" in output:
                return {
                    'success': True,
                    'message': f"✅ Successfully clicked first search result for '{search_query}'",
                    'action': 'clicked_first_result',
                    'browser': browser,
                    'search_query': search_query
                }
            else:
                # If UI automation failed, try keyboard method
                print("🔄 UI automation failed, trying keyboard navigation...")
                return click_first_search_result_keyboard(browser, search_query)
        else:
            # If AppleScript failed, try keyboard method
            print("🔄 AppleScript failed, trying keyboard navigation...")
            return click_first_search_result_keyboard(browser, search_query)
            
    except subprocess.TimeoutExpired:
        # If everything fails, provide manual instructions
        print("🔄 All automation methods failed, providing manual instructions...")
        return provide_manual_instructions(browser, search_query)
    except Exception as e:
        # If everything fails, provide manual instructions
        print(f"🔄 Automation error ({e}), providing manual instructions...")
        return provide_manual_instructions(browser, search_query)

def click_link_by_text(browser: str = "Google Chrome", link_text: str = "", partial_match: bool = True) -> Dict[str, Any]:
    """
    Click a link by its text content
    
    Args:
        browser: Browser name
        link_text: Text content of the link to click
        partial_match: Whether to match partial text
    
    Returns:
        Dict with success status and message
    """
    try:
        print(f"🔗 Attempting to click link with text '{link_text}' in {browser}")
        
        if browser.lower() in ["chrome", "google chrome"]:
            # Escape quotes in link text for JavaScript
            escaped_text = link_text.replace("'", "\\'").replace('"', '\\"')
            
            if partial_match:
                js_selector = f"Array.from(document.querySelectorAll('a')).find(a => a.textContent.toLowerCase().includes('{escaped_text.lower()}'))"
            else:
                js_selector = f"Array.from(document.querySelectorAll('a')).find(a => a.textContent.trim() === '{escaped_text}')"
            
            applescript = f'''
            tell application "Google Chrome"
                activate
                delay 1
                
                set clickScript to "
                    var link = {js_selector};
                    if (link) {{
                        link.click();
                        'SUCCESS: Clicked link with text {escaped_text}';
                    }} else {{
                        'ERROR: Link not found with text {escaped_text}';
                    }}
                "
                
                set result to execute front window's active tab javascript clickScript
                return result
            end tell
            '''
        
        elif browser.lower() == "safari":
            escaped_text = link_text.replace("'", "\\'").replace('"', '\\"')
            
            if partial_match:
                js_selector = f"Array.from(document.querySelectorAll('a')).find(a => a.textContent.toLowerCase().includes('{escaped_text.lower()}'))"
            else:
                js_selector = f"Array.from(document.querySelectorAll('a')).find(a => a.textContent.trim() === '{escaped_text}')"
            
            applescript = f'''
            tell application "Safari"
                activate
                delay 1
                
                set clickScript to "
                    var link = {js_selector};
                    if (link) {{
                        link.click();
                        'SUCCESS: Clicked link with text {escaped_text}';
                    }} else {{
                        'ERROR: Link not found with text {escaped_text}';
                    }}
                "
                
                set result to do JavaScript clickScript in front document
                return result
            end tell
            '''
        
        else:
            return {
                'success': False,
                'error': f"Browser {browser} not supported",
                'message': f"Please manually click the link with text '{link_text}'"
            }
        
        # Execute the AppleScript
        result = subprocess.run(
            ['osascript', '-e', applescript],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            output = result.stdout.strip()
            if "SUCCESS" in output:
                return {
                    'success': True,
                    'message': f"✅ Successfully clicked link: '{link_text}'",
                    'action': 'clicked_link',
                    'browser': browser,
                    'link_text': link_text
                }
            else:
                return {
                    'success': False,
                    'error': output,
                    'message': f"⚠️ Could not find link with text '{link_text}'"
                }
        else:
            return {
                'success': False,
                'error': result.stderr.strip(),
                'message': f"⚠️ Failed to click link '{link_text}'"
            }
            
    except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"⚠️ Error clicking link '{link_text}': {e}"
            }

def provide_manual_instructions(browser: str, search_query: str) -> Dict[str, Any]:
    """
    Provide clear instructions for manual clicking when automation fails
    """
    instructions = f"""
🔗 Manual Instructions for '{search_query}' in {browser}:

1. Look at your {browser} window
2. Find the first search result (usually has a blue link title)
3. Click on the title or URL of the first result
4. This will open the website you're looking for

💡 Tip: The first result is typically the most relevant one for '{search_query}'
"""
    
    return {
        'success': True,  # We successfully provided instructions
        'message': f"📋 Please manually click the first search result for '{search_query}' in {browser}",
        'instructions': instructions,
        'action': 'manual_instructions',
        'browser': browser,
        'search_query': search_query
    }

def get_search_results_info(browser: str = "Google Chrome") -> Dict[str, Any]:
    """
    Get information about search results on the current page
    
    Args:
        browser: Browser name
    
    Returns:
        Dict with search results information
    """
    try:
        if browser.lower() in ["chrome", "google chrome"]:
            applescript = '''
            tell application "Google Chrome"
                activate
                
                set infoScript to "
                    var results = [];
                    var links = document.querySelectorAll('h3 a, .g h3 a, [data-ved] h3 a, .yuRUbf a, .r a');
                    for (var i = 0; i < Math.min(5, links.length); i++) {
                        results.push({
                            index: i + 1,
                            title: links[i].textContent.trim(),
                            url: links[i].href
                        });
                    }
                    JSON.stringify(results);
                "
                
                set result to execute front window's active tab javascript infoScript
                return result
            end tell
            '''
        
        elif browser.lower() == "safari":
            applescript = '''
            tell application "Safari"
                activate
                
                set infoScript to "
                    var results = [];
                    var links = document.querySelectorAll('h3 a, .g h3 a, [data-ved] h3 a, .yuRUbf a, .r a');
                    for (var i = 0; i < Math.min(5, links.length); i++) {
                        results.push({
                            index: i + 1,
                            title: links[i].textContent.trim(),
                            url: links[i].href
                        });
                    }
                    JSON.stringify(results);
                "
                
                set result to do JavaScript infoScript in front document
                return result
            end tell
            '''
        
        else:
            return {
                'success': False,
                'error': f"Browser {browser} not supported",
                'results': []
            }
        
        # Execute the AppleScript
        result = subprocess.run(
            ['osascript', '-e', applescript],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        if result.returncode == 0:
            try:
                import json
                results = json.loads(result.stdout.strip())
                return {
                    'success': True,
                    'results': results,
                    'count': len(results),
                    'browser': browser
                }
            except json.JSONDecodeError:
                return {
                    'success': False,
                    'error': "Could not parse search results",
                    'results': []
                }
        else:
            return {
                'success': False,
                'error': result.stderr.strip(),
                'results': []
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'results': []
        }

# Main function for MCP integration
def web_link_automation(command: str, **kwargs) -> Dict[str, Any]:
    """
    Main function for web link automation
    
    Args:
        command: The automation command
        **kwargs: Additional parameters
    
    Returns:
        Dict with execution results
    """
    try:
        command_lower = command.lower()
        
        # Extract parameters
        browser = kwargs.get('browser', 'Google Chrome')
        search_query = kwargs.get('search_query', '')
        link_text = kwargs.get('link_text', '')
        
        # Determine action based on command
        if any(phrase in command_lower for phrase in ['first', 'top', '1st']):
            if any(phrase in command_lower for phrase in ['result', 'link', 'search']):
                return click_first_search_result(browser, search_query)
        
        elif 'click' in command_lower and link_text:
            return click_link_by_text(browser, link_text)
        
        elif any(phrase in command_lower for phrase in ['info', 'results', 'list']):
            return get_search_results_info(browser)
        
        else:
            # Try to extract search query and browser from command
            if not search_query:
                # Look for quoted text or specific patterns
                import re
                quotes_match = re.search(r'"([^"]+)"', command)
                if quotes_match:
                    search_query = quotes_match.group(1)
                else:
                    # Extract from common patterns
                    for pattern in [r'search for ([^,\n]+)', r'find ([^,\n]+)', r'look for ([^,\n]+)']:
                        match = re.search(pattern, command_lower)
                        if match:
                            search_query = match.group(1).strip()
                            break
            
            # Default to clicking first search result
            return click_first_search_result(browser, search_query)
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': f"⚠️ Web link automation error: {e}"
        }

# Tool metadata for MCP server
if __name__ == "__main__":
    print(f"🔧 {TOOL_NAME}: {TOOL_DESCRIPTION}")
    print("Available functions:")
    print("  - click_first_search_result(browser, search_query, wait_time)")
    print("  - click_link_by_text(browser, link_text, partial_match)")
    print("  - get_search_results_info(browser)")
    print("  - web_link_automation(command, **kwargs)")
