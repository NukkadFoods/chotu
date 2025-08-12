"""
Chotu Password Manager - Secure credential storage and auto-login functionality
"""
import json
import os
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime
import hashlib
from cryptography.fernet import Fernet
import base64

class PasswordManager:
    """Secure password storage and automatic login functionality"""
    
    def __init__(self, vault_path: str = "autonomous/memory/passwordVault.json"):
        self.vault_path = Path(vault_path)
        self.vault_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize encryption key
        self.key = self._get_or_create_key()
        self.cipher = Fernet(self.key)
        
        # Load existing passwords
        self.passwords = self._load_passwords()
        
        self.logger = logging.getLogger(__name__)
    
    def _get_or_create_key(self) -> bytes:
        """Get or create encryption key for password storage"""
        key_file = self.vault_path.parent / ".vault_key"
        
        if key_file.exists():
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            # Generate new key
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    def _load_passwords(self) -> List[Dict]:
        """Load passwords from vault file"""
        try:
            if self.vault_path.exists():
                with open(self.vault_path, 'r') as f:
                    data = json.load(f)
                    return data.get('passwords', [])
            return []
        except Exception as e:
            self.logger.error(f"Failed to load passwords: {e}")
            return []
    
    def vault_exists(self) -> bool:
        """Check if password vault file exists"""
        return self.vault_path.exists()
    
    def list_credentials(self) -> List[str]:
        """List all stored credential domains"""
        return [pwd['service'] for pwd in self.passwords]
    
    def _save_passwords(self):
        """Save passwords to vault file"""
        try:
            vault_data = {
                "passwords": self.passwords,
                "last_updated": datetime.now().isoformat()
            }
            
            with open(self.vault_path, 'w') as f:
                json.dump(vault_data, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Failed to save passwords: {e}")
    
    def extract_domain(self, url: str) -> str:
        """Extract domain name from URL"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            # Remove www. prefix
            if domain.startswith('www.'):
                domain = domain[4:]
                
            # Remove common TLD for matching (e.g., instagram.com -> instagram)
            if '.' in domain:
                return domain.split('.')[0]
            return domain
            
        except Exception:
            return url.lower()
    
    def get_credentials(self, service: str) -> Optional[Tuple[str, str]]:
        """Get stored credentials for a service"""
        service_domain = self.extract_domain(service)
        
        for cred in self.passwords:
            stored_service = self.extract_domain(cred.get('service', ''))
            if stored_service == service_domain:
                try:
                    # Decrypt password if it's encrypted
                    password = cred['password']
                    if password.startswith('enc:'):
                        encrypted_password = password[4:].encode()
                        password = self.cipher.decrypt(encrypted_password).decode()
                    
                    return cred['username'], password
                except Exception as e:
                    self.logger.error(f"Failed to decrypt password for {service}: {e}")
                    # Fallback to plain text (for existing unencrypted passwords)
                    return cred['username'], cred['password']
        
        return None
    
    def save_credentials(self, service: str, username: str, password: str, 
                        encrypt: bool = True) -> bool:
        """Save new credentials to vault"""
        try:
            service_domain = self.extract_domain(service)
            
            # Check if credentials already exist
            existing_index = None
            for i, cred in enumerate(self.passwords):
                if self.extract_domain(cred.get('service', '')) == service_domain:
                    existing_index = i
                    break
            
            # Encrypt password if requested
            stored_password = password
            if encrypt:
                encrypted_password = self.cipher.encrypt(password.encode())
                stored_password = f"enc:{encrypted_password.decode()}"
            
            new_cred = {
                "username": username,
                "password": stored_password,
                "service": service,
                "created_at": datetime.now().isoformat(),
                "last_used": datetime.now().isoformat()
            }
            
            if existing_index is not None:
                # Update existing credentials
                self.passwords[existing_index] = new_cred
                self.logger.info(f"Updated credentials for {service}")
            else:
                # Add new credentials
                self.passwords.append(new_cred)
                self.logger.info(f"Saved new credentials for {service}")
            
            self._save_passwords()
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save credentials for {service}: {e}")
            return False
    
    def update_last_used(self, service: str):
        """Update last used timestamp for a service"""
        service_domain = self.extract_domain(service)
        
        for cred in self.passwords:
            if self.extract_domain(cred.get('service', '')) == service_domain:
                cred['last_used'] = datetime.now().isoformat()
                self._save_passwords()
                break
    
    def delete_credentials(self, service: str) -> bool:
        """Delete credentials for a service"""
        try:
            service_domain = self.extract_domain(service)
            
            original_length = len(self.passwords)
            self.passwords = [
                cred for cred in self.passwords 
                if self.extract_domain(cred.get('service', '')) != service_domain
            ]
            
            if len(self.passwords) < original_length:
                self._save_passwords()
                self.logger.info(f"Deleted credentials for {service}")
                return True
            else:
                self.logger.warning(f"No credentials found for {service}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to delete credentials for {service}: {e}")
            return False
    
    def list_services(self) -> List[str]:
        """List all services with stored credentials"""
        return [cred.get('service', '') for cred in self.passwords]
    
    def detect_login_form(self, driver) -> Optional[Dict[str, str]]:
        """Detect login form elements on current page"""
        try:
            from selenium.webdriver.common.by import By
            
            # Common login form selectors
            username_selectors = [
                'input[type="email"]',
                'input[type="text"][name*="user"]',
                'input[type="text"][name*="email"]',
                'input[name="username"]',
                'input[name="email"]',
                'input[id*="user"]',
                'input[id*="email"]',
                'input[placeholder*="email"]',
                'input[placeholder*="username"]',
                '#username', '#user', '#email',
                '.username', '.user', '.email'
            ]
            
            password_selectors = [
                'input[type="password"]',
                'input[name="password"]',
                'input[name="pass"]',
                '#password', '#pass',
                '.password', '.pass'
            ]
            
            login_elements = {}
            
            # Find username/email field
            for selector in username_selectors:
                try:
                    element = driver.find_element(By.CSS_SELECTOR, selector)
                    if element.is_displayed():
                        login_elements['username'] = selector
                        break
                except:
                    continue
            
            # Find password field
            for selector in password_selectors:
                try:
                    element = driver.find_element(By.CSS_SELECTOR, selector)
                    if element.is_displayed():
                        login_elements['password'] = selector
                        break
                except:
                    continue
            
            # Find submit button
            submit_selectors = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button:contains("Log in")',
                'button:contains("Sign in")',
                'button:contains("Login")',
                '[role="button"]:contains("Log in")',
                '.login-button', '.signin-button',
                '#login', '#signin'
            ]
            
            for selector in submit_selectors:
                try:
                    element = driver.find_element(By.CSS_SELECTOR, selector)
                    if element.is_displayed():
                        login_elements['submit'] = selector
                        break
                except:
                    continue
            
            if 'username' in login_elements and 'password' in login_elements:
                return login_elements
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to detect login form: {e}")
            return None
    
    def auto_login(self, driver, service: str) -> bool:
        """Automatically login to a service using stored credentials"""
        try:
            # Get stored credentials
            credentials = self.get_credentials(service)
            if not credentials:
                self.logger.info(f"No stored credentials found for {service}")
                return False
            
            username, password = credentials
            
            # Detect login form
            login_form = self.detect_login_form(driver)
            if not login_form:
                self.logger.warning(f"No login form detected on {service}")
                return False
            
            # Fill in credentials
            from selenium.webdriver.common.by import By
            import time
            
            # Fill username
            username_element = driver.find_element(By.CSS_SELECTOR, login_form['username'])
            username_element.clear()
            time.sleep(0.5)
            username_element.send_keys(username)
            time.sleep(1)
            
            # Fill password
            password_element = driver.find_element(By.CSS_SELECTOR, login_form['password'])
            password_element.clear()
            time.sleep(0.5)
            password_element.send_keys(password)
            time.sleep(1)
            
            # Submit form
            if 'submit' in login_form:
                submit_element = driver.find_element(By.CSS_SELECTOR, login_form['submit'])
                submit_element.click()
            else:
                # Fallback: press Enter on password field
                from selenium.webdriver.common.keys import Keys
                password_element.send_keys(Keys.RETURN)
            
            # Update last used timestamp
            self.update_last_used(service)
            
            self.logger.info(f"Auto-login attempted for {service}")
            return True
            
        except Exception as e:
            self.logger.error(f"Auto-login failed for {service}: {e}")
            return False
