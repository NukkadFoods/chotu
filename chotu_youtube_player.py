#!/usr/bin/env python3
"""
🎯 CHOTU YOUTUBE PLAYER - WORKING VERSION
========================================
Actually searches and plays YouTube videos using available browser
"""

import os
import time
import webbrowser
import subprocess
from typing import Dict, Any

def skip_ads_automatically(driver, wait, silent=False) -> bool:
    """Automatically detect and skip YouTube ads with safety measures"""
    
    try:
        from selenium.webdriver.common.by import By
        
        # STRICT selectors for ONLY skip buttons (not ad links)
        skip_selectors = [
            # Text-based selectors with strict positioning requirements
            "//button[contains(text(), 'Skip') and contains(@class, 'ytp')]",
            "//button[contains(text(), 'skip') and contains(@class, 'ytp')]", 
            "//button[contains(text(), 'SKIP') and contains(@class, 'ytp')]",
            "//button[contains(text(), 'Skip Ad')]",
            "//button[contains(text(), 'Skip Ads')]",
            
            # Class-based selectors (most reliable for YouTube)
            ".ytp-ad-skip-button",
            ".ytp-skip-ad-button", 
            ".ytp-ad-skip-button-modern",
            ".videoAdUiSkipButton",
            
            # Aria-label based with strict requirements
            "//button[contains(@aria-label, 'Skip') and contains(@class, 'ytp')]",
            "//button[contains(@aria-label, 'skip') and contains(@class, 'ytp')]",
            
            # Container-specific selectors to avoid clicking ads
            ".ytp-ad-skip-button-container button",
            ".ytp-ad-player-overlay .ytp-ad-skip-button"
        ]
        
        # FORBIDDEN patterns that should NEVER be clicked (ad links)
        forbidden_patterns = [
            "learn more",
            "shop now", 
            "visit site",
            "download",
            "install",
            "get app",
            "buy now",
            "order now",
            "flipkart",
            "amazon",
            "myntra",
            "paytm",
            ".com",
            "www.",
            "http"
        ]
        
        ad_detected = False
        
        # Check for ad indicators first
        ad_indicators = [
            ".ytp-ad-player-overlay",
            ".ytp-ad-module", 
            ".ytp-ad-text",
            "[class*='advertisement']",
            "[class*='ad-showing']",
            ".video-ads"
        ]
        
        for indicator in ad_indicators:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, indicator)
                if elements and any(el.is_displayed() for el in elements):
                    ad_detected = True
                    break
            except:
                continue
        
        if ad_detected and not silent:
            print("📺 Ad detected! Looking for GENUINE skip button...")
        
        # Try to find and click skip button with STRICT validation
        for selector in skip_selectors:
            try:
                if selector.startswith("//"):
                    # XPath selector
                    skip_buttons = driver.find_elements(By.XPATH, selector)
                else:
                    # CSS selector
                    skip_buttons = driver.find_elements(By.CSS_SELECTOR, selector)
                
                for skip_button in skip_buttons:
                    try:
                        # Check if button is visible and clickable
                        if skip_button.is_displayed() and skip_button.is_enabled():
                            # Get all text and attributes for validation
                            button_text = (skip_button.text or "").lower().strip()
                            aria_label = (skip_button.get_attribute("aria-label") or "").lower().strip()
                            class_name = (skip_button.get_attribute("class") or "").lower()
                            href = (skip_button.get_attribute("href") or "").lower()
                            onclick = (skip_button.get_attribute("onclick") or "").lower()
                            
                            # SAFETY CHECK: Make sure it's NOT an ad link
                            all_text = f"{button_text} {aria_label} {href} {onclick}"
                            is_forbidden = any(pattern in all_text for pattern in forbidden_patterns)
                            
                            if is_forbidden:
                                if not silent:
                                    print(f"🚫 BLOCKED ad link: '{button_text}' (contains forbidden pattern)")
                                continue
                            
                            # POSITIVE VALIDATION: Must be a real skip button
                            is_skip_button = (
                                # Must contain 'skip' text
                                ("skip" in button_text or "skip" in aria_label) and
                                # Must have YouTube player classes OR be exact skip text
                                ("ytp" in class_name or 
                                 button_text in ["skip", "skip ad", "skip ads"] or
                                 "skip advertisement" in aria_label) and
                                # Must NOT be a link
                                not href and
                                # Must be a button element
                                skip_button.tag_name.lower() == "button"
                            )
                            
                            if is_skip_button:
                                if not silent:
                                    print(f"✅ VERIFIED skip button: '{button_text or aria_label}' - Safe to click")
                                
                                # Try multiple click methods
                                try:
                                    # Method 1: Regular click
                                    skip_button.click()
                                except:
                                    try:
                                        # Method 2: JavaScript click
                                        driver.execute_script("arguments[0].click();", skip_button)
                                    except:
                                        # Method 3: Action chains
                                        from selenium.webdriver.common.action_chains import ActionChains
                                        ActionChains(driver).move_to_element(skip_button).click().perform()
                                
                                time.sleep(2)  # Wait for ad to be skipped
                                
                                if not silent:
                                    print("✅ Ad skipped successfully!")
                                
                                return True
                            else:
                                if not silent:
                                    print(f"⚠️ REJECTED button: '{button_text}' (failed validation)")
                                
                    except Exception as e:
                        if not silent:
                            print(f"⚠️ Error validating button: {e}")
                        continue
                            
            except Exception as e:
                continue
        
        # If no skip button found, check for countdown
        try:
            countdown_selectors = [
                ".ytp-ad-skip-button-countdown",
                ".ytp-ad-preview-text", 
                "[class*='countdown']"
            ]
            
            for countdown_selector in countdown_selectors:
                countdown_elements = driver.find_elements(By.CSS_SELECTOR, countdown_selector)
                if countdown_elements:
                    countdown_text = countdown_elements[0].text
                    if countdown_text and any(char.isdigit() for char in countdown_text):
                        if not silent:
                            print(f"⏳ Waiting for skip button... ({countdown_text})")
                        return False  # Wait for skip button to become available
                        
        except:
            pass
        
        # If ad detected but no skip button found
        if ad_detected and not silent:
            print("⏳ Ad playing - no skip button available yet")
            
        return False
        
    except Exception as e:
        if not silent:
            print(f"⚠️ Ad skip check failed: {e}")
        return False

