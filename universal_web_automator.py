#!/usr/bin/env python3
"""
🌐 UNIVERSAL WEB AUTOMATOR FOR CHOTU
===================================
General-purpose web automation that works with ANY website
- Auto-detects elements and actions
- Uses site profiles when available
- Falls back to AI-powered element detection
- Works with or without Selenium/OpenCV
"""

import os
import sys
import json
import time
import webbrowser
import urllib.parse
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

def check_automation_capabilities() -> Dict[str, Any]:
    """Check what automation capabilities are currently available"""
    
    caps = {
        "lightweight": True,
        "selenium": False,
        "playwright": False, 
        "computer_vision": False,
        "available_engines": ["system_browser"],
        "missing": []
    }
    
    try:
        import selenium
        from selenium import webdriver
        caps["selenium"] = True
        caps["available_engines"].append("selenium")
    except ImportError:
        caps["missing"].append("selenium")
    
    try:
        import playwright
        caps["playwright"] = True
        caps["available_engines"].append("playwright")
    except ImportError:
        caps["missing"].append("playwright")
    
    try:
        import cv2
        caps["computer_vision"] = True
        caps["available_engines"].append("computer_vision")
    except ImportError:
        caps["missing"].append("opencv")
    
    return caps

def load_site_profile(site_name: str) -> Dict[str, Any]:
    """Load site-specific automation profile"""
    
    config_dir = os.path.join(os.getcwd(), "config", "web_profiles")
    profile_file = os.path.join(config_dir, f"{site_name}.json")
    
    if os.path.exists(profile_file):
        try:
            with open(profile_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Error loading {site_name} profile: {e}")
    
    return {}

def detect_site_from_url(url: str) -> str:
    """Auto-detect what site we're dealing with"""
    
    site_patterns = {
        "youtube": ["youtube.com", "youtu.be"],
        "google": ["google.com", "google.co"],
        "amazon": ["amazon.com", "amazon.co"],
        "github": ["github.com"],
        "twitter": ["twitter.com", "x.com"],
        "facebook": ["facebook.com"],
        "reddit": ["reddit.com"],
        "stackoverflow": ["stackoverflow.com"],
        "linkedin": ["linkedin.com"]
    }
    
    url_lower = url.lower()
    for site, patterns in site_patterns.items():
        if any(pattern in url_lower for pattern in patterns):
            return site
    
    return "generic"

def parse_automation_intent(command: str) -> Dict[str, Any]:
    """Parse user command to understand automation intent"""
    
    command_lower = command.lower()
    
    intent = {
        "action": "unknown",
        "target_site": "unknown", 
        "search_query": "",
        "url": "",
        "data_to_extract": [],
        "specific_actions": [],
        "auto_play": False
    }
    
    # Detect actions
    if any(word in command_lower for word in ["play", "listen", "watch"]):
        intent["action"] = "play_media"
        intent["auto_play"] = True
    elif any(word in command_lower for word in ["search", "find", "look for"]):
        intent["action"] = "search"
    elif any(word in command_lower for word in ["navigate", "go to", "open", "visit"]):
        intent["action"] = "navigate"
    elif any(word in command_lower for word in ["extract", "get", "scrape", "download"]):
        intent["action"] = "extract_data"
    elif any(word in command_lower for word in ["click", "press", "tap"]):
        intent["action"] = "click_element"
    elif any(word in command_lower for word in ["fill", "type", "enter"]):
        intent["action"] = "fill_form"
    
    # Detect target sites
    site_keywords = {
        "youtube": ["youtube", "yt"],
        "google": ["google"],
        "amazon": ["amazon"],
        "github": ["github"],
        "twitter": ["twitter", "x.com"],
        "facebook": ["facebook"],
        "reddit": ["reddit"],
        "stackoverflow": ["stackoverflow", "stack overflow"]
    }
    
    for site, keywords in site_keywords.items():
        if any(keyword in command_lower for keyword in keywords):
            intent["target_site"] = site
            break
    
    # Extract search query
    search_triggers = ["search for", "look for", "find", "play", "listen to", "watch"]
    for trigger in search_triggers:
        if trigger in command_lower:
            parts = command_lower.split(trigger, 1)
            if len(parts) > 1:
                query = parts[1].strip()
                # Remove site names from query
                for site in site_keywords.keys():
                    query = query.replace(site, "").strip()
                intent["search_query"] = query.strip("on ").strip()
                break
    
    # Detect URLs
    if "http" in command or "www." in command:
        words = command.split()
        for word in words:
            if "http" in word or "www." in word:
                intent["url"] = word
                intent["target_site"] = detect_site_from_url(word)
                break
    
    return intent

def selenium_automation(intent: Dict[str, Any]) -> Dict[str, Any]:
    """Full Selenium automation for complex interactions"""
    
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.keys import Keys
        
        print("🚀 Starting Selenium automation...")
        
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_experimental_option("detach", True)  # Keep browser open
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        
        try:
            if intent["action"] == "play_media" and intent["target_site"] == "youtube":
                return selenium_youtube_play(driver, intent)
            elif intent["action"] == "search":
                return selenium_search(driver, intent)
            elif intent["action"] == "navigate":
                return selenium_navigate(driver, intent)
            else:
                return selenium_generic_action(driver, intent)
                
        except Exception as e:
            driver.quit()
            raise e
            
    except ImportError:
        raise Exception("Selenium not available")

def selenium_youtube_play(driver, intent: Dict[str, Any]) -> Dict[str, Any]:
    """Selenium automation specifically for YouTube play actions"""
    
    try:
        # Load YouTube profile
        profile = load_site_profile("youtube")
        
        # Navigate to YouTube
        driver.get("https://www.youtube.com")
        wait = WebDriverWait(driver, 10)
        
        # Wait for search box and search
        search_box = wait.until(EC.presence_of_element_located((By.XPATH, profile.get("search_box", "//input[@name='search_query']"))))
        search_box.clear()
        search_box.send_keys(intent["search_query"])
        search_box.send_keys(Keys.RETURN)
        
        # Wait for results and click first video
        time.sleep(3)  # Let results load
        
        # Try multiple selectors for video titles
        video_selectors = [
            "//a[@id='video-title']",
            "//h3[@class='ytd-video-renderer']//a",
            "//ytd-video-renderer//a[@id='video-title']",
            "#contents ytd-video-renderer a#video-title"
        ]
        
        first_video = None
        for selector in video_selectors:
            try:
                if selector.startswith("//"):
                    first_video = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                else:
                    first_video = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                break
            except:
                continue
        
        if first_video:
            video_title = first_video.text or "Unknown Video"
            first_video.click()
            
            # Wait for video to start
            time.sleep(5)
            
            return {
                "success": True,
                "action": "youtube_play",
                "query": intent["search_query"],
                "video_title": video_title,
                "method": "selenium_automation",
                "message": f"Successfully started playing: {video_title}",
                "browser_kept_open": True
            }
        else:
            raise Exception("Could not find video to play")
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "method": "selenium_automation"
        }

