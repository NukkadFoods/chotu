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
        """Set up Chrome driver with anti-detection measures"""
        if not SELENIUM_AVAILABLE:
            raise ImportError("Selenium is required for web automation")
        
        options = Options()
        
        if self.headless:
            options.add_argument('--headless')
        
        # Anti-detection measures
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Stealth options
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-web-security')
        options.add_argument('--disable-features=VizDisplayCompositor')
        
        # User agent and window size for natural browsing
        options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Preferences for natural behavior
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
            "profile.managed_default_content_settings.images": 1 if not self.disable_images else 2
        }
        options.add_experimental_option("prefs", prefs)
        
        try:
            # Use the fixed ChromeDriver path
            from selenium.webdriver.chrome.service import Service
            
            # Try to use the local ChromeDriver first (version 138)
            local_chromedriver = "/Users/mahendrabahubali/chotu/mcp/tools/chromedriver-mac-x64/chromedriver"
            
            if os.path.exists(local_chromedriver):
                service = Service(executable_path=local_chromedriver)
                self.driver = webdriver.Chrome(service=service, options=options)
                print("✅ Using local ChromeDriver 138")
            else:
                # Fallback to system ChromeDriver
                self.driver = webdriver.Chrome(options=options)
                print("✅ Using system ChromeDriver")
            
            # Execute anti-detection script
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.driver.implicitly_wait(3)
            self.driver.set_window_size(1366, 768)  # More common resolution
            print("✅ Chrome driver initialized with stealth mode")
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
        """Perform a Google search with CAPTCHA detection"""
        if not self.navigate_to("https://google.com"):
            return False
        
        try:
            self._rate_limit_check()
            
            # Check for CAPTCHA or unusual traffic detection
            if self._check_for_captcha():
                print("🤖 CAPTCHA detected - waiting for manual resolution or trying alternative approach")
                return self._handle_captcha_situation(query)
            
            # Find search box with multiple strategies
            search_selectors = ['input[name="q"]', 'textarea[name="q"]', '#searchbox input']
            search_box = None
            
            for selector in search_selectors:
                try:
                    search_box = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    break
                except TimeoutException:
                    continue
            
            if not search_box:
                print("❌ Could not find search box")
                return False
            
            # Human-like typing
            search_box.clear()
            self._human_like_typing(search_box, query)
            
            # Add small delay before pressing enter
            time.sleep(0.5 + (time.time() % 0.5))  # Random delay 0.5-1s
            search_box.send_keys(Keys.RETURN)
            
            # Wait for results
            time.sleep(2)
            
            # Check if CAPTCHA appeared after search
            if self._check_for_captcha():
                print("🤖 Post-search CAPTCHA detected")
                return self._handle_captcha_situation(query)
            
            print(f"🔍 Google search completed: {query}")
            return True
            
        except Exception as e:
            print(f"❌ Google search failed: {e}")
            return False
    
    def _check_for_captcha(self) -> bool:
        """Check if CAPTCHA or unusual traffic page is displayed"""
        try:
            captcha_indicators = [
                "unusual traffic",
                "captcha",
                "recaptcha",
                "verify you're not a robot",
                "prove you're not a robot",
                "security check"
            ]
            
            page_text = self.driver.page_source.lower()
            page_title = self.driver.title.lower()
            
            for indicator in captcha_indicators:
                if indicator in page_text or indicator in page_title:
                    return True
            
            # Check for specific CAPTCHA elements
            captcha_selectors = [
                '.g-recaptcha',
                '#recaptcha',
                '[data-recaptcha]',
                '.captcha',
                'iframe[src*="recaptcha"]'
            ]
            
            for selector in captcha_selectors:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if element:
                        return True
                except NoSuchElementException:
                    continue
            
            return False
            
        except Exception as e:
            print(f"⚠️ Error checking for CAPTCHA: {e}")
            return False
    
    def _handle_captcha_situation(self, original_query: str) -> bool:
        """Handle CAPTCHA situation with alternative strategies"""
        print("🔄 Implementing CAPTCHA bypass strategies...")
        
        # Strategy 1: Wait and retry
        print("   Strategy 1: Waiting for manual resolution (10 seconds)...")
        time.sleep(10)
        
        if not self._check_for_captcha():
            print("   ✅ CAPTCHA resolved, continuing with search")
            return self.search_google(original_query)
        
        # Strategy 2: Try DuckDuckGo as alternative
        print("   Strategy 2: Switching to DuckDuckGo...")
        if self._search_duckduckgo(original_query):
            return True
        
        # Strategy 3: Direct site navigation
        print("   Strategy 3: Attempting direct site navigation...")
        return self._try_direct_navigation(original_query)
    
    def _search_duckduckgo(self, query: str) -> bool:
        """Use DuckDuckGo as alternative search engine"""
        try:
            if not self.navigate_to("https://duckduckgo.com"):
                return False
            
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            
            search_box.clear()
            self._human_like_typing(search_box, query)
            search_box.send_keys(Keys.RETURN)
            
            print(f"🦆 DuckDuckGo search completed: {query}")
            return True
            
        except Exception as e:
            print(f"❌ DuckDuckGo search failed: {e}")
            return False
    
    def _try_direct_navigation(self, query: str) -> bool:
        """Try to navigate directly to common sites based on query"""
        # Common site mappings
        site_mappings = {
            'amazon': 'https://amazon.com',
            'youtube': 'https://youtube.com',
            'facebook': 'https://facebook.com',
            'twitter': 'https://twitter.com',
            'instagram': 'https://instagram.com',
            'linkedin': 'https://linkedin.com',
            'github': 'https://github.com',
            'stackoverflow': 'https://stackoverflow.com',
            'reddit': 'https://reddit.com',
            'wikipedia': 'https://wikipedia.org'
        }
        
        query_lower = query.lower()
        for site, url in site_mappings.items():
            if site in query_lower:
                print(f"🎯 Direct navigation to {site}")
                return self.navigate_to(url)
        
        print("❌ No direct navigation option found")
        return False
    
    def _human_like_typing(self, element, text: str):
        """Type text in a human-like manner with random delays"""
        for char in text:
            element.send_keys(char)
            # Random delay between keystrokes (50-150ms)
            time.sleep(0.05 + (time.time() % 0.1))
    
    def click_first_search_result(self, search_query: str = "") -> bool:
        """Click the first search result on Google or DuckDuckGo"""
        try:
            self._rate_limit_check()
            
            # Check if we're on DuckDuckGo or Google
            current_url = self.driver.current_url.lower()
            
            if 'duckduckgo' in current_url:
                return self._click_first_duckduckgo_result(search_query)
            else:
                return self._click_first_google_result(search_query)
            
        except Exception as e:
            print(f"❌ Click first search result failed: {e}")
            return False
    
    def _click_first_google_result(self, search_query: str) -> bool:
        """Click first result on Google search with improved element handling"""
        # Common selectors for Google search results
        result_selectors = [
            'h3 a',  # Standard title links
            '.g h3 a',  # Result group title links
            '[data-ved] h3 a',  # Data-ved title links
            '.yuRUbf a',  # New Google layout
            '.r a',  # Classic layout
            'a[href*="/url?q="]'  # URL redirect links
        ]
        
        for selector in result_selectors:
            try:
                # Wait for search results to load
                results = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                )
                
                if results:
                    first_result = results[0]
                    
                    # Try multiple click strategies
                    success = self._try_multiple_click_strategies(first_result, search_query)
                    if success:
                        print(f"✅ Clicked first Google search result for: {search_query}")
                        return True
                    
            except TimeoutException:
                continue
            except Exception as e:
                print(f"⚠️ Google selector {selector} failed: {e}")
                continue
        
        print(f"❌ No clickable Google search results found for: {search_query}")
        return False
    
    def _try_multiple_click_strategies(self, element, search_query: str) -> bool:
        """Try multiple strategies to click an element"""
        
        # Strategy 1: Scroll into view and regular click
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.5)
            element.click()
            return True
        except Exception as e:
            print(f"🔄 Regular click failed: {str(e)[:100]}...")
        
        # Strategy 2: JavaScript click
        try:
            print("🔄 Trying JavaScript click...")
            self.driver.execute_script("arguments[0].click();", element)
            return True
        except Exception as e:
            print(f"🔄 JavaScript click failed: {e}")
        
        # Strategy 3: Actions click
        try:
            print("🔄 Trying Actions click...")
            from selenium.webdriver.common.action_chains import ActionChains
            actions = ActionChains(self.driver)
            actions.move_to_element(element).click().perform()
            return True
        except Exception as e:
            print(f"🔄 Actions click failed: {e}")
        
        # Strategy 4: Get href and navigate directly
        try:
            print("🔄 Trying direct navigation...")
            href = element.get_attribute('href')
            if href and href.startswith('http'):
                self.driver.get(href)
                return True
        except Exception as e:
            print(f"🔄 Direct navigation failed: {e}")
        
        # Strategy 5: Send Enter key to element
        try:
            print("🔄 Trying Enter key...")
            element.send_keys(Keys.RETURN)
            return True
        except Exception as e:
            print(f"🔄 Enter key failed: {e}")
        
        return False
    
    def _click_first_duckduckgo_result(self, search_query: str) -> bool:
        """Click first result on DuckDuckGo search with improved element handling"""
        # DuckDuckGo result selectors
        result_selectors = [
            '.result__title a',  # Standard DuckDuckGo results
            '.result h2 a',      # Alternative layout
            'a[data-testid="result-title-a"]',  # New layout
            '.result__a'         # Direct result links
        ]
        
        for selector in result_selectors:
            try:
                # Wait for search results to load
                results = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                )
                
                if results:
                    first_result = results[0]
                    
                    # Try multiple click strategies
                    success = self._try_multiple_click_strategies(first_result, search_query)
                    if success:
                        print(f"✅ Clicked first DuckDuckGo search result for: {search_query}")
                        return True
                    
            except TimeoutException:
                continue
            except Exception as e:
                print(f"⚠️ DuckDuckGo selector {selector} failed: {e}")
                continue
        
        print(f"❌ No clickable DuckDuckGo search results found for: {search_query}")
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
    
    def search(self, query: str) -> bool:
        """
        Wrapper method for search functionality
        Calls search_google for consistency with test expectations
        """
        try:
            return self.search_google(query)
        except Exception as e:
            print(f"⚠️ Search failed: {e}")
            return False
    
    def scroll_down(self, pixels: int = 300) -> bool:
        """
        Scroll down the page
        
        Args:
            pixels: Number of pixels to scroll down
            
        Returns:
            bool: True if scroll was successful
        """
        try:
            if not self.driver:
                print("❌ No browser session active")
                return False
            
            self._rate_limit_check()
            
            # Scroll down using JavaScript
            self.driver.execute_script(f"window.scrollBy(0, {pixels});")
            
            # Small delay to allow page to settle
            import time
            time.sleep(1)
            
            print(f"✅ Scrolled down {pixels} pixels")
            return True
            
        except Exception as e:
            print(f"❌ Scroll failed: {e}")
            return False
    
    def scroll_up(self, pixels: int = 300) -> bool:
        """
        Scroll up the page
        
        Args:
            pixels: Number of pixels to scroll up
            
        Returns:
            bool: True if scroll was successful
        """
        try:
            if not self.driver:
                print("❌ No browser session active")
                return False
            
            self._rate_limit_check()
            
            # Scroll up using JavaScript (negative pixels)
            self.driver.execute_script(f"window.scrollBy(0, -{pixels});")
            
            # Small delay to allow page to settle
            import time
            time.sleep(1)
            
            print(f"✅ Scrolled up {pixels} pixels")
            return True
            
        except Exception as e:
            print(f"❌ Scroll up failed: {e}")
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