def close_ad_tabs(driver, youtube_tab_handle, silent=False):
    """Close any tabs that were opened by clicking ads"""
    
    try:
        current_handles = driver.window_handles
        
        # If more than one tab is open, close the extras
        if len(current_handles) > 1:
            for handle in current_handles:
                if handle != youtube_tab_handle:
                    try:
                        driver.switch_to.window(handle)
                        current_url = driver.current_url.lower()
                        
                        # Check if it's an ad-related site
                        ad_sites = [
                            'flipkart', 'amazon', 'myntra', 'paytm', 
                            'shopping', 'buy', 'order', 'download',
                            'install', 'app', 'store'
                        ]
                        
                        is_ad_tab = any(site in current_url for site in ad_sites)
                        
                        if is_ad_tab:
                            if not silent:
                                print(f"🚫 Closing ad tab: {current_url}")
                            driver.close()
                        
                    except Exception as e:
                        if not silent:
                            print(f"⚠️ Error checking tab: {e}")
                        # Close the tab anyway if we can't identify it
                        try:
                            driver.close()
                        except:
                            pass
            
            # Switch back to YouTube tab
            driver.switch_to.window(youtube_tab_handle)
            
            if not silent and len(current_handles) > 1:
                print(f"✅ Closed {len(current_handles) - 1} unwanted tab(s)")
        
    except Exception as e:
        if not silent:
            print(f"⚠️ Error managing tabs: {e}")

def find_chrome_path():
    """Find Chrome executable on macOS"""
    chrome_paths = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/google-chrome",
        "/usr/local/bin/chrome"
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            return path
    return None

def youtube_search_and_play_working(query: str) -> Dict[str, Any]:
    """Search YouTube and play first video - WORKING VERSION"""
    
    print(f"🎵 CHOTU: Searching and playing '{query}' on YouTube...")
    
    # Try Selenium with Chrome first
    chrome_path = find_chrome_path()
    
    if chrome_path:
        try:
            return selenium_youtube_automation(query, chrome_path)
        except Exception as e:
            print(f"⚠️ Selenium failed: {e}")
            print("🔄 Falling back to smart browser approach...")
    
    # Fallback to smart browser approach
    return smart_browser_youtube(query)

