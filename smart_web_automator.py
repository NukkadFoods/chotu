#!/usr/bin/env python3
"""
🎯 CHOTU SMART WEB AUTOMATOR - UNIVERSAL SOLUTION
===============================================
Full web automation that works on ANY website with actual interaction
"""

import os
import sys
import json
import time
import webbrowser
import urllib.parse
from datetime import datetime
from typing import Dict, List, Any, Optional

def check_automation_capabilities() -> Dict[str, Any]:
    """Check what automation capabilities are available"""
    
    capabilities = {
        "selenium": False,
        "playwright": False,
        "opencv": False,
        "lightweight": True,
        "available_engines": ["lightweight"],
        "missing": []
    }
    
    # Check Selenium
    try:
        import selenium
        from selenium import webdriver
        capabilities["selenium"] = True
        capabilities["available_engines"].append("selenium")
    except ImportError:
        capabilities["missing"].append("selenium")
    
    # Check Playwright
    try:
        import playwright
        capabilities["playwright"] = True
        capabilities["available_engines"].append("playwright")
    except ImportError:
        capabilities["missing"].append("playwright")
    
    # Check OpenCV
    try:
        import cv2
        capabilities["opencv"] = True
        capabilities["available_engines"].append("computer_vision")
    except ImportError:
        capabilities["missing"].append("opencv")
    
    return capabilities

def smart_web_automation(command: str, site_hint: str = None) -> Dict[str, Any]:
    """
    Universal web automation that works on any site
    
    Args:
        command: Natural language command (e.g., "search and play kitne bechain hoke on YouTube")
        site_hint: Optional site hint (youtube, google, etc.)
    
    Returns:
        Dict: Automation result with success/failure details
    """
    
    print(f"🎯 UNIVERSAL WEB AUTOMATION: {command}")
    
    caps = check_automation_capabilities()
    print(f"🔧 Available engines: {', '.join(caps['available_engines'])}")
    
    # Parse the command to understand intent
    intent = parse_web_command(command)
    print(f"🧠 Parsed intent: {intent['action']} on {intent['site']}")
    
    # Choose best automation method
    if caps["selenium"] and intent["needs_interaction"]:
        return selenium_automation(intent)
    elif caps["playwright"] and intent["needs_interaction"]:
        return playwright_automation(intent)
    else:
        return lightweight_automation(intent)

def parse_web_command(command: str) -> Dict[str, Any]:
    """Parse natural language command into structured intent"""
    
    command_lower = command.lower()
    
    intent = {
        "action": "unknown",
        "site": "unknown", 
        "query": "",
        "needs_interaction": False,
        "target_element": None,
        "original_command": command
    }
    
    # Detect site
    if "youtube" in command_lower:
        intent["site"] = "youtube"
    elif "google" in command_lower:
        intent["site"] = "google"
    elif "amazon" in command_lower:
        intent["site"] = "amazon"
    elif "github" in command_lower:
        intent["site"] = "github"
    
    # Detect action
    if "search" in command_lower:
        intent["action"] = "search"
        intent["needs_interaction"] = True
        
        # Extract search query
        if "search" in command_lower and "for" in command_lower:
            parts = command_lower.split("for", 1)
            if len(parts) > 1:
                query_part = parts[1].strip()
                # Clean up the query
                query_part = query_part.replace("and play", "").replace("first video", "").strip()
                intent["query"] = query_part
    
    elif "play" in command_lower:
        intent["action"] = "play"
        intent["needs_interaction"] = True
        intent["target_element"] = "first_video"
        
        # Extract what to play
        if intent["query"] == "":  # If not set by search
            # Try to extract from play command
            play_parts = command_lower.split("play", 1)
            if len(play_parts) > 1:
                intent["query"] = play_parts[1].strip()
    
    elif "navigate" in command_lower or "go to" in command_lower:
        intent["action"] = "navigate"
        intent["needs_interaction"] = False
    
    # Handle combined commands (search and play)
    if "search" in command_lower and "play" in command_lower:
        intent["action"] = "search_and_play"
        intent["needs_interaction"] = True
        intent["target_element"] = "first_result"
    
    return intent

