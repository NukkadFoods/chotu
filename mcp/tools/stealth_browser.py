#!/usr/bin/env python3
"""
🕵️ STEALTH BROWSER FOR CHOTU AI
===============================
Advanced anti-detection browser setup to prevent YouTube blocking
"""

import random
import time
import os
from typing import Optional

# SSL Configuration
try:
    import ssl
    import certifi
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
except:
    pass

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    # Silently skip - selenium is optional for main functionality

try:
    import undetected_chromedriver as uc
    UNDETECTED_AVAILABLE = True
except ImportError:
    UNDETECTED_AVAILABLE = False
    # Silent fail - optional dependency

try:
    from fake_useragent import UserAgent
    FAKE_UA_AVAILABLE = True
except ImportError:
    FAKE_UA_AVAILABLE = False
    # Silent fail - optional dependency

class StealthBrowser:
    """Advanced stealth browser for YouTube automation"""
    
    def __init__(self):
        self.driver = None
        self.session_active = False
        
    def get_stealth_driver(self, headless: bool = False) -> Optional[webdriver.Chrome]:
        """Create a stealth browser instance - UNDETECTED ONLY"""
        
        if not UNDETECTED_AVAILABLE:
            raise Exception("Undetected ChromeDriver required! Install: pip install undetected-chromedriver")
        
        # ONLY use undetected driver - no fallbacks
        return self._get_undetected_driver(headless)
    
    def _get_undetected_driver(self, headless: bool = False) -> Optional[webdriver.Chrome]:
        """Create undetected ChromeDriver (best option)"""
        try:
            print("🕵️ Creating undetected ChromeDriver...")
            
            # Configure options
            options = uc.ChromeOptions()
            
            if headless:
                options.add_argument("--headless=new")
            
            # Randomize window size
            width = random.randint(1200, 1600)
            height = random.randint(800, 1200)
            options.add_argument(f"--window-size={width},{height}")
            
            # Additional stealth options
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-web-security")
            options.add_argument("--ignore-ssl-errors")
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--allow-running-insecure-content")
            
            # DNS and network configuration
            options.add_argument("--dns-prefetch-disable")
            options.add_argument("--disable-background-networking")
            options.add_argument("--disable-domain-reliability")
            options.add_argument("--disable-sync")
            options.add_argument("--disable-background-timer-throttling")
            options.add_argument("--host-resolver-rules=MAP www.youtube.com 142.250.80.110")
            options.add_argument("--remote-debugging-port=0")
            
            # Create driver with SSL configuration and correct Chrome version
            # Use local ChromeDriver path
            local_chromedriver = "/Users/mahendrabahubali/chotu/mcp/tools/chromedriver-mac-x64/chromedriver"
            if os.path.exists(local_chromedriver):
                driver = uc.Chrome(
                    options=options, 
                    version_main=138, 
                    use_subprocess=False,
                    driver_executable_path=local_chromedriver
                )
            else:
                driver = uc.Chrome(
                    options=options, 
                    version_main=138, 
                    use_subprocess=False
                )
            
            # Execute additional stealth scripts
            self._execute_stealth_scripts(driver)
            
            print("✅ Undetected ChromeDriver created successfully")
            return driver
            
        except Exception as e:
            print(f"❌ Failed to create undetected driver: {e}")
            return self._get_standard_stealth_driver(headless)
    
    def _get_standard_stealth_driver(self, headless: bool = False) -> Optional[webdriver.Chrome]:
        """Create standard stealth ChromeDriver"""
        try:
            print("🔧 Creating standard stealth ChromeDriver...")
            
            options = Options()
            
            # Core stealth settings
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            if headless:
                options.add_argument("--headless=new")
            
            # Randomize window size
            width = random.randint(1200, 1600)
            height = random.randint(800, 1200)
            options.add_argument(f"--window-size={width},{height}")
            
            # Random user agent
            user_agent = self._get_random_user_agent()
            options.add_argument(f"--user-agent={user_agent}")
            
            # Additional stealth options
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-web-security")
            options.add_argument("--disable-features=VizDisplayCompositor")
            options.add_argument("--disable-ipc-flooding-protection")
            options.add_argument("--disable-renderer-backgrounding")
            options.add_argument("--disable-backgrounding-occluded-windows")
            options.add_argument("--disable-client-side-phishing-detection")
            
            # DNS and network configuration
            options.add_argument("--dns-prefetch-disable")
            options.add_argument("--disable-background-networking")
            options.add_argument("--disable-domain-reliability")
            options.add_argument("--disable-sync")
            options.add_argument("--disable-background-timer-throttling")
            options.add_argument("--host-resolver-rules=MAP www.youtube.com 142.250.80.110")
            options.add_argument("--remote-debugging-port=0")
            
            # Preferences
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
            
            # Create driver
            driver = webdriver.Chrome(options=options)
            
            # Execute stealth scripts
            self._execute_stealth_scripts(driver)
            
            print("✅ Standard stealth ChromeDriver created successfully")
            return driver
            
        except Exception as e:
            print(f"❌ Failed to create standard stealth driver: {e}")
            return None
    
    def _get_random_user_agent(self) -> str:
        """Get a random realistic user agent"""
        
        if FAKE_UA_AVAILABLE:
            try:
                ua = UserAgent()
                return ua.random
            except:
                pass
        
        # Fallback user agents
        user_agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0"
        ]
        
        return random.choice(user_agents)
    
    def _execute_stealth_scripts(self, driver):
        """Execute JavaScript to enhance stealth"""
        try:
            stealth_script = """
            // Remove webdriver property
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            // Mock plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            // Mock languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
            
            // Mock chrome object
            window.chrome = {
                runtime: {},
            };
            
            // Override permissions
            const originalQuery = window.navigator.permissions.query;
            return window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
            
            // Mock hardware concurrency
            Object.defineProperty(navigator, 'hardwareConcurrency', {
                get: () => 4,
            });
            
            // Mock device memory
            Object.defineProperty(navigator, 'deviceMemory', {
                get: () => 8,
            });
            
            // Hide automation indicators
            delete navigator.__proto__.webdriver;
            """
            
            driver.execute_script(stealth_script)
            print("✅ Stealth scripts executed")
            
        except Exception as e:
            print(f"⚠️ Stealth script execution failed: {e}")
    
    def simulate_human_behavior(self, driver):
        """Simulate human-like behavior"""
        try:
            from selenium.webdriver.common.action_chains import ActionChains
            
            # Random mouse movements
            actions = ActionChains(driver)
            
            # Move to random positions
            for _ in range(random.randint(2, 5)):
                x = random.randint(100, 800)
                y = random.randint(100, 600)
                actions.move_by_offset(x, y).perform()
                time.sleep(random.uniform(0.1, 0.3))
            
            # Random scrolling
            scroll_amount = random.randint(100, 500)
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(0.5, 1.5))
            
            # Scroll back a bit
            scroll_back = random.randint(50, 200)
            driver.execute_script(f"window.scrollBy(0, -{scroll_back});")
            time.sleep(random.uniform(0.3, 0.8))
            
        except Exception as e:
            print(f"⚠️ Human behavior simulation failed: {e}")
    
    def random_delay(self, min_seconds: float = 0.5, max_seconds: float = 2.0):
        """Add random delay to mimic human timing"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)

# Global instance
stealth_browser = StealthBrowser()

def create_stealth_driver(headless: bool = False):
    """Convenience function to create stealth driver"""
    return stealth_browser.get_stealth_driver(headless)

    def create_stealth_driver(self, headless: bool = False) -> Optional[webdriver.Chrome]:
        """Create the most stealth driver possible - entry point for enhanced automation"""
        return self.get_stealth_driver(headless)

if __name__ == "__main__":
    # Test the stealth browser
    print("🧪 Testing Stealth Browser...")
    
    driver = create_stealth_driver(headless=False)
    if driver:
        print("✅ Stealth browser created successfully")
        
        # Test navigation
        driver.get("https://www.youtube.com")
        time.sleep(5)
        
        # Simulate human behavior
        stealth_browser.simulate_human_behavior(driver)
        
        print("🎉 Test completed. Check if YouTube detects automation.")
        input("Press Enter to close browser...")
        driver.quit()
    else:
        print("❌ Failed to create stealth browser")