def selenium_youtube_automation(query: str, chrome_path: str) -> Dict[str, Any]:
    """Full Selenium automation with Chrome"""
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        print("🚀 Starting Selenium automation with Chrome...")
        
        # Setup Chrome options
        options = Options()
        options.binary_location = chrome_path
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # Create service (no need to specify chromedriver path if it's in PATH)
        service = Service()
        
        # Initialize driver
        driver = webdriver.Chrome(service=service, options=options)
        wait = WebDriverWait(driver, 15)
        
        try:
            # Navigate to YouTube
            print("📺 Opening YouTube...")
            driver.get("https://www.youtube.com")
            
            # Wait for and find search box
            print("🔍 Finding search box...")
            search_box = wait.until(EC.presence_of_element_located((By.NAME, "search_query")))
            
            # Enter search query
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            print(f"🔎 Searching for: {query}")
            
            # Wait for results and find first video
            print("🎬 Looking for first video...")
            time.sleep(3)  # Let results load
            
            # Multiple selectors to find video links
            video_selectors = [
                "a#video-title",
                "ytd-video-renderer a#video-title", 
                "a[href*='/watch?v=']"
            ]
            
            first_video = None
            video_title = "Unknown Video"
            
            for selector in video_selectors:
                try:
                    videos = driver.find_elements(By.CSS_SELECTOR, selector)
                    if videos:
                        first_video = videos[0]
                        video_title = first_video.get_attribute("title") or first_video.text or "Video"
                        break
                except:
                    continue
            
            if first_video:
                print(f"🎵 Found: {video_title}")
                print("▶️ Clicking to play...")
                
                # Scroll into view and click
                driver.execute_script("arguments[0].scrollIntoView(true);", first_video)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", first_video)
                
                # Wait for video page to load
                time.sleep(5)
                
                # Store the YouTube tab handle for later
                youtube_tab = driver.current_window_handle
                
                # Auto-skip ads functionality with safety measures
                print("🚫 Checking for ads and auto-skipping (with safety measures)...")
                skip_ads_automatically(driver, wait)
                
                # Close any unwanted tabs that might have opened
                close_ad_tabs(driver, youtube_tab)
                
                current_url = driver.current_url
                
                print("🎉 SUCCESS! Video should be playing now!")
                print(f"🎬 Playing: {video_title}")
                
                # Keep browser open and continue monitoring for ads
                print("⏰ Keeping browser open for 10 seconds to enjoy the music...")
                print("🛡️ Continuing to monitor for ads with safety measures...")
                
                # Monitor for ads for a longer period with tab management
                for i in range(10):
                    time.sleep(1)
                    skip_ads_automatically(driver, wait, silent=True)
                    # Check for unwanted tabs every few seconds
                    if i % 3 == 0:
                        close_ad_tabs(driver, youtube_tab, silent=True)
                
                return {
                    "success": True,
                    "method": "selenium_chrome",
                    "action": "search_and_play",
                    "query": query,
                    "video_title": video_title,
                    "url": current_url,
                    "message": f"Successfully playing '{video_title}' on YouTube"
                }
            else:
                return {
                    "success": False,
                    "error": "No videos found in search results",
                    "fallback_available": True
                }
                
        finally:
            driver.quit()
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Selenium automation failed: {e}",
            "fallback_available": True
        }

def smart_browser_youtube(query: str) -> Dict[str, Any]:
    """Smart browser approach - opens YouTube search and uses AppleScript to interact"""
    
    print("🌟 Using smart browser approach...")
    
    try:
        import urllib.parse
        
        # Create YouTube search URL
        search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
        
        print(f"🌐 Opening: {search_url}")
        webbrowser.open(search_url)
        
        # Wait a moment for page to load
        time.sleep(3)
        
        # Try to use AppleScript to click first video (macOS only)
        try:
            applescript = '''
            tell application "Google Chrome"
                activate
                delay 2
                tell application "System Events"
                    tell process "Google Chrome"
                        set frontmost to true
                        delay 1
                        -- Try to find and click first video
                        try
                            click (first button of first group of first UI element whose name contains "video")
                        on error
                            -- Fallback: just press tab and enter to navigate to first result
                            key code 48  -- Tab key
                            delay 0.5
                            key code 48  -- Tab key
                            delay 0.5
                            key code 36  -- Return key
                        end try
                    end tell
                end tell
            end tell
            '''
            
            subprocess.run(["osascript", "-e", applescript], check=False)
            
            return {
                "success": True,
                "method": "smart_browser_applescript",
                "action": "search_and_play",
                "query": query,
                "url": search_url,
                "message": f"Opened YouTube search for '{query}' and attempted to play first video"
            }
            
        except:
            # If AppleScript fails, just return the search
            return {
                "success": True,
                "method": "smart_browser_basic",
                "action": "search",
                "query": query,
                "url": search_url,
                "message": f"Opened YouTube search for '{query}' - please click on first video to play"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Smart browser approach failed: {e}"
        }

# Main function for Chotu
def chotu_play_youtube(song_query: str) -> Dict[str, Any]:
    """Main function for Chotu to play YouTube videos"""
    
    print("🎵 CHOTU YOUTUBE PLAYER")
    print("=" * 40)
    
    result = youtube_search_and_play_working(song_query)
    
    if result["success"]:
        print(f"\\n✅ SUCCESS!")
        print(f"🎶 {result['message']}")
    else:
        print(f"\\n❌ FAILED!")
        print(f"💥 {result.get('error', 'Unknown error')}")
        
        if result.get('fallback_available'):
            print("🔄 Trying fallback method...")
            fallback_result = smart_browser_youtube(song_query)
            if fallback_result["success"]:
                print(f"✅ Fallback success: {fallback_result['message']}")
                return fallback_result
    
    return result

# Test the system
if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Chotu YouTube Player with Ad-Skipping')
    parser.add_argument('--search', type=str, help='Search query for YouTube')
    parser.add_argument('--headless', type=str, default='false', help='Run in headless mode (true/false)')
    
    args = parser.parse_args()
    
    # Use search query from command line or default
    search_query = args.search if args.search else "kitne bechain hoke"
    
    print("🎯 CHOTU YOUTUBE PLAYER")
    print("=" * 50)
    print(f"🔍 Search Query: {search_query}")
    print(f"👁️ Headless Mode: {args.headless}")
    print()
    
    result = chotu_play_youtube(search_query)
    
    print("\n📊 FINAL RESULT:")
    for key, value in result.items():
        print(f"   {key}: {value}")