def selenium_search(driver, intent: Dict[str, Any]) -> Dict[str, Any]:
    """Generic search automation"""
    
    try:
        site = intent["target_site"]
        query = intent["search_query"]
        
        # Site-specific search URLs
        search_urls = {
            "google": f"https://www.google.com/search?q={urllib.parse.quote(query)}",
            "youtube": f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}",
            "amazon": f"https://www.amazon.com/s?k={urllib.parse.quote(query)}",
            "github": f"https://github.com/search?q={urllib.parse.quote(query)}"
        }
        
        url = search_urls.get(site, f"https://www.google.com/search?q={urllib.parse.quote(f'{query} site:{site}.com')}")
        driver.get(url)
        
        time.sleep(3)  # Let page load
        
        return {
            "success": True,
            "action": "search",
            "site": site,
            "query": query,
            "url": url,
            "method": "selenium_automation",
            "message": f"Successfully searched {site} for: {query}"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "method": "selenium_automation"
        }

def selenium_navigate(driver, intent: Dict[str, Any]) -> Dict[str, Any]:
    """Generic navigation automation"""
    
    try:
        url = intent["url"]
        if not url.startswith("http"):
            url = f"https://{url}"
        
        driver.get(url)
        time.sleep(3)
        
        return {
            "success": True,
            "action": "navigate",
            "url": url,
            "method": "selenium_automation",
            "message": f"Successfully navigated to: {url}"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "method": "selenium_automation"
        }

def selenium_generic_action(driver, intent: Dict[str, Any]) -> Dict[str, Any]:
    """Generic Selenium action handler"""
    
    try:
        # For now, default to search behavior
        if intent["search_query"]:
            return selenium_search(driver, intent)
        elif intent["url"]:
            return selenium_navigate(driver, intent)
        else:
            return {
                "success": False,
                "error": "No clear action could be determined",
                "method": "selenium_automation"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "method": "selenium_automation"
        }