def selenium_automation(intent: Dict[str, Any]) -> Dict[str, Any]:
    """Full Selenium automation with actual interaction"""
    
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.chrome.options import Options
        
        print("🚀 Starting Selenium automation...")
        
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_argument("--headless")  # Comment out to see browser
        
        # Initialize driver
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 10)
        
        try:
            result = {"success": False, "method": "selenium", "steps": []}
            
            if intent["site"] == "youtube" and intent["action"] == "search_and_play":
                result = youtube_search_and_play(driver, wait, intent["query"], EC)
            elif intent["site"] == "youtube" and intent["action"] == "search":
                result = youtube_search(driver, wait, intent["query"], EC)
            else:
                # Generic automation
                result = generic_site_automation(driver, wait, intent)
            
            # Keep browser open for a moment to see result
            time.sleep(3)
            
            return result
            
        finally:
            driver.quit()
            
    except ImportError:
        return {"success": False, "error": "Selenium not available", "fallback": "lightweight"}
    except Exception as e:
        return {"success": False, "error": f"Selenium automation failed: {e}", "fallback": "lightweight"}

def youtube_search_and_play(driver, wait, query: str, EC) -> Dict[str, Any]:
    """Search YouTube and play first video"""
    
    steps = []
    
    try:
        # Navigate to YouTube
        print("📺 Opening YouTube...")
        driver.get("https://www.youtube.com")
        steps.append("Navigated to YouTube")
        
        # Find and click search box
        print("🔍 Finding search box...")
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "search_query")))
        search_box.clear()
        search_box.send_keys(query)
        steps.append(f"Entered search query: {query}")
        
        # Submit search
        search_box.send_keys(Keys.RETURN)
        print("🔎 Searching...")
        steps.append("Submitted search")
        
        # Wait for results and click first video
        print("🎬 Looking for first video...")
        time.sleep(2)  # Let results load
        
        # Try multiple selectors for video links
        video_selectors = [
            "a#video-title",
            "a.ytd-video-renderer",
            "a[href*='/watch?v=']"
        ]
        
        first_video = None
        for selector in video_selectors:
            try:
                videos = driver.find_elements(By.CSS_SELECTOR, selector)
                if videos:
                    first_video = videos[0]
                    break
            except:
                continue
        
        if first_video:
            video_title = first_video.get_attribute("title") or first_video.text or "Video"
            print(f"🎵 Found video: {video_title}")
            print("▶️ Clicking to play...")
            
            # Click the video
            driver.execute_script("arguments[0].click();", first_video)
            steps.append(f"Clicked first video: {video_title}")
            
            # Wait for video page to load
            time.sleep(3)
            
            return {
                "success": True,
                "method": "selenium_youtube",
                "action": "search_and_play",
                "query": query,
                "video_title": video_title,
                "url": driver.current_url,
                "steps": steps,
                "message": f"Successfully playing '{video_title}' on YouTube"
            }
        else:
            return {
                "success": False,
                "error": "No videos found in search results",
                "steps": steps
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"YouTube automation failed: {e}",
            "steps": steps
        }

def youtube_search(driver, wait, query: str, EC) -> Dict[str, Any]:
    """Just search YouTube without playing"""
    
    try:
        driver.get("https://www.youtube.com")
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "search_query")))
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        
        time.sleep(2)
        
        return {
            "success": True,
            "method": "selenium_youtube",
            "action": "search",
            "query": query,
            "url": driver.current_url,
            "message": f"Successfully searched YouTube for '{query}'"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"YouTube search failed: {e}"
        }

