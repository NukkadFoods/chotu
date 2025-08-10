#!/usr/bin/env python3
"""
🎯 ENHANCED CHOTU YOUTUBE AUTOMATION
===================================
Advanced YouTube automation with session management, popup handling, and video control
"""

import os
import time
import json
import subprocess
import random
import socket
import requests
from datetime import datetime
from typing import Dict, Any, List, Optional

try:
    from .stealth_browser import create_stealth_driver, stealth_browser
    STEALTH_AVAILABLE = True
except ImportError:
    try:
        from stealth_browser import create_stealth_driver, stealth_browser
        STEALTH_AVAILABLE = True
    except ImportError:
        STEALTH_AVAILABLE = False
        print("⚠️ Stealth browser not available")

class YouTubeSessionManager:
    """Manages persistent YouTube browser sessions"""
    
    def __init__(self):
        self.active_driver = None
        self.youtube_tab = None
        self.session_active = False
        self.last_query = None
        self.current_video_url = None
    
    def check_network_connectivity(self) -> bool:
        """Check network connectivity to YouTube"""
        try:
            print("🔌 Checking network connectivity...")
            
            # Check DNS resolution
            try:
                socket.gethostbyname('www.youtube.com')
                print("✅ DNS resolution successful")
            except socket.gaierror as e:
                print(f"❌ DNS resolution failed: {e}")
                return False
            
            # Check HTTP connectivity
            try:
                response = requests.get('https://www.google.com', timeout=10)
                if response.status_code == 200:
                    print("✅ Internet connectivity confirmed")
                    return True
                else:
                    print(f"❌ HTTP check failed with status: {response.status_code}")
                    return False
            except requests.RequestException as e:
                print(f"❌ Network connectivity test failed: {e}")
                return False
                
        except Exception as e:
            print(f"❌ Network check error: {e}")
            return False
        
    def get_active_driver(self):
        """Get or create an active browser session"""
        
        if self.active_driver and self.session_active:
            try:
                # Test if driver is still alive
                self.active_driver.current_url
                return self.active_driver
            except:
                # Driver is dead, clean up
                self.cleanup_session()
        
        # Create new session
        return self.create_new_session()
    
    def create_new_session(self):
        """Create a new browser session using ONLY stealth browser"""
        try:
            print("🕵️ Creating new stealth YouTube browser session...")
            
            # FORCE stealth browser usage - no fallbacks
            if not STEALTH_AVAILABLE:
                raise Exception("Stealth browser not available. Please install: pip install undetected-chromedriver")
            
            # Use ONLY stealth browser
            from stealth_browser import StealthBrowser
            stealth = StealthBrowser()
            self.active_driver = stealth.get_stealth_driver(headless=False)
            
            if not self.active_driver:
                raise Exception("Failed to create stealth browser")
            
            self.session_active = True
            print("✅ Stealth browser session created successfully")
            return self.active_driver
            
        except Exception as e:
            print(f"❌ Failed to create stealth session: {e}")
            raise Exception(f"Stealth browser creation failed: {e} - No fallback allowed!")
    
    def _create_fallback_session(self):
        """Fallback browser creation"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            
            print("� Creating fallback browser session...")
            
            # Setup Chrome options for persistent session
            options = Options()
            
            # Anti-detection options
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Additional stealth options
            options.add_argument("--disable-web-security")
            options.add_argument("--disable-features=VizDisplayCompositor")
            options.add_argument("--disable-ipc-flooding-protection")
            options.add_argument("--disable-renderer-backgrounding")
            options.add_argument("--disable-backgrounding-occluded-windows")
            options.add_argument("--disable-client-side-phishing-detection")
            
            # Performance and stability options
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-gpu")
            options.add_argument("--remote-debugging-port=9222")  # For session reuse
            
            # YouTube-specific optimizations
            options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Preferences for better YouTube experience
            prefs = {
                "profile.default_content_setting_values.notifications": 2,
                "profile.default_content_settings.popups": 0,
                "profile.managed_default_content_settings.images": 1,
                "profile.default_content_setting_values.media_stream": 1,
                "profile.default_content_setting_values.geolocation": 2,
                "profile.default_content_setting_values.microphone": 2,
                "profile.default_content_setting_values.camera": 2
            }
            options.add_experimental_option("prefs", prefs)
            
            # Use user data directory for persistence
            user_data_dir = os.path.expanduser("~/Library/Application Support/Google/Chrome/ChoutuYoutube")
            options.add_argument(f"--user-data-dir={user_data_dir}")
            
            service = Service()
            self.active_driver = webdriver.Chrome(service=service, options=options)
            
            # Execute comprehensive anti-detection script
            self.active_driver.execute_script("""
                // Remove webdriver property
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                
                // Mock plugins and languages
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
                
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en']
                });
                
                // Mock chrome object
                window.chrome = {
                    runtime: {}
                };
                
                // Override permissions API
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                        Promise.resolve({ state: Notification.permission }) :
                        originalQuery(parameters)
                );
                
                // Randomize screen properties
                Object.defineProperty(screen, 'availHeight', {get: () => 900});
                Object.defineProperty(screen, 'availWidth', {get: () => 1440});
            """)
            
            self.session_active = True
            
            print("✅ Fallback browser session created")
            return self.active_driver
            
        except Exception as e:
            print(f"❌ Failed to create fallback session: {e}")
            return None
    
    def cleanup_session(self):
        """Clean up browser session"""
        if self.active_driver:
            try:
                self.active_driver.quit()
            except:
                pass
        
        self.active_driver = None
        self.youtube_tab = None
        self.session_active = False
        self.current_video_url = None

class YouTubeVideoController:
    """Controls YouTube video playback"""
    
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
    
    def stop_current_video(self) -> bool:
        """Stop currently playing video"""
        try:
            print("⏹️ Stopping current video...")
            
            # Method 1: Try to pause using keyboard shortcut
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.common.action_chains import ActionChains
            
            # Focus on video player and press spacebar to pause
            try:
                video_player = self.driver.find_element("css selector", ".html5-video-player")
                video_player.click()
                time.sleep(0.5)
                ActionChains(self.driver).send_keys(Keys.SPACE).perform()
                print("✅ Video paused using spacebar")
                return True
            except:
                pass
            
            # Method 2: Try to click pause button
            try:
                pause_selectors = [
                    ".ytp-play-button[aria-label*='Pause']",
                    ".ytp-play-button[title*='Pause']",
                    "button[aria-label*='Pause']"
                ]
                
                for selector in pause_selectors:
                    pause_buttons = self.driver.find_elements("css selector", selector)
                    for btn in pause_buttons:
                        if btn.is_displayed() and btn.is_enabled():
                            btn.click()
                            print("✅ Video paused using pause button")
                            return True
            except:
                pass
            
            # Method 3: JavaScript method
            try:
                self.driver.execute_script("""
                    var videos = document.querySelectorAll('video');
                    for (var i = 0; i < videos.length; i++) {
                        if (!videos[i].paused) {
                            videos[i].pause();
                        }
                    }
                """)
                print("✅ Video paused using JavaScript")
                return True
            except:
                pass
            
            print("⚠️ Could not pause current video")
            return False
            
        except Exception as e:
            print(f"❌ Error stopping video: {e}")
            return False
    
    def handle_youtube_errors(self) -> bool:
        """Handle YouTube error messages and recovery - improved to avoid refresh loops"""
        try:
            print("🔍 Checking for YouTube error messages...")
            
            # Check for critical errors only (not general page errors)
            critical_error_indicators = [
                "This video is unavailable",
                "Video unavailable", 
                "Please try again later"
            ]
            
            # Less aggressive error detection - only check visible error messages
            try:
                # Look for actual error dialogs/overlays, not page source
                error_elements = self.driver.find_elements("css selector", 
                    ".ytp-error, .error-screen, [class*='error'], [id*='error']")
                
                visible_errors = []
                for element in error_elements:
                    if element.is_displayed():
                        error_text = element.text.strip()
                        if error_text and len(error_text) > 10:  # Avoid empty or tiny text
                            visible_errors.append(error_text.lower())
                
                # Only trigger recovery for actual critical errors
                found_critical_error = False
                for error_text in visible_errors:
                    for critical_error in critical_error_indicators:
                        if critical_error.lower() in error_text:
                            print(f"⚠️ Found critical YouTube error: {critical_error}")
                            found_critical_error = True
                            break
                    if found_critical_error:
                        break
                
                if not found_critical_error:
                    return False
                
            except Exception:
                # If we can't check for errors, assume everything is fine
                return False
            
            # Minimal recovery - just try to click play button if video is paused
            print("🔄 Attempting minimal error recovery...")
            
            try:
                # Try to find and click play button instead of refreshing
                play_button = self.driver.find_element("css selector", ".ytp-play-button")
                if play_button.is_displayed():
                    play_button.click()
                    print("✅ Clicked play button for recovery")
                    return True
            except:
                pass
            
            # Only refresh as last resort and limit frequency
            if not hasattr(self, '_last_refresh_time'):
                self._last_refresh_time = 0
            
            current_time = time.time()
            if current_time - self._last_refresh_time > 60:  # Max 1 refresh per minute
                print("🔄 Performing limited refresh (max once per minute)...")
                self.driver.refresh()
                self._last_refresh_time = current_time
                time.sleep(5)
                return True
            else:
                print("⏭️ Skipping refresh (too recent), letting video continue...")
                return False
            
        except Exception as e:
            print(f"❌ Error handling YouTube errors: {e}")
            return False
    
    def _handle_automation_detection(self) -> bool:
        """Special handling for automation detection"""
        try:
            print("🕵️ Implementing stealth mode for automation detection...")
            
            # Strategy 1: Execute additional stealth scripts
            self.driver.execute_script("""
                // Additional stealth measures
                delete navigator.__proto__.webdriver;
                
                // Override toString methods
                navigator.plugins.toString = () => '[object PluginArray]';
                navigator.languages.toString = () => 'en-US,en';
                
                // Mock additional properties
                Object.defineProperty(navigator, 'hardwareConcurrency', {
                    get: () => 4
                });
                
                // Clear automation flags
                window.navigator.webdriver = undefined;
                delete window.navigator.webdriver;
                
                // Override Notification.permission
                try {
                    Object.defineProperty(Notification, 'permission', {
                        get: () => 'default'
                    });
                } catch(e) {}
            """)
            
            # Strategy 2: Clear browser data
            print("🧹 Clearing browser data...")
            try:
                self.driver.delete_all_cookies()
                self.driver.execute_script("window.localStorage.clear();")
                self.driver.execute_script("window.sessionStorage.clear();")
            except:
                pass
            
            # Strategy 3: Navigate away and back
            print("🔄 Performing navigation reset...")
            self.driver.get("https://www.google.com")
            time.sleep(3)
            self.driver.get("https://www.youtube.com")
            time.sleep(5)
            
            # Strategy 4: User-like behavior simulation
            print("👤 Simulating user behavior...")
            from selenium.webdriver.common.action_chains import ActionChains
            actions = ActionChains(self.driver)
            
            # Simulate mouse movements
            actions.move_by_offset(100, 100).perform()
            time.sleep(1)
            actions.move_by_offset(-50, -50).perform()
            time.sleep(1)
            
            # Simulate scrolling
            self.driver.execute_script("window.scrollBy(0, 300);")
            time.sleep(2)
            self.driver.execute_script("window.scrollBy(0, -200);")
            time.sleep(1)
            
            print("✅ Stealth recovery completed")
            return True
            
        except Exception as e:
            print(f"❌ Error in automation detection handling: {e}")
            return False
    
    def monitor_video_health(self, duration_seconds: int = 30) -> bool:
        """Monitor video for errors during playback"""
        try:
            print(f"👁️ Monitoring video health for {duration_seconds} seconds...")
            
            start_time = time.time()
            check_interval = 5  # Check every 5 seconds
            
            while time.time() - start_time < duration_seconds:
                # Check for errors
                if self.handle_youtube_errors():
                    print("⚠️ Error detected and handled during monitoring")
                
                # Check if video is still playing
                video_playing = self.driver.execute_script("""
                    var videos = document.querySelectorAll('video');
                    for (var i = 0; i < videos.length; i++) {
                        if (!videos[i].paused && videos[i].currentTime > 0) {
                            return true;
                        }
                    }
                    return false;
                """)
                
                if not video_playing:
                    print("⚠️ Video stopped playing, checking for errors...")
                    self.handle_youtube_errors()
                
                time.sleep(check_interval)
            
            print("✅ Video health monitoring completed")
            return True
            
        except Exception as e:
            print(f"❌ Error monitoring video health: {e}")
            return False
    
    def close_popups_and_ads(self) -> bool:
        """Close YouTube popups, overlays, and ads"""
        try:
            print("🚫 Checking for popups and ads to close...")
            
            closed_something = False
            
            # Check for YouTube error messages first
            if self.handle_youtube_errors():
                closed_something = True
            
            # Close consent/cookie popups
            consent_selectors = [
                "button[aria-label*='Accept all']",
                "button[aria-label*='I agree']", 
                "button[aria-label*='Accept']",
                "button:contains('Accept all')",
                ".consent-button",
                "[data-testid='accept-all-button']"
            ]
            
            for selector in consent_selectors:
                try:
                    elements = self.driver.find_elements("css selector", selector)
                    for element in elements:
                        if element.is_displayed():
                            element.click()
                            print("✅ Closed consent popup")
                            closed_something = True
                            time.sleep(1)
                            break
                except:
                    continue
            
            # Close YouTube Music desktop app promotion - ENHANCED METHOD
            print("🎵 Enhanced YouTube Music popup detection...")
            
            # Method 1: Multiple text-based detection
            music_popup_texts = [
                "Music discovery made easy",
                "Get YouTube Music",
                "Try YouTube Music",
                "YouTube Music Premium",
                "No thanks"
            ]
            
            for text_to_find in music_popup_texts:
                try:
                    # Find elements containing this text
                    elements = self.driver.find_elements("xpath", f"//*[contains(text(), '{text_to_find}')]")
                    for element in elements:
                        if element.is_displayed():
                            # Look for parent containers or nearby buttons
                            parent = element.find_element("xpath", "..")
                            buttons = parent.find_elements("css selector", "button")
                            for btn in buttons:
                                btn_text = btn.text.lower()
                                if "no thanks" in btn_text or "dismiss" in btn_text or "close" in btn_text:
                                    btn.click()
                                    print(f"✅ Closed YouTube Music popup using: {btn_text}")
                                    closed_something = True
                                    time.sleep(1)
                                    break
                except:
                    continue
            
            # Method 2: Direct button selectors for YouTube Music popup
            music_close_selectors = [
                "button[aria-label*='No thanks']",
                "button[aria-label*='Dismiss']", 
                "button[aria-label*='Close']",
                "button:contains('No thanks')",
                "button:contains('Dismiss')",
                "[data-testid*='dismiss']",
                "[data-testid*='close']",
                ".dismiss-button",
                ".close-button"
            ]
            
            for selector in music_close_selectors:
                try:
                    elements = self.driver.find_elements("css selector", selector)
                    for element in elements:
                        if element.is_displayed():
                            element.click()
                            print(f"✅ Closed popup with selector: {selector}")
                            closed_something = True
                            time.sleep(1)
                            break
                except:
                    continue
            
            # Method 3: Enhanced JavaScript detection and closing
            try:
                popup_closed = self.driver.execute_script("""
                    // Look for YouTube Music popup more aggressively
                    var allElements = document.querySelectorAll('*');
                    var found = false;
                    
                    for (var i = 0; i < allElements.length; i++) {
                        var elem = allElements[i];
                        var text = (elem.textContent || elem.innerText || '').toLowerCase();
                        
                        if (text.includes('music discovery made easy') || 
                            text.includes('get youtube music') ||
                            text.includes('try youtube music')) {
                            
                            // Look for close/dismiss buttons in the same container
                            var container = elem.closest('div[role="dialog"], div[class*="popup"], div[class*="modal"], div[class*="overlay"]');
                            if (container) {
                                var buttons = container.querySelectorAll('button, [role="button"]');
                                for (var j = 0; j < buttons.length; j++) {
                                    var btn = buttons[j];
                                    var btnText = (btn.textContent || btn.innerText || '').toLowerCase();
                                    var ariaLabel = (btn.getAttribute('aria-label') || '').toLowerCase();
                                    
                                    if (btnText.includes('no thanks') || btnText.includes('dismiss') || 
                                        btnText.includes('close') || ariaLabel.includes('dismiss') ||
                                        ariaLabel.includes('close') || ariaLabel.includes('no thanks')) {
                                        btn.click();
                                        found = true;
                                        break;
                                    }
                                }
                            }
                        }
                    }
                    return found;
                """)
                
                if popup_closed:
                    print("✅ Closed YouTube Music popup using JavaScript")
                    closed_something = True
                    time.sleep(1)
                    
            except Exception as e:
                print(f"⚠️ JavaScript popup detection failed: {e}")
            
            # Method 4: Look for overlay/modal containers and close them
            overlay_selectors = [
                "[role='dialog']",
                ".popup-container", 
                ".modal-container",
                ".overlay",
                "[class*='popup']",
                "[class*='modal']",
                "[class*='overlay']"
            ]
            
            for selector in overlay_selectors:
                try:
                    overlays = self.driver.find_elements("css selector", selector)
                    for overlay in overlays:
                        if overlay.is_displayed():
                            # Look for close buttons within the overlay
                            close_buttons = overlay.find_elements("css selector", "button[aria-label*='Close'], button[aria-label*='Dismiss'], .close-button")
                            for btn in close_buttons:
                                if btn.is_displayed():
                                    btn.click()
                                    print("✅ Closed overlay popup")
                                    closed_something = True
                                    time.sleep(1)
                                    break
                except:
                    continue
            
            # Original JavaScript method (keeping as backup)
            try:
                popup_closed = self.driver.execute_script("""
                    // Look for text containing "Music discovery made easy" or "No thanks"
                    var elements = document.querySelectorAll('*');
                    for (var i = 0; i < elements.length; i++) {
                        var elem = elements[i];
                        var text = elem.textContent || elem.innerText || '';
                        
                        if (text.includes('Music discovery made easy') || 
                            text.includes('YouTube Music web player') ||
                            text.includes('new releases, covers and hard-to-find songs')) {
                            
                            // Found the popup, now find the close button
                            var buttons = elem.querySelectorAll('button, [role="button"]');
                            for (var j = 0; j < buttons.length; j++) {
                                var btnText = buttons[j].textContent || buttons[j].innerText || '';
                                var ariaLabel = buttons[j].getAttribute('aria-label') || '';
                                
                                if (btnText.includes('No thanks') || 
                                    btnText.includes('Dismiss') ||
                                    ariaLabel.includes('Close') ||
                                    ariaLabel.includes('Dismiss')) {
                                    
                                    buttons[j].click();
                                    console.log('Closed YouTube Music popup via JavaScript');
                                    return true;
                                }
                            }
                        }
                    }
                    return false;
                """)
                
                if popup_closed:
                    print("✅ Closed YouTube Music popup via JavaScript")
                    closed_something = True
                    time.sleep(2)
                
            except Exception as e:
                print(f"⚠️ JavaScript popup close failed: {e}")
            
            # Backup method: CSS selectors for specific buttons
            music_popup_selectors = [
                "button:contains('No thanks')",
                "button[aria-label*='No thanks']", 
                "button:contains('Check it out')",
                "button:contains('Dismiss')",
                "[data-testid='dismiss-button']",
                ".ytmusic-promotion-dialog button",
                "[aria-label*='Close'] button",
                ".dismiss-button",
                "yt-button-renderer:contains('No thanks')",
                "tp-yt-paper-button:contains('No thanks')",
                "button[aria-label*='Dismiss']",
                "button[title*='Close']",
                "button[title*='Dismiss']",
                "[role='button']:contains('No thanks')"
            ]
            
            for selector in music_popup_selectors:
                try:
                    elements = self.driver.find_elements("css selector", selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            # Check if this looks like the YouTube Music popup
                            parent_text = ""
                            try:
                                parent = element.find_element("xpath", "../..")
                                parent_text = parent.text.lower()
                            except:
                                pass
                            
                            if any(keyword in parent_text for keyword in [
                                "music discovery made easy",
                                "youtube music web player", 
                                "new releases, covers",
                                "hard-to-find songs",
                                "monthly paid subscription",
                                "cancel anytime"
                            ]):
                                print(f"🎯 Found YouTube Music popup button: {element.text}")
                                element.click()
                                print("✅ Closed YouTube Music desktop promotion")
                                closed_something = True
                                time.sleep(2)
                                break
                except:
                    continue
            
            # Additional aggressive search for YouTube Music popup
            try:
                print("🔍 Aggressive search for YouTube Music popup...")
                all_buttons = self.driver.find_elements("css selector", "button, [role='button']")
                
                for button in all_buttons:
                    try:
                        if not button.is_displayed():
                            continue
                            
                        button_text = button.text.lower()
                        aria_label = (button.get_attribute("aria-label") or "").lower()
                        
                        # Look for "No thanks" button specifically
                        if ("no thanks" in button_text or "no thanks" in aria_label):
                            # Check if nearby text mentions music
                            try:
                                parent_element = button.find_element("xpath", "../../../..")
                                context_text = parent_element.text.lower()
                                
                                if any(phrase in context_text for phrase in [
                                    "music discovery",
                                    "youtube music",
                                    "web player",
                                    "monthly paid subscription"
                                ]):
                                    print(f"🎯 Found 'No thanks' in music context")
                                    button.click()
                                    print("✅ Closed YouTube Music popup via aggressive search")
                                    closed_something = True
                                    time.sleep(2)
                                    break
                            except:
                                # Just click any "No thanks" button as backup
                                print(f"🎯 Clicking 'No thanks' button as backup")
                                button.click()
                                print("✅ Closed popup via 'No thanks' button")
                                closed_something = True
                                time.sleep(1)
                                break
                                
                    except:
                        continue
                        
            except Exception as e:
                print(f"⚠️ Aggressive search failed: {e}")
            
            # Try alternative approach for YouTube Music popup using XPath
            try:
                # Look for text containing "Where music meets your desktop"
                music_popup_xpath = "//div[contains(text(), 'Where music meets your desktop')]//ancestor::div[contains(@class, 'dialog') or contains(@class, 'popup')]//button[contains(text(), 'No thanks')]"
                no_thanks_button = self.driver.find_elements("xpath", music_popup_xpath)
                
                if no_thanks_button and no_thanks_button[0].is_displayed():
                    no_thanks_button[0].click()
                    print("✅ Closed YouTube Music popup via XPath")
                    closed_something = True
                    time.sleep(2)
            except:
                pass
            
            # JavaScript-based popup detection and closure
            try:
                popup_closed = self.driver.execute_script("""
                    // Look for YouTube Music desktop promotion
                    var found = false;
                    
                    // Method 1: Find by text content
                    var elements = document.querySelectorAll('*');
                    for (var i = 0; i < elements.length; i++) {
                        var text = elements[i].textContent || elements[i].innerText || '';
                        if (text.includes('Where music meets your desktop') || 
                            text.includes('Our desktop experience was built') ||
                            text.includes('Monthly paid subscription')) {
                            
                            // Find the parent container
                            var container = elements[i];
                            while (container.parentElement) {
                                container = container.parentElement;
                                if (container.className && 
                                    (container.className.includes('dialog') || 
                                     container.className.includes('popup') ||
                                     container.className.includes('modal'))) {
                                    break;
                                }
                            }
                            
                            // Look for "No thanks" button in this container
                            var buttons = container.querySelectorAll('button');
                            for (var j = 0; j < buttons.length; j++) {
                                var buttonText = buttons[j].textContent || buttons[j].innerText || '';
                                if (buttonText.toLowerCase().includes('no thanks') || 
                                    buttonText.toLowerCase().includes('dismiss')) {
                                    buttons[j].click();
                                    found = true;
                                    break;
                                }
                            }
                            
                            if (found) break;
                        }
                    }
                    
                    return found;
                """)
                
                if popup_closed:
                    print("✅ Closed YouTube Music popup via JavaScript")
                    closed_something = True
                    time.sleep(2)
                
            except Exception as e:
                print(f"⚠️ JavaScript popup closure failed: {e}")
                pass
            
            # Close YouTube premium/subscription popups
            premium_selectors = [
                "button[aria-label*='No thanks']",
                "button[aria-label*='Not now']",
                "button[aria-label*='Skip trial']",
                "button[aria-label*='Dismiss']",
                ".dismiss-button",
                ".ytd-popup-container button[aria-label*='Close']"
            ]
            
            for selector in premium_selectors:
                try:
                    elements = self.driver.find_elements("css selector", selector)
                    for element in elements:
                        if element.is_displayed():
                            element.click()
                            print("✅ Closed premium popup")
                            closed_something = True
                            time.sleep(1)
                            break
                except:
                    continue
            
            # Close notification popups  
            notification_selectors = [
                "button[aria-label*='Turn on notifications']",
                "button[aria-label*='Allow notifications']", 
                "button[aria-label*='Block']",
                "button[aria-label*='Don\\'t allow']",
                ".notification-popup button"
            ]
            
            for selector in notification_selectors:
                try:
                    elements = self.driver.find_elements("css selector", selector)
                    for element in elements:
                        if element.is_displayed():
                            element.click()
                            print("✅ Closed notification popup")
                            closed_something = True
                            time.sleep(1)
                            break
                except:
                    continue
            
            # Handle video overlay ads
            overlay_selectors = [
                ".ytp-ad-overlay-close-button",
                ".ytp-ad-overlay-close-container button",
                "button[aria-label*='Close ad']",
                ".ad-overlay-close-button"
            ]
            
            for selector in overlay_selectors:
                try:
                    elements = self.driver.find_elements("css selector", selector)
                    for element in elements:
                        if element.is_displayed():
                            element.click()
                            print("✅ Closed video overlay ad")
                            closed_something = True
                            time.sleep(1)
                            break
                except:
                    continue
            
            # Skip video ads
            skip_selectors = [
                ".ytp-ad-skip-button",
                ".ytp-skip-ad-button",
                "button[aria-label*='Skip ad']",
                "button:contains('Skip Ad')"
            ]
            
            for selector in skip_selectors:
                try:
                    elements = self.driver.find_elements("css selector", selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            # Safety check - make sure it's actually a skip button
                            button_text = element.text.lower()
                            aria_label = (element.get_attribute("aria-label") or "").lower()
                            
                            if "skip" in button_text or "skip" in aria_label:
                                element.click()
                                print("✅ Skipped video ad")
                                closed_something = True
                                time.sleep(2)
                                break
                except:
                    continue
            
            if closed_something:
                print("✅ Successfully handled popups/ads")
            else:
                print("ℹ️ No popups or ads found to close")
            
            return closed_something
            
        except Exception as e:
            print(f"❌ Error handling popups: {e}")
            return False
    
    def skip_video_ads_only(self) -> bool:
        """Enhanced video ad skipping with aggressive detection"""
        try:
            print("🎬 Looking for video ads to skip...")
            
            # Enhanced skip selectors with ALL possible variations
            skip_selectors = [
                # Standard YouTube skip buttons
                ".ytp-ad-skip-button",
                ".ytp-skip-ad-button", 
                ".ytp-ad-skip-button-modern",
                ".ytp-ad-skip-button-text",
                ".ytp-ad-skip-button-container button",
                
                # Aria label based (most reliable)
                "button[aria-label*='Skip ad']",
                "button[aria-label*='Skip Ad']", 
                "button[aria-label*='skip ad']",
                "button[aria-label*='Skip this ad']",
                "button[aria-label*='Skip']",
                
                # Text content based
                "button:contains('Skip Ad')",
                "button:contains('Skip ad')",
                "button:contains('skip ad')",
                "button:contains('SKIP AD')",
                "button:contains('Skip')",
                
                # Class name based
                "[class*='skip'][class*='button']",
                "button[class*='ytp-ad-skip']",
                "button[class*='skip-button']",
                "[class*='ad-skip']",
                
                # Generic approaches
                "[data-testid*='skip']",
                "button[id*='skip']",
                ".skip-button",
                "[role='button'][aria-label*='Skip']",
                
                # Container searches
                ".video-ads button",
                ".ytp-ad-module button",
                ".ad-container button"
            ]
            
            # Method 1: Multiple rounds of selector trying (ads might not be ready immediately)
            for round_num in range(3):  # Try 3 rounds with delays
                print(f"🔍 Ad skip round {round_num + 1}/3...")
                
                for selector in skip_selectors:
                    try:
                        elements = self.driver.find_elements("css selector", selector)
                        for element in elements:
                            if element.is_displayed() and element.is_enabled():
                                # Enhanced safety check
                                button_text = (element.text or "").lower().strip()
                                aria_label = (element.get_attribute("aria-label") or "").lower().strip()
                                class_name = (element.get_attribute("class") or "").lower()
                                
                                # Check if it's really a skip button
                                is_skip_button = (
                                    ("skip" in button_text and ("ad" in button_text or len(button_text) < 15)) or
                                    ("skip" in aria_label and "ad" in aria_label) or
                                    ("skip" in class_name and ("ad" in class_name or "ytp" in class_name))
                                )
                                
                                if is_skip_button:
                                    print(f"🎯 Found skip button: text='{button_text}', aria='{aria_label}'")
                                    try:
                                        # Enhanced clicking approach
                                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                                        time.sleep(0.3)
                                        
                                        # Try direct click first
                                        element.click()
                                        print("✅ Clicked skip button successfully")
                                        time.sleep(1.5)
                                        
                                        # Verify the ad was actually skipped
                                        time.sleep(1)
                                        remaining_ads = len(self.driver.find_elements("css selector", ".ytp-ad-skip-button, .ytp-skip-ad-button"))
                                        if remaining_ads == 0:
                                            print("✅ Ad successfully skipped - no more skip buttons visible")
                                            return True
                                        else:
                                            print(f"⚠️ Skip clicked but {remaining_ads} skip buttons still visible")
                                            
                                    except Exception as click_error:
                                        print(f"⚠️ Click failed, trying JavaScript: {click_error}")
                                        try:
                                            self.driver.execute_script("arguments[0].click();", element)
                                            print("✅ JavaScript click successful")
                                            time.sleep(1.5)
                                            return True
                                        except:
                                            print("❌ JavaScript click also failed")
                                            
                    except Exception as e:
                        continue  # Silent failure for individual selectors
                
                # Wait between rounds to let ads load
                if round_num < 2:
                    time.sleep(1.5)
            
            # Method 2: JavaScript-based comprehensive detection
            try:
                print("🔍 Trying comprehensive JavaScript ad skip detection...")
                skip_result = self.driver.execute_script("""
                    console.log('Starting comprehensive ad skip detection...');
                    
                    // Function to click element safely
                    function safeClick(element) {
                        try {
                            element.scrollIntoView({block: 'center'});
                            setTimeout(() => {
                                element.click();
                                console.log('Successfully clicked skip button');
                            }, 100);
                            return true;
                        } catch (e) {
                            console.log('Click failed:', e);
                            return false;
                        }
                    }
                    
                    // Method 1: Look for YouTube's standard skip buttons
                    var standardSelectors = [
                        '.ytp-ad-skip-button',
                        '.ytp-skip-ad-button',
                        '.ytp-ad-skip-button-modern'
                    ];
                    
                    for (var sel of standardSelectors) {
                        var btns = document.querySelectorAll(sel);
                        for (var btn of btns) {
                            if (btn.offsetParent !== null) { // Check if visible
                                console.log('Found standard skip button:', sel);
                                if (safeClick(btn)) return true;
                            }
                        }
                    }
                    
                    // Method 2: Comprehensive button scanning
                    var allButtons = document.querySelectorAll('button, [role="button"], [class*="button"]');
                    
                    for (var btn of allButtons) {
                        if (btn.offsetParent === null) continue; // Skip hidden elements
                        
                        var text = (btn.textContent || btn.innerText || '').toLowerCase().trim();
                        var ariaLabel = (btn.getAttribute('aria-label') || '').toLowerCase();
                        var className = (btn.className || '').toLowerCase();
                        
                        // Check for skip ad indicators
                        var isSkipButton = (
                            (text.includes('skip') && (text.includes('ad') || text.length < 15)) ||
                            (ariaLabel.includes('skip') && ariaLabel.includes('ad')) ||
                            (className.includes('skip') && (className.includes('ad') || className.includes('ytp')))
                        );
                        
                        if (isSkipButton) {
                            console.log('Found skip button via comprehensive scan:', text || ariaLabel || className);
                            if (safeClick(btn)) return true;
                        }
                    }
                    
                    // Method 3: Look for ad containers and find skip buttons within
                    var adContainers = document.querySelectorAll('.ytp-ad-module, .video-ads, [class*="ad-"], .ytp-ad-text');
                    for (var container of adContainers) {
                        var buttons = container.querySelectorAll('button, [role="button"]');
                        for (var btn of buttons) {
                            if (btn.offsetParent !== null) {
                                console.log('Found button in ad container, trying click...');
                                if (safeClick(btn)) return true;
                            }
                        }
                    }
                    
                    console.log('No skip buttons found');
                    return false;
                """)
                
                if skip_result:
                    print("✅ Successfully skipped ad using JavaScript method")
                    time.sleep(2)
                    return True
                    
            except Exception as e:
                print(f"⚠️ JavaScript skip method failed: {e}")
            
            # Method 3: Wait and retry approach (some ads have countdown)
            try:
                # Look for countdown indicators
                countdown_indicators = [
                    ".ytp-ad-duration-remaining",
                    ".ytp-ad-text", 
                    "[class*='countdown']",
                    "[class*='timer']"
                ]
                
                countdown_found = False
                for indicator_selector in countdown_indicators:
                    countdown_elements = self.driver.find_elements("css selector", indicator_selector)
                    for elem in countdown_elements:
                        if elem.is_displayed():
                            countdown_text = elem.text.strip()
                            if countdown_text and any(char.isdigit() for char in countdown_text):
                                print(f"🕐 Ad countdown detected: '{countdown_text}' - waiting for skip button...")
                                countdown_found = True
                                break
                    if countdown_found:
                        break
                
                if countdown_found:
                    # Wait a bit for skip button to appear
                    for wait_round in range(5):  # Wait up to 5 seconds
                        time.sleep(1)
                        print(f"⏳ Waiting for skip button... ({wait_round + 1}/5)")
                        
                        # Try the first few selectors again
                        for selector in skip_selectors[:8]:  # Try top 8 selectors
                            try:
                                elements = self.driver.find_elements("css selector", selector)
                                for element in elements:
                                    if element.is_displayed() and element.is_enabled():
                                        element.click()
                                        print(f"✅ Skipped ad after countdown wait using: {selector}")
                                        return True
                            except:
                                continue
                                
            except Exception as e:
                print(f"⚠️ Countdown detection failed: {e}")
            
            print("ℹ️ No video ads found to skip")
            return False
            
        except Exception as e:
            print(f"⚠️ Ad skip error: {e}")
            return False

class EnhancedYouTubeAutomation:
    """Enhanced YouTube automation with session management"""
    
    def __init__(self):
        self.session_manager = YouTubeSessionManager()
        self.video_controller = None
        
    def play_youtube_video(self, query: str, stop_current: bool = True) -> Dict[str, Any]:
        """
        Play YouTube video with enhanced controls
        
        Args:
            query: Search query for the video
            stop_current: Whether to stop current video before playing new one
            
        Returns:
            Dict: Result of the operation
        """
        
        print(f"🎵 ENHANCED YOUTUBE AUTOMATION")
        print(f"🔍 Query: {query}")
        print(f"⏹️ Stop current: {stop_current}")
        print("=" * 50)
        
        start_time = time.time()
        
        try:
            # Check network connectivity first
            if not self.session_manager.check_network_connectivity():
                return {
                    "success": False,
                    "error": "Network connectivity issue - unable to reach YouTube",
                    "query": query,
                    "duration_seconds": time.time() - start_time
                }
            
            # Get or create browser session
            driver = self.session_manager.get_active_driver()
            if not driver:
                return {
                    "success": False,
                    "error": "Failed to create browser session",
                    "query": query
                }
            
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.by import By
            from selenium.webdriver.common.keys import Keys
            
            wait = WebDriverWait(driver, 15)
            self.video_controller = YouTubeVideoController(driver, wait)
            
            # Step 1: Handle current video if requested
            if stop_current and self.session_manager.current_video_url:
                print("⏹️ Stopping current video...")
                self.video_controller.stop_current_video()
                time.sleep(1)
            
            # Step 2: Navigate to YouTube homepage (natural behavior)
            search_url = f"https://www.youtube.com"
            print(f"� Searching directly: {search_url}")
            driver.get(search_url)
            
            # Wait for page load
            time.sleep(4)
            
            # Ensure we're on desktop version
            if "m.youtube.com" in driver.current_url:
                print("🔄 Force switching to desktop YouTube...")
                desktop_search_url = f"https://www.youtube.com&force_desktop=1"
                driver.get(desktop_search_url)
                time.sleep(3)
                
                # Human-like delay and behavior
                time.sleep(random.uniform(2, 4))
                
                # Simulate human scrolling behavior
                driver.execute_script("window.scrollBy(0, 200);")
                time.sleep(random.uniform(0.5, 1.5))
                driver.execute_script("window.scrollBy(0, -100);")
                time.sleep(random.uniform(0.5, 1))
            
            # Step 3: Close any popups/ads with enhanced detection
            print("🚫 Handling popups and ads...")
            self.video_controller.close_popups_and_ads()
            
            # Step 4: Perform natural search using search box
            print(f"🔍 Searching for: {query}")
            
            # Find search box with multiple strategies
            search_box = None
            search_selectors = [
                "input[name='search_query']",
                "#search-input input", 
                "input[placeholder*='Search']",
                "ytd-searchbox input",
                "#searchbox input"
            ]
            
            for selector in search_selectors:
                try:
                    search_box = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    print(f"✅ Found search box with: {selector}")
                    break
                except:
                    continue
            
            if search_box:
                # Human-like search interaction
                search_box.click()
                time.sleep(random.uniform(0.3, 0.8))
                search_box.clear()
                time.sleep(random.uniform(0.2, 0.5))
                
                # Type with human-like delays
                for char in query:
                    search_box.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.15))
                
                time.sleep(random.uniform(0.8, 1.5))
                search_box.send_keys(Keys.RETURN)
                print("⌨️ Search submitted")
            else:
                print("⚠️ Could not find search box, trying fallback")
                # Fallback: use URL navigation
                search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
                driver.get(search_url)
            
            time.sleep(3)
            
            # Add necessary imports for search
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support import expected_conditions as EC
            
            # Additional popup check after search results load
            self.video_controller.close_popups_and_ads()
            
            # SKIP SEARCH BOX - WE'RE ALREADY ON SEARCH RESULTS PAGE

            
            # Step 6: Find and click best matching video
            print("🎬 Looking for best matching video...")
            
            video_selectors = [
                "a#video-title",
                "ytd-video-renderer a#video-title",
                "a[href*='/watch?v=']",
                ".ytd-video-renderer .ytd-thumbnail a"
            ]
            
            best_video = None
            video_title = "Unknown Video"
            best_relevance_score = 0
            
            # Get all videos and score them for relevance
            all_videos = []
            for selector in video_selectors:
                try:
                    videos = driver.find_elements(By.CSS_SELECTOR, selector)
                    for video in videos:
                        if video.is_displayed():
                            title = video.get_attribute("title") or video.text or ""
                            if title and len(title) > 5:  # Skip empty or very short titles
                                all_videos.append((video, title))
                    if all_videos:
                        break
                except:
                    continue
            
            print(f"🔍 Found {len(all_videos)} videos, selecting first available...")
            
            # Use first available video for now (simple approach)
            if all_videos:
                first_video = all_videos[0][0]
                video_title = all_videos[0][1]
            
            if not first_video:
                return {
                    "success": False,
                    "error": "No videos found in search results",
                    "query": query
                }
            
            print(f"🎵 Found: {video_title}")
            
            # Step 7: Click video with retry mechanism
            print("▶️ Clicking to play...")
            
            for attempt in range(3):
                try:
                    # Scroll into view
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_video)
                    time.sleep(1)
                    
                    # Click using JavaScript to avoid interception
                    driver.execute_script("arguments[0].click();", first_video)
                    break
                    
                except Exception as e:
                    print(f"⚠️ Click attempt {attempt + 1} failed: {e}")
                    if attempt == 2:
                        return {
                            "success": False,
                            "error": f"Failed to click video after 3 attempts: {e}",
                            "query": query
                        }
                    time.sleep(1)
            
            # Step 8: Enhanced video loading and continuous ad monitoring
            print("⏳ Waiting for video to load...")
            time.sleep(random.uniform(2, 3))
            
            # Multi-stage ad checking with better timing
            ad_check_stages = [
                {"name": "immediate", "delay": 0, "description": "Checking for immediate ads"},
                {"name": "early", "delay": 2, "description": "Checking for early-load ads"},
                {"name": "delayed", "delay": 4, "description": "Checking for delayed ads"},
                {"name": "final", "delay": 6, "description": "Final ad check"}
            ]
            
            ads_skipped = 0
            for stage in ad_check_stages:
                if stage["delay"] > 0:
                    time.sleep(stage["delay"])
                
                print(f"🎬 {stage['description']}...")
                ad_skipped = self.video_controller.skip_video_ads_only()
                if ad_skipped:
                    ads_skipped += 1
                    print(f"✅ Skipped ad in {stage['name']} stage (total: {ads_skipped})")
                    time.sleep(1)  # Brief pause after successful skip
                else:
                    print(f"ℹ️ No ads found in {stage['name']} stage")
            
            # Additional continuous monitoring for 10 seconds
            print("🔄 Starting continuous ad monitoring...")
            monitoring_start = time.time()
            monitoring_duration = 10  # Monitor for 10 seconds
            
            while time.time() - monitoring_start < monitoring_duration:
                time.sleep(2)  # Check every 2 seconds
                
                # Quick ad check
                try:
                    quick_ad_check = self.driver.execute_script("""
                        // Quick check for any visible skip buttons
                        var skipButtons = document.querySelectorAll('.ytp-ad-skip-button, .ytp-skip-ad-button, button[aria-label*="Skip"]');
                        for (var btn of skipButtons) {
                            if (btn.offsetParent !== null) {
                                return true;
                            }
                        }
                        return false;
                    """)
                    
                    if quick_ad_check:
                        print("� Continuous monitoring detected ad - attempting skip...")
                        ad_skipped = self.video_controller.skip_video_ads_only()
                        if ad_skipped:
                            ads_skipped += 1
                            print(f"✅ Continuous monitoring skipped ad (total: {ads_skipped})")
                        
                except Exception as e:
                    print(f"⚠️ Continuous monitoring error: {e}")
                    break
            
            print(f"📊 Ad monitoring completed. Total ads skipped: {ads_skipped}")
            
            # Wait a bit more for full load
            time.sleep(random.uniform(1, 2))
            
            # Only check for errors if there's obvious trouble (no constant checking)
            try:
                page_title = driver.title.lower()
                if "youtube" not in page_title or len(page_title) < 5:
                    print("⚠️ Page seems problematic, checking for errors...")
                    error_found = self.video_controller.handle_youtube_errors()
                    if error_found:
                        time.sleep(3)
            except:
                pass
            
            # Store current video info
            self.session_manager.current_video_url = driver.current_url
            self.session_manager.last_query = query
            
            # Add human-like behavior after video loads
            if STEALTH_AVAILABLE:
                print("👤 Simulating human viewing behavior...")
                stealth_browser.simulate_human_behavior(driver)
                stealth_browser.random_delay(1, 3)
            else:
                # Basic human simulation without stealth browser
                time.sleep(random.uniform(1, 2))
            
            # Step 9: Minimal popup handling (much less aggressive)
            print("🚫 Quick popup check...")
            if not hasattr(self.video_controller, '_last_popup_cleanup'):
                self.video_controller._last_popup_cleanup = 0
            
            if time.time() - self.video_controller._last_popup_cleanup > 60:  # Max once per minute
                self.video_controller.close_popups_and_ads()
                self.video_controller._last_popup_cleanup = time.time()
            else:
                print("⏭️ Skipping popup cleanup (too recent)")
                time.sleep(2)  # Just wait a bit instead
            
            # Step 10: Verify video is playing
            try:
                # Check if video element exists and is playing
                video_playing = driver.execute_script("""
                    var videos = document.querySelectorAll('video');
                    for (var i = 0; i < videos.length; i++) {
                        if (!videos[i].paused && videos[i].currentTime > 0) {
                            return true;
                        }
                    }
                    return false;
                """)
                
                if video_playing:
                    print("✅ Video is playing!")
                    print("🎉 Successfully started YouTube video without disruption")
                    
                else:
                    print("⚠️ Video may not be playing, will check once more...")
                    # Only do one gentle check, no loops
                    try:
                        play_button = driver.find_element("css selector", ".ytp-play-button")
                        if play_button.is_displayed():
                            play_button.click()
                            print("✅ Clicked play button")
                    except:
                        pass
                    
            except:
                print("ℹ️ Could not verify video playback status")
            
            duration = time.time() - start_time
            
            return {
                "success": True,
                "method": "enhanced_session_management",
                "query": query,
                "video_title": video_title,
                "url": self.session_manager.current_video_url,
                "duration_seconds": round(duration, 2),
                "popups_handled": True,
                "message": f"Successfully playing '{video_title}' with enhanced controls"
            }
            
        except Exception as e:
            print(f"❌ Enhanced automation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "query": query,
                "duration_seconds": round(time.time() - start_time, 2)
            }
    
    def stop_current_video(self) -> Dict[str, Any]:
        """Stop currently playing video"""
        
        if not self.session_manager.session_active:
            return {
                "success": False,
                "error": "No active YouTube session"
            }
        
        try:
            if self.video_controller:
                success = self.video_controller.stop_current_video()
                return {
                    "success": success,
                    "action": "video_stopped",
                    "message": "Current video stopped" if success else "Could not stop video"
                }
            else:
                return {
                    "success": False,
                    "error": "Video controller not initialized"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def close_session(self) -> Dict[str, Any]:
        """Close the YouTube session"""
        
        try:
            self.session_manager.cleanup_session()
            return {
                "success": True,
                "action": "session_closed",
                "message": "YouTube session closed successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_session_status(self) -> Dict[str, Any]:
        """Get current session status"""
        
        return {
            "session_active": self.session_manager.session_active,
            "current_video": self.session_manager.current_video_url,
            "last_query": self.session_manager.last_query,
            "driver_alive": self.session_manager.active_driver is not None
        }

# Global instance for persistent session
_youtube_automation = None

def get_youtube_automation():
    """Get global YouTube automation instance"""
    global _youtube_automation
    if _youtube_automation is None:
        _youtube_automation = EnhancedYouTubeAutomation()
    return _youtube_automation

# Main functions for MCP integration
def enhanced_youtube_play(query: str, stop_current: bool = True) -> Dict[str, Any]:
    """
    Play YouTube video with enhanced session management
    
    Args:
        query: Search query for the video  
        stop_current: Whether to stop current video first
        
    Returns:
        Dict: Result of the operation
    """
    
    automation = get_youtube_automation()
    return automation.play_youtube_video(query, stop_current)

def enhanced_youtube_stop() -> Dict[str, Any]:
    """Stop currently playing YouTube video"""
    
    automation = get_youtube_automation()
    return automation.stop_current_video()

def enhanced_youtube_close() -> Dict[str, Any]:
    """Close YouTube session"""
    
    automation = get_youtube_automation()
    return automation.close_session()

def enhanced_youtube_status() -> Dict[str, Any]:
    """Get YouTube session status"""
    
    automation = get_youtube_automation()
    return automation.get_session_status()

# Test functions
def test_enhanced_youtube():
    """Test the enhanced YouTube automation"""
    
    print("🧪 TESTING ENHANCED YOUTUBE AUTOMATION")
    print("=" * 50)
    
    # Test 1: Play a video
    print("\n🎵 Test 1: Playing Alka Yagnik songs...")
    result1 = enhanced_youtube_play("Alka Yagnik best songs", stop_current=False)
    print(f"Result: {'SUCCESS' if result1['success'] else 'FAILED'}")
    if result1.get('error'):
        print(f"Error: {result1['error']}")
    
    time.sleep(5)
    
    # Test 2: Stop and play different video
    print("\n🎵 Test 2: Stopping and playing Kasoor songs...")
    result2 = enhanced_youtube_play("Kasoor movie songs", stop_current=True)
    print(f"Result: {'SUCCESS' if result2['success'] else 'FAILED'}")
    if result2.get('error'):
        print(f"Error: {result2['error']}")
    
    # Test 3: Check status
    print("\n📊 Test 3: Checking session status...")
    status = enhanced_youtube_status()
    print(f"Session active: {status['session_active']}")
    print(f"Current video: {status.get('current_video', 'None')}")
    
    print("\n✅ Enhanced YouTube automation testing completed!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Use command line argument as song query
        song_query = " ".join(sys.argv[1:])
        print(f"🧪 TESTING ENHANCED YOUTUBE AUTOMATION")
        print("=" * 50)
        print(f"🎵 Playing: {song_query}")
        
        result = enhanced_youtube_play(song_query, stop_current=False)
        print(f"Result: {'SUCCESS' if result['success'] else 'FAILED'}")
        if result.get('error'):
            print(f"Error: {result['error']}")
        
        # Wait a bit to see if it works
        time.sleep(10)
        
        # Check status
        status = enhanced_youtube_status()
        print(f"\n📊 Status: {status}")
    else:
        # Run default tests
        test_enhanced_youtube()
