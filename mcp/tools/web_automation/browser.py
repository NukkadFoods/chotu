#!/usr/bin/env python3
"""
🌐 CHOTU WEB BROWSER CONTROLLER
==============================
Enhanced browser control with safety mechanisms
"""

import os
import sys
import time
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("⚠️ Selenium not installed. Web automation will be limited.")

class WebCommander:
    """Enhanced browser controller with safety mechanisms"""
    
    def __init__(self, headless: bool = False, disable_images: bool = True):
        self.driver = None
        self.headless = headless
        self.disable_images = disable_images
        self.action_count = 0
        self.action_limit = 5  # Max 5 actions per second
        self.last_action_time = 0
        self.session_start = datetime.now()
        
        # Safety settings
        self.safety_mode = True
        self.confirm_destructive = True
        self.max_retries = 3
        
        # Load web profiles
        self.profiles = self._load_web_profiles()
        
        print(f"🌐 WebCommander initialized")
        print(f"   Safety Mode: {'ON' if self.safety_mode else 'OFF'}")
        print(f"   Headless: {'ON' if self.headless else 'OFF'}")
    
    def _load_web_profiles(self) -> Dict:
        """Load site-specific configuration profiles"""
        profiles = {}
        profiles_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                   "config", "web_profiles")
        
        if os.path.exists(profiles_dir):
            for file in os.listdir(profiles_dir):
                if file.endswith('.json'):
                    site_name = file[:-5]  # Remove .json
                    try:
                        with open(os.path.join(profiles_dir, file), 'r') as f:
                            profiles[site_name] = json.load(f)
                    except Exception as e:
                        print(f"⚠️ Failed to load profile {site_name}: {e}")
        
        return profiles
    
    def _rate_limit_check(self):
        """Enforce action rate limiting for safety"""
        current_time = time.time()
        
        if current_time - self.last_action_time < 0.2:  # Max 5 actions per second
            sleep_time = 0.2 - (current_time - self.last_action_time)
            time.sleep(sleep_time)
        
        self.last_action_time = time.time()
        self.action_count += 1
    
    def _setup_driver(self):
        """Set up Chrome driver with optimized options"""
        if not SELENIUM_AVAILABLE:
            raise ImportError("Selenium is required for web automation")
        
        options = Options()
        
        if self.headless:
            options.add_argument('--headless')
        
        if self.disable_images:
            prefs = {"profile.managed_default_content_settings.images": 2}
            options.add_experimental_option("prefs", prefs)
        
        # Security and performance options
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-web-security')
        options.add_argument('--disable-features=VizDisplayCompositor')
        
        try:
            self.driver = webdriver.Chrome(options=options)
            self.driver.implicitly_wait(3)
            self.driver.set_window_size(1920, 1080)
            print("✅ Chrome driver initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize Chrome driver: {e}")
            return False
    
    def start_session(self) -> bool:
        """Start a new web automation session"""
        if self.driver:
            print("⚠️ Session already active")
            return True
        
        return self._setup_driver()
    
    def end_session(self):
        """End the web automation session safely"""
        if self.driver:
            try:
                # Clear cookies for privacy
                self.driver.delete_all_cookies()
                self.driver.quit()
                self.driver = None
                
                session_duration = (datetime.now() - self.session_start).total_seconds()
                print(f"✅ Web session ended")
                print(f"   Duration: {session_duration:.1f} seconds")
                print(f"   Actions performed: {self.action_count}")
                
            except Exception as e:
                print(f"⚠️ Error ending session: {e}")
    
    def navigate_to(self, url: str) -> bool:
        """Navigate to a URL with safety checks"""
        if not self.driver:
            if not self.start_session():
                return False
        
        self._rate_limit_check()
        
        try:
            # Basic URL validation
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            print(f"🌐 Navigating to: {url}")
            self.driver.get(url)
            
            # Wait for page load
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            print(f"✅ Successfully loaded: {self.driver.title}")
            return True
            
        except Exception as e:
            print(f"❌ Navigation failed: {e}")
            return False
    
    def search_google(self, query: str) -> bool:
        """Perform a Google search"""
        if not self.navigate_to("https://google.com"):
            return False
        
        try:
            self._rate_limit_check()
            
            # Find search box
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            
            print(f"🔍 Google search completed: {query}")
            return True
            
        except Exception as e:
            print(f"❌ Google search failed: {e}")
            return False
    
    def find_element_smart(self, target: str, by_type: str = "auto") -> Optional[Any]:
        """Smart element finding with multiple strategies"""
        if not self.driver:
            return None
        
        strategies = []
        
        if by_type == "auto":
            # Try multiple strategies
            strategies = [
                (By.ID, target),
                (By.NAME, target),
                (By.CLASS_NAME, target),
                (By.XPATH, f"//*[contains(text(), '{target}')]"),
                (By.CSS_SELECTOR, target),
                (By.PARTIAL_LINK_TEXT, target)
            ]
        else:
            # Use specific strategy
            strategy_map = {
                "id": By.ID,
                "name": By.NAME,
                "class": By.CLASS_NAME,
                "xpath": By.XPATH,
                "css": By.CSS_SELECTOR,
                "text": By.PARTIAL_LINK_TEXT
            }
            if by_type in strategy_map:
                strategies = [(strategy_map[by_type], target)]
        
        for by, value in strategies:
            try:
                element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((by, value))
                )
                print(f"✅ Found element using {by}: {value}")
                return element
            except TimeoutException:
                continue
        
        print(f"❌ Element not found: {target}")
        return None
    
    def click_element(self, target: str, confirm: bool = None) -> bool:
        """Click an element with safety confirmation"""
        if confirm is None:
            confirm = self.confirm_destructive
        
        element = self.find_element_smart(target)
        if not element:
            return False
        
        try:
            self._rate_limit_check()
            
            # Check if action might be destructive
            element_text = element.text.lower()
            destructive_keywords = ['buy', 'purchase', 'delete', 'remove', 'pay', 'submit payment']
            
            if confirm and any(keyword in element_text for keyword in destructive_keywords):
                print(f"⚠️ Potentially destructive action detected: {element_text}")
                print("   This action has been blocked for safety")
                return False
            
            # Scroll element into view
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            time.sleep(0.5)
            
            # Click the element
            element.click()
            print(f"✅ Clicked element: {target}")
            return True
            
        except Exception as e:
            print(f"❌ Click failed: {e}")
            return False
    
    def fill_form_field(self, target: str, value: str) -> bool:
        """Fill a form field"""
        element = self.find_element_smart(target)
        if not element:
            return False
        
        try:
            self._rate_limit_check()
            
            # Clear and fill
            element.clear()
            element.send_keys(value)
            
            print(f"✅ Filled field {target}: {value}")
            return True
            
        except Exception as e:
            print(f"❌ Form fill failed: {e}")
            return False
    
    def extract_text(self, target: str) -> Optional[str]:
        """Extract text from an element"""
        element = self.find_element_smart(target)
        if not element:
            return None
        
        try:
            text = element.text.strip()
            print(f"📄 Extracted text: {text[:50]}...")
            return text
            
        except Exception as e:
            print(f"❌ Text extraction failed: {e}")
            return None
    
    def take_screenshot(self, filename: str = None) -> str:
        """Take a screenshot for debugging"""
        if not self.driver:
            return None
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        try:
            screenshots_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                         "logs", "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            
            filepath = os.path.join(screenshots_dir, filename)
            self.driver.save_screenshot(filepath)
            
            print(f"📸 Screenshot saved: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Screenshot failed: {e}")
            return None
    
    def get_page_info(self) -> Dict[str, str]:
        """Get current page information"""
        if not self.driver:
            return {}
        
        try:
            return {
                "title": self.driver.title,
                "url": self.driver.current_url,
                "domain": self.driver.current_url.split('/')[2] if '/' in self.driver.current_url else "",
                "ready_state": self.driver.execute_script("return document.readyState")
            }
        except Exception as e:
            print(f"⚠️ Could not get page info: {e}")
            return {}
    
    def wait_for_element(self, target: str, timeout: int = 10) -> bool:
        """Wait for an element to appear"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{target}')]"))
            )
            return element is not None
        except TimeoutException:
            return False

# Example usage
if __name__ == "__main__":
    commander = WebCommander(headless=False)
    
    if commander.start_session():
        # Test basic functionality
        commander.search_google("Python selenium tutorial")
        time.sleep(2)
        commander.take_screenshot()
        commander.end_session()