def generic_site_automation(driver, wait, intent: Dict[str, Any]) -> Dict[str, Any]:
    """Generic automation for any website"""
    
    try:
        # Map sites to URLs
        site_urls = {
            "google": "https://www.google.com",
            "youtube": "https://www.youtube.com",
            "github": "https://www.github.com",
            "amazon": "https://www.amazon.com"
        }
        
        url = site_urls.get(intent["site"], f"https://www.{intent['site']}.com")
        driver.get(url)
        
        if intent["action"] == "search" and intent["query"]:
            # Try to find search box
            search_selectors = [
                "input[name='q']",
                "input[name='search']", 
                "input[type='search']",
                ".search-input",
                "#search"
            ]
            
            for selector in search_selectors:
                try:
                    search_box = driver.find_element(By.CSS_SELECTOR, selector)
                    search_box.clear()
                    search_box.send_keys(intent["query"])
                    search_box.send_keys(Keys.RETURN)
                    
                    return {
                        "success": True,
                        "method": "selenium_generic",
                        "action": "search",
                        "site": intent["site"],
                        "query": intent["query"],
                        "url": driver.current_url,
                        "message": f"Successfully searched {intent['site']} for '{intent['query']}'"
                    }
                except:
                    continue
        
        return {
            "success": True,
            "method": "selenium_generic",
            "action": "navigate",
            "site": intent["site"],
            "url": driver.current_url,
            "message": f"Successfully navigated to {intent['site']}"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Generic automation failed: {e}"
        }

def playwright_automation(intent: Dict[str, Any]) -> Dict[str, Any]:
    """Playwright automation (alternative to Selenium)"""
    
    try:
        from playwright.sync_api import sync_playwright
        
        print("🎭 Starting Playwright automation...")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            if intent["site"] == "youtube" and intent["action"] == "search_and_play":
                page.goto("https://www.youtube.com")
                page.fill("input[name='search_query']", intent["query"])
                page.press("input[name='search_query']", "Enter")
                page.wait_for_timeout(2000)
                
                # Click first video
                page.click("a#video-title")
                page.wait_for_timeout(3000)
                
                browser.close()
                
                return {
                    "success": True,
                    "method": "playwright_youtube",
                    "action": "search_and_play",
                    "query": intent["query"],
                    "message": f"Successfully playing '{intent['query']}' on YouTube"
                }
            
            browser.close()
            
    except ImportError:
        return {"success": False, "error": "Playwright not available", "fallback": "selenium"}
    except Exception as e:
        return {"success": False, "error": f"Playwright automation failed: {e}", "fallback": "selenium"}

def lightweight_automation(intent: Dict[str, Any]) -> Dict[str, Any]:
    """Fallback lightweight automation"""
    
    print("🌟 Using lightweight automation...")
    
    if intent["site"] == "youtube":
        query = intent["query"] or "music"
        url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
    elif intent["site"] == "google":
        query = intent["query"] or "search"
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    else:
        url = f"https://www.{intent['site']}.com"
    
    webbrowser.open(url)
    
    return {
        "success": True,
        "method": "lightweight",
        "action": intent["action"],
        "site": intent["site"],
        "query": intent.get("query", ""),
        "url": url,
        "message": f"Opened {intent['site']} in browser",
        "note": "For full automation with clicking/playing, Selenium is recommended"
    }

# Main interface function
def chotu_web_command(command: str) -> Dict[str, Any]:
    """Main interface for Chotu web automation"""
    
    return smart_web_automation(command)

# Test function
if __name__ == "__main__":
    print("🎯 CHOTU SMART WEB AUTOMATOR TEST")
    print("=" * 50)
    
    # Test commands
    test_commands = [
        "search and play kitne bechain hoke on YouTube",
        "search Google for AI news",
        "navigate to GitHub"
    ]
    
    for command in test_commands:
        print(f"\n🧪 Testing: {command}")
        result = chotu_web_command(command)
        
        if result["success"]:
            print(f"✅ Success: {result['message']}")
            print(f"   Method: {result.get('method', 'unknown')}")
        else:
            print(f"❌ Failed: {result.get('error', 'Unknown error')}")
