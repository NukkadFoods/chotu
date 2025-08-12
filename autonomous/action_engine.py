"""
Chotu Action Engine - Advanced Browser and System Automation
Implements stealth browser control and OS-level interactions
"""
import time
import random
import json
import os
from typing import List, Dict, Tuple, Optional, Any, Union
from dataclasses import dataclass
from pathlib import Path
import logging

# Browser automation imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium_stealth import stealth
import undetected_chromedriver as uc

# System automation imports
import pyautogui
from .vision_engine import VisionEngine, ScreenRegion
from .password_manager import PasswordManager

@dataclass
class HumanBehavior:
    """Settings for human-like automation behavior"""
    typing_speed_range: Tuple[float, float] = (0.05, 0.15)  # seconds per character
    mouse_speed_range: Tuple[float, float] = (0.5, 1.5)     # seconds for movement
    click_delay_range: Tuple[float, float] = (0.1, 0.3)     # seconds before/after click
    scroll_delay_range: Tuple[float, float] = (0.2, 0.8)    # seconds between scrolls
    page_load_wait_range: Tuple[float, float] = (2.0, 5.0)  # seconds to wait for page load
    
@dataclass
class StealthSettings:
    """Browser stealth and fingerprint masking settings"""
    user_agent: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    viewport_size: Tuple[int, int] = (1366, 768)
    timezone: str = "America/New_York"
    language: str = "en-US,en;q=0.9"
    disable_images: bool = False
    disable_javascript: bool = False
    use_proxy: bool = False
    proxy_server: Optional[str] = None