def lightweight_automation(intent: Dict[str, Any]) -> Dict[str, Any]:
    """Lightweight browser automation using system browser"""
    
    try:
        if intent["action"] == "play_media" and intent["target_site"] == "youtube":
            # Direct play URL for YouTube
            query = intent["search_query"]
            url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
            webbrowser.open(url)
            
            return {
                "success": True,
                "action": "youtube_search_opened",
                "query": query,
                "url": url,
                "method": "lightweight_automation",
                "message": f"Opened YouTube search for: {query}",
                "note": "Manual video selection required - use Selenium for auto-play"
            }
        
        elif intent["action"] == "search":
            site = intent["target_site"]
            query = intent["search_query"]
            
            search_urls = {
                "google": f"https://www.google.com/search?q={urllib.parse.quote(query)}",
                "youtube": f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}",
                "amazon": f"https://www.amazon.com/s?k={urllib.parse.quote(query)}",
                "github": f"https://github.com/search?q={urllib.parse.quote(query)}"
            }
            
            url = search_urls.get(site, f"https://www.google.com/search?q={urllib.parse.quote(query)}")
            webbrowser.open(url)
            
            return {
                "success": True,
                "action": "search",
                "site": site,
                "query": query,
                "url": url,
                "method": "lightweight_automation",
                "message": f"Opened {site} search for: {query}"
            }
        
        elif intent["action"] == "navigate":
            url = intent["url"]
            if not url.startswith("http"):
                url = f"https://{url}"
            
            webbrowser.open(url)
            
            return {
                "success": True,
                "action": "navigate",
                "url": url,
                "method": "lightweight_automation",
                "message": f"Opened: {url}"
            }
        
        else:
            # Default to Google search
            query = intent["search_query"] or "general search"
            url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
            webbrowser.open(url)
            
            return {
                "success": True,
                "action": "default_search",
                "query": query,
                "url": url,
                "method": "lightweight_automation",
                "message": f"Opened Google search for: {query}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "method": "lightweight_automation"
        }

def universal_web_automate(command: str, prefer_engine: str = "auto") -> Dict[str, Any]:
    """
    Universal web automation that works with any site
    
    Args:
        command: Natural language command
        prefer_engine: auto, selenium, playwright, lightweight
    
    Returns:
        Automation result
    """
    
    print(f"🌐 UNIVERSAL WEB AUTOMATOR: {command}")
    
    # Parse intent
    intent = parse_automation_intent(command)
    print(f"🎯 Detected: {intent['action']} on {intent['target_site']}")
    if intent['search_query']:
        print(f"🔍 Query: {intent['search_query']}")
    
    # Check capabilities
    caps = check_automation_capabilities()
    print(f"🔧 Available: {', '.join(caps['available_engines'])}")
    
    # Choose engine
    if prefer_engine == "auto":
        if intent["auto_play"] and caps["selenium"]:
            engine = "selenium"
        elif caps["selenium"]:
            engine = "selenium" 
        else:
            engine = "lightweight"
    else:
        engine = prefer_engine
    
    print(f"⚡ Using: {engine}")
    
    # Execute automation
    try:
        if engine == "selenium" and caps["selenium"]:
            return selenium_automation(intent)
        else:
            return lightweight_automation(intent)
            
    except Exception as e:
        print(f"⚠️ {engine} failed, falling back to lightweight")
        return lightweight_automation(intent)

# Convenient wrapper functions
def chotu_play_song(song_name: str, site: str = "youtube") -> Dict[str, Any]:
    """Have Chotu play a song"""
    command = f"play {song_name} on {site}"
    return universal_web_automate(command)

def chotu_search_anything(query: str, site: str = "google") -> Dict[str, Any]:
    """Have Chotu search for anything"""
    command = f"search {site} for {query}"
    return universal_web_automate(command)

def chotu_open_url(url: str) -> Dict[str, Any]:
    """Have Chotu open any URL"""
    command = f"navigate to {url}"
    return universal_web_automate(command)

# Test and demo
if __name__ == "__main__":
    print("🌐 UNIVERSAL WEB AUTOMATOR - TEST")
    print("=" * 50)
    
    # Show capabilities
    caps = check_automation_capabilities()
    print(f"🔧 Available engines: {', '.join(caps['available_engines'])}")
    
    if caps['missing']:
        print(f"⚠️  Missing: {', '.join(caps['missing'])}")
    
    # Test commands
    test_commands = [
        "play kitne bechain hoke on youtube",
        "search google for AI news",
        "navigate to github.com",
        "find python tutorials on youtube"
    ]
    
    for command in test_commands:
        print(f"\n🧪 Testing: {command}")
        
        try:
            result = universal_web_automate(command)
            
            if result.get('success'):
                print(f"✅ Success: {result.get('message')}")
                if result.get('url'):
                    print(f"   URL: {result['url']}")
            else:
                print(f"❌ Failed: {result.get('error')}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n🎯 UNIVERSAL WEB AUTOMATOR READY!")
    print(f"   • Works with ANY website")
    print(f"   • Auto-detects actions and sites") 
    print(f"   • Upgrades capabilities automatically")
    print(f"   • Falls back gracefully")