class ActionEngine:
    """Advanced automation engine for stealth browser and system control"""
    
    # Class-level browser registry to share instances
    _browser_instances = {}
    _current_browser_id = None
    
    def __init__(self, vision_engine: VisionEngine, headless: bool = False):
        self.vision = vision_engine
        self.headless = headless
        
        # Initialize password manager
        self.password_manager = PasswordManager()
        
        # Behavior settings
        self.human_behavior = HumanBehavior()
        self.stealth_settings = StealthSettings()
        
        # Browser instance
        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None
        
        # Action history
        self.action_history: List[Dict] = []
        
        # Configure PyAutoGUI for human-like behavior
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def create_stealth_browser(self) -> bool:
        """Create or reuse undetected Chrome browser with stealth features"""
        try:
            # Check if we have an existing browser instance
            if ActionEngine._current_browser_id and ActionEngine._current_browser_id in ActionEngine._browser_instances:
                existing_driver = ActionEngine._browser_instances[ActionEngine._current_browser_id]
                try:
                    # Test if the browser is still responsive
                    existing_driver.current_url
                    self.driver = existing_driver
                    self.wait = WebDriverWait(self.driver, 30)
                    self.logger.info("Reusing existing browser instance")
                    return True
                except:
                    # Browser is dead, remove it from registry
                    del ActionEngine._browser_instances[ActionEngine._current_browser_id]
                    ActionEngine._current_browser_id = None
                    self.logger.info("Existing browser instance is dead, creating new one")
            
            # Suppress Selenium warnings and logs
            import logging
            import warnings
            
            # Suppress specific warnings
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            logging.getLogger('selenium').setLevel(logging.ERROR)
            logging.getLogger('urllib3').setLevel(logging.ERROR)
            
            # Fix SSL certificate issue on macOS
            import ssl
            import certifi
            import os
            import urllib3
            
            # Disable SSL warnings
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            
            # Set SSL certificate verification
            os.environ['SSL_CERT_FILE'] = certifi.where()
            os.environ['PYTHONHTTPSVERIFY'] = '0'
            
            # Create unverified SSL context to avoid certificate errors
            ssl._create_default_https_context = ssl._create_unverified_context
            
            # Chrome options for stealth
            options = uc.ChromeOptions()
            
            if self.headless:
                options.add_argument("--headless")
            
            # Stealth options
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-plugins")
            
            # Suppress Chrome logs and warnings
            options.add_argument("--disable-logging")
            options.add_argument("--log-level=3")
            options.add_argument("--silent")
            options.add_argument("--disable-gpu-sandbox")
            
            options.add_argument("--disable-images") if self.stealth_settings.disable_images else None
            options.add_argument("--disable-javascript") if self.stealth_settings.disable_javascript else None
            
            # Fingerprint masking
            options.add_argument(f"--user-agent={self.stealth_settings.user_agent}")
            options.add_argument(f"--window-size={self.stealth_settings.viewport_size[0]},{self.stealth_settings.viewport_size[1]}")
            
            # Proxy settings
            if self.stealth_settings.use_proxy and self.stealth_settings.proxy_server:
                options.add_argument(f"--proxy-server={self.stealth_settings.proxy_server}")
            
            # Additional stealth options
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Create undetected Chrome driver with SSL fix
            try:
                # Fix SSL certificate issue on macOS - suppress warnings
                import ssl
                import certifi
                import os
                import urllib3
                
                # Disable SSL warnings
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                
                # Set SSL certificate verification
                os.environ['SSL_CERT_FILE'] = certifi.where()
                os.environ['PYTHONHTTPSVERIFY'] = '0'
                
                # Create unverified SSL context to avoid certificate errors
                ssl._create_default_https_context = ssl._create_unverified_context
                
                self.driver = uc.Chrome(options=options, version_main=None)
                
            except Exception as ssl_error:
                # Suppress SSL error logging to reduce noise
                self.logger.info("Using fallback ChromeDriver (SSL download unavailable)")
                
                # Try to use system ChromeDriver or existing installation
                from selenium import webdriver
                from selenium.webdriver.chrome.service import Service
                
                # Use system Chrome with regular selenium as fallback
                service = Service()
                chrome_options = webdriver.ChromeOptions()
                
                # Copy the stealth options to regular Chrome options
                for arg in options.arguments:
                    chrome_options.add_argument(arg)
                
                for option_name, option_value in options.experimental_options.items():
                    chrome_options.add_experimental_option(option_name, option_value)
                
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Apply stealth settings
            stealth(self.driver,
                   languages=[self.stealth_settings.language],
                   vendor="Google Inc.",
                   platform="MacIntel",
                   webgl_vendor="Intel Inc.",
                   renderer="Intel Iris OpenGL Engine",
                   fix_hairline=True)
            
            # Configure WebDriverWait
            self.wait = WebDriverWait(self.driver, 30)
            
            # Register the browser instance for reuse
            import uuid
            browser_id = str(uuid.uuid4())
            ActionEngine._browser_instances[browser_id] = self.driver
            ActionEngine._current_browser_id = browser_id
            
            self.logger.info("Stealth browser created successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create stealth browser: {e}")
            return False
    
    def navigate_to_url(self, url: str, verify_load: bool = True) -> bool:
        """Navigate to URL with human-like behavior and verification"""
        try:
            if not self.driver:
                if not self.create_stealth_browser():
                    return False
            
            self.logger.info(f"Navigating to: {url}")
            
            # Human-like navigation
            self.driver.get(url)
            
            # Wait for page load with random delay
            load_wait = random.uniform(*self.human_behavior.page_load_wait_range)
            time.sleep(load_wait)
            
            if verify_load:
                # Verify page loaded successfully
                if not self._verify_page_load(url):
                    return False
            
            # Check for auto-login opportunity
            self._try_auto_login(url)
            
            self._record_action("navigate", {"url": url, "success": True})
            return True
            
        except Exception as e:
            self.logger.error(f"Navigation failed: {e}")
            self._record_action("navigate", {"url": url, "success": False, "error": str(e)})
            return False
    
    def open_new_tab(self) -> bool:
        """Open a new browser tab"""
        try:
            if not self.driver:
                if not self.create_stealth_browser():
                    return False
            
            self.logger.info("Opening new browser tab")
            
            # Method 1: Try JavaScript approach
            try:
                self.driver.execute_script("window.open('about:blank', '_blank');")
                
                # Switch to the new tab
                self.driver.switch_to.window(self.driver.window_handles[-1])
                
                # Add human-like delay
                time.sleep(random.uniform(0.5, 1.5))
                
                self._record_action("new_tab", {"success": True})
                return True
                
            except Exception:
                # Method 2: Fallback to keyboard shortcut
                from selenium.webdriver.common.keys import Keys
                from selenium.webdriver.common.action_chains import ActionChains
                
                actions = ActionChains(self.driver)
                actions.key_down(Keys.COMMAND).send_keys('t').key_up(Keys.COMMAND).perform()
                
                time.sleep(random.uniform(0.5, 1.5))
                
                self._record_action("new_tab", {"success": True, "method": "keyboard"})
                return True
            
        except Exception as e:
            self.logger.error(f"Failed to open new tab: {e}")
            self._record_action("new_tab", {"success": False, "error": str(e)})
            return False
    
    def _verify_page_load(self, expected_url: str) -> bool:
        """Verify that page loaded correctly"""
        try:
            # Check if we're on the expected domain
            current_url = self.driver.current_url
            from urllib.parse import urlparse
            
            expected_domain = urlparse(expected_url).netloc
            current_domain = urlparse(current_url).netloc
            
            if expected_domain in current_domain or current_domain in expected_domain:
                # Check if page is fully loaded
                return self.driver.execute_script("return document.readyState") == "complete"
            
            return False
        except Exception:
            return False
    
    def find_element_by_vision(self, element_name: str, timeout: int = 10) -> Optional[Any]:
        """Find web element using computer vision + DOM mapping or CSS selector"""
        try:
            # Check if element_name is a CSS selector (starts with # or .)
            if element_name.startswith('#') or element_name.startswith('.') or element_name.startswith('['):
                return self._find_element_by_css(element_name, timeout)
            
            # First try vision detection
            element_bounds = self.vision.wait_for_element(element_name, timeout)
            if not element_bounds:
                return None
            
            # Get center coordinates
            center_x, center_y = self.vision.get_element_center(element_bounds)
            
            # Try to map vision coordinates to DOM element
            script = f"""
            var element = document.elementFromPoint({center_x}, {center_y});
            if (element) {{
                element.setAttribute('data-chotu-found', 'true');
                return true;
            }}
            return false;
            """
            
            if self.driver.execute_script(script):
                # Find the marked element
                try:
                    return self.driver.find_element(By.CSS_SELECTOR, "[data-chotu-found='true']")
                except:
                    pass
            
            # Fallback: return coordinates for PyAutoGUI
            return {"type": "coordinates", "x": center_x, "y": center_y}
            
        except Exception as e:
            self.logger.error(f"Vision element search failed: {e}")
            return None
    
    def _find_element_by_css(self, css_selector: str, timeout: int = 10) -> Optional[Any]:
        """Find element using CSS selector with wait"""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
            self.logger.info(f"Found element with CSS selector: {css_selector}")
            return element
        except Exception as e:
            self.logger.warning(f"CSS selector '{css_selector}' not found: {e}")
            # Try alternative selectors for common elements
            return self._try_alternative_selectors(css_selector, timeout)
    
    def _try_alternative_selectors(self, original_selector: str, timeout: int = 10) -> Optional[Any]:
        """Try alternative selectors for common elements"""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        
        alternative_selectors = []
        
        # For YouTube search box
        if 'search_query' in original_selector or ('search' in original_selector and 'youtube' in self.driver.current_url.lower()):
            alternative_selectors = [
                "input[name='search_query']",
                "input[id='search']",
                "#search input",
                "input[placeholder*='Search']",
                "ytd-searchbox input",
                "#masthead-search input",
                ".ytd-searchbox input",
                "form[role='search'] input"
            ]
        # For Amazon search box
        elif 'twotabsearch' in original_selector or ('search' in original_selector and 'amazon' in self.driver.current_url.lower()):
            alternative_selectors = [
                "input[name='field-keywords']",
                "input[placeholder*='Search']",
                "input[type='search']",
                "#nav-search-input input",
                "input[data-testid='search-input']",
                "input.nav-input",
                "form[role='search'] input"
            ]
        # For Google search box
        elif 'search' in original_selector and 'google' in self.driver.current_url.lower():
            alternative_selectors = [
                "input[name='q']",
                "input[title='Search']",
                "#search input",
                "form[role='search'] input",
                ".gLFyf"
            ]
        
        for selector in alternative_selectors:
            try:
                wait = WebDriverWait(self.driver, 2)  # Shorter timeout for alternatives
                element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                self.logger.info(f"Found element with alternative selector: {selector}")
                return element
            except:
                continue
        
        return None
    
    def human_click(self, element: Union[Any, Dict], offset: Tuple[int, int] = (0, 0)) -> bool:
        """Perform human-like click with randomized timing and movement"""
        try:
            if isinstance(element, dict) and element.get("type") == "coordinates":
                # Direct coordinate click using PyAutoGUI
                x, y = element["x"] + offset[0], element["y"] + offset[1]
                
                # Human-like mouse movement
                duration = random.uniform(*self.human_behavior.mouse_speed_range)
                pyautogui.moveTo(x, y, duration=duration, tween=pyautogui.easeOutQuad)
                
                # Pre-click delay
                time.sleep(random.uniform(*self.human_behavior.click_delay_range))
                
                # Click
                pyautogui.click()
                
                # Post-click delay
                time.sleep(random.uniform(*self.human_behavior.click_delay_range))
                
            else:
                # Selenium WebElement click
                # Add randomized offset to avoid detection
                action = ActionChains(self.driver)
                action.move_to_element_with_offset(element, offset[0], offset[1])
                
                # Human-like delay before click
                time.sleep(random.uniform(*self.human_behavior.click_delay_range))
                
                action.click().perform()
                
                # Post-click delay
                time.sleep(random.uniform(*self.human_behavior.click_delay_range))
            
            self._record_action("click", {"success": True})
            return True
            
        except Exception as e:
            self.logger.error(f"Human click failed: {e}")
            self._record_action("click", {"success": False, "error": str(e)})
            return False
    
    def human_type(self, element: Union[Any, Dict], text: str, clear_first: bool = True) -> bool:
        """Type text with human-like timing and behavior"""
        try:
            if isinstance(element, dict) and element.get("type") == "coordinates":
                # Click field first
                if not self.human_click(element):
                    return False
                
                # Clear field if requested
                if clear_first:
                    pyautogui.hotkey('cmd', 'a')  # Select all (macOS)
                    time.sleep(0.1)
                
                # Type with human-like speed
                for char in text:
                    pyautogui.typewrite(char)
                    delay = random.uniform(*self.human_behavior.typing_speed_range)
                    time.sleep(delay)
                    
            else:
                # Selenium WebElement typing
                if clear_first:
                    element.clear()
                
                # Type with human-like behavior
                for char in text:
                    element.send_keys(char)
                    delay = random.uniform(*self.human_behavior.typing_speed_range)
                    time.sleep(delay)
            
            self._record_action("type", {"text": text, "success": True})
            return True
            
        except Exception as e:
            self.logger.error(f"Human typing failed: {e}")
            self._record_action("type", {"text": text, "success": False, "error": str(e)})
            return False
    
    def human_scroll(self, direction: str = "down", amount: int = 3) -> bool:
        """Perform human-like scrolling"""
        try:
            if direction == "down":
                scroll_amount = -amount * 100
            else:
                scroll_amount = amount * 100
            
            # Random scrolling pattern
            for _ in range(amount):
                pyautogui.scroll(scroll_amount // amount)
                delay = random.uniform(*self.human_behavior.scroll_delay_range)
                time.sleep(delay)
            
            self._record_action("scroll", {"direction": direction, "amount": amount, "success": True})
            return True
            
        except Exception as e:
            self.logger.error(f"Human scroll failed: {e}")
            self._record_action("scroll", {"direction": direction, "amount": amount, "success": False, "error": str(e)})
            return False
    
    def wait_for_page_change(self, timeout: int = 30) -> bool:
        """Wait for page to change (new URL or significant DOM changes)"""
        try:
            initial_url = self.driver.current_url
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                current_url = self.driver.current_url
                
                # Check for URL change
                if current_url != initial_url:
                    return True
                
                # Check for DOM changes (placeholder - could be enhanced)
                ready_state = self.driver.execute_script("return document.readyState")
                if ready_state == "complete":
                    time.sleep(1)  # Give it a moment to settle
                    return True
                
                time.sleep(0.5)
            
            return False
            
        except Exception as e:
            self.logger.error(f"Wait for page change failed: {e}")
            return False
    
    def handle_captcha_detection(self) -> bool:
        """Detect and handle CAPTCHA challenges"""
        try:
            # Look for common CAPTCHA indicators
            captcha_indicators = [
                "captcha", "recaptcha", "hcaptcha", 
                "verification", "robot", "human"
            ]
            
            page_source = self.driver.page_source.lower()
            
            for indicator in captcha_indicators:
                if indicator in page_source:
                    self.logger.warning("CAPTCHA detected - requesting human assistance")
                    self._record_action("captcha_detected", {"indicator": indicator})
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"CAPTCHA detection failed: {e}")
            return False
    
    def take_screenshot(self, filename: Optional[str] = None) -> str:
        """Take screenshot for verification or debugging"""
        try:
            if not filename:
                timestamp = int(time.time())
                filename = f"action_screenshot_{timestamp}.png"
            
            screenshot_path = self.vision.screenshots_dir / filename
            
            if self.driver:
                self.driver.save_screenshot(str(screenshot_path))
            else:
                # Fallback to PyAutoGUI
                screenshot = pyautogui.screenshot()
                screenshot.save(screenshot_path)
            
            return str(screenshot_path)
            
        except Exception as e:
            self.logger.error(f"Screenshot failed: {e}")
            return ""
    
    def close_browser(self):
        """Safely close browser"""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
                self.wait = None
                self.logger.info("Browser closed successfully")
        except Exception as e:
            self.logger.error(f"Browser close failed: {e}")
    
    def _record_action(self, action_type: str, details: Dict):
        """Record action for audit trail"""
        record = {
            "timestamp": time.time(),
            "action": action_type,
            "details": details
        }
        self.action_history.append(record)
        
        # Keep only last 1000 actions to prevent memory bloat
        if len(self.action_history) > 1000:
            self.action_history = self.action_history[-1000:]
    
    def get_action_history(self, limit: int = 50) -> List[Dict]:
        """Get recent action history"""
        return self.action_history[-limit:]
    
    def randomize_behavior(self, behavior_profile: str = "normal"):
        """Adjust human behavior settings based on profile"""
        profiles = {
            "conservative": {
                "typing_speed_range": (0.1, 0.3),
                "mouse_speed_range": (1.0, 2.0),
                "click_delay_range": (0.2, 0.5),
                "scroll_delay_range": (0.5, 1.2),
                "page_load_wait_range": (3.0, 6.0)
            },
            "normal": {
                "typing_speed_range": (0.05, 0.15),
                "mouse_speed_range": (0.5, 1.5),
                "click_delay_range": (0.1, 0.3),
                "scroll_delay_range": (0.2, 0.8),
                "page_load_wait_range": (2.0, 5.0)
            },
            "aggressive": {
                "typing_speed_range": (0.02, 0.08),
                "mouse_speed_range": (0.2, 0.8),
                "click_delay_range": (0.05, 0.15),
                "scroll_delay_range": (0.1, 0.4),
                "page_load_wait_range": (1.0, 3.0)
            }
        }
        
        if behavior_profile in profiles:
            profile_settings = profiles[behavior_profile]
            for attr, value in profile_settings.items():
                setattr(self.human_behavior, attr, value)
            
            self.logger.info(f"Behavior profile set to: {behavior_profile}")
    
    def _try_auto_login(self, url: str):
        """Try to automatically login if credentials are available"""
        try:
            # Wait a moment for page to fully load
            time.sleep(2)
            
            # Extract service name from URL
            service = self.password_manager.extract_domain(url)
            
            # Check if we have credentials for this service
            credentials = self.password_manager.get_credentials(service)
            if credentials:
                self.logger.info(f"Found credentials for {service}, attempting auto-login")
                
                # Try auto-login
                if self.password_manager.auto_login(self.driver, service):
                    self.logger.info(f"Auto-login successful for {service}")
                else:
                    self.logger.warning(f"Auto-login failed for {service}")
            else:
                # Monitor for password entry to capture new credentials
                self._monitor_password_entry(service)
                
        except Exception as e:
            self.logger.error(f"Auto-login attempt failed: {e}")
    
    def _monitor_password_entry(self, service: str):
        """Monitor for manual password entry to capture credentials"""
        try:
            # This is a simplified version - in a full implementation,
            # you'd want to monitor form submissions more carefully
            login_form = self.password_manager.detect_login_form(self.driver)
            if login_form:
                self.logger.info(f"Login form detected on {service}, monitoring for credential entry")
                # Store form selectors for later capture
                self._pending_capture = {
                    'service': service,
                    'form': login_form,
                    'timestamp': time.time()
                }
        except Exception as e:
            self.logger.error(f"Failed to monitor password entry: {e}")
    
    def capture_login_credentials(self, service: str, username: str, password: str) -> bool:
        """Manually capture and save login credentials"""
        try:
            success = self.password_manager.save_credentials(service, username, password)
            if success:
                self.logger.info(f"Credentials saved for {service}")
            return success
        except Exception as e:
            self.logger.error(f"Failed to capture credentials: {e}")
            return False
    
    def close_browser(self):
        """Safely close the browser"""
        try:
            if self.driver:
                self.driver.quit()
                
                # Remove from class registry
                if ActionEngine._current_browser_id and ActionEngine._current_browser_id in ActionEngine._browser_instances:
                    del ActionEngine._browser_instances[ActionEngine._current_browser_id]
                    ActionEngine._current_browser_id = None
                
                self.logger.info("Browser closed successfully")
        except Exception as e:
            self.logger.error(f"Error closing browser: {e}")
