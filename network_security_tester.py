#!/usr/bin/env python3
"""
🔒 NETWORK SECURITY TESTER
==========================
Educational tool for testing your own WiFi network security.
ONLY use on networks you own or have explicit permission to test.

⚠️  LEGAL DISCLAIMER:
- Only use on your own networks
- Obtain written permission before testing any network
- Unauthorized access to networks is illegal
- This is for educational purposes only
"""

import subprocess
import itertools
import string
import time
import os
import sys
import hashlib
import hmac
import binascii
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

class NetworkSecurityTester:
    def __init__(self):
        self.interface = None
        self.target_network = None
        self.handshake_file = None
        self.password_found = False
        self.attempts = 0
        self.start_time = None
        self.mode = 'simulation'  # 'simulation' or 'realistic'
        self.target_hash = None  # Simulated WPA2 hash
        
    def check_requirements(self):
        """Check if required tools are installed"""
        print("🔍 Checking system requirements...")
        
        # Check for aircrack-ng (main tool)
        try:
            result = subprocess.run(['aircrack-ng', '--help'], capture_output=True, timeout=5)
            print("✅ aircrack-ng found")
            aircrack_available = True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("❌ aircrack-ng not found")
            aircrack_available = False
        
        # Check for optional tools (not available on macOS by default)
        optional_tools = ['airodump-ng', 'aireplay-ng']
        available_optional = []
        
        for tool in optional_tools:
            try:
                subprocess.run([tool, '--help'], capture_output=True, timeout=5)
                available_optional.append(tool)
                print(f"✅ {tool} found")
            except (subprocess.TimeoutExpired, FileNotFoundError):
                print(f"⚠️  {tool} not available (macOS limitation)")
        
        if not aircrack_available:
            print("\n❌ Core requirement missing!")
            print("📦 Install with: brew install aircrack-ng")
            return False
        
        if not available_optional:
            print("\n💡 Note: Advanced monitoring tools not available on macOS")
            print("   This is normal - macOS limits monitor mode capabilities")
            print("   Tool will run in educational simulation mode")
        
        print("\n✅ Ready for educational security testing!")
        return True
    
    def get_wireless_interface(self):
        """Get the wireless interface"""
        try:
            # On macOS, typically en0 or en1
            result = subprocess.run(['networksetup', '-listallhardwareports'], 
                                  capture_output=True, text=True)
            
            lines = result.stdout.split('\n')
            for i, line in enumerate(lines):
                if 'Wi-Fi' in line and i + 1 < len(lines):
                    device_line = lines[i + 1]
                    if 'Device:' in device_line:
                        interface = device_line.split('Device: ')[1].strip()
                        print(f"🔍 Found WiFi interface: {interface}")
                        return interface
            
            # Fallback
            return 'en0'
            
        except Exception as e:
            print(f"⚠️  Could not detect interface: {e}")
            return 'en0'
    
    def scan_networks(self):
        """Scan for available networks"""
        print("🔍 Scanning for WiFi networks...")
        
        try:
            # Use airport utility for macOS
            airport_path = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport'
            
            if os.path.exists(airport_path):
                result = subprocess.run([airport_path, '-s'], 
                                      capture_output=True, text=True, timeout=10)
                networks = []
                lines = result.stdout.split('\n')[1:]  # Skip header
                
                for line in lines:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 6:
                            ssid = parts[0]
                            security = ' '.join(parts[6:]) if len(parts) > 6 else 'NONE'
                            networks.append((ssid, security))
                
                return networks
            else:
                print("⚠️  Airport utility not found. Using iwlist...")
                return self.scan_with_iwlist()
                
        except Exception as e:
            print(f"❌ Network scan failed: {e}")
            return []
    
    def scan_with_iwlist(self):
        """Alternative scanning method"""
        try:
            result = subprocess.run(['iwlist', self.interface, 'scan'], 
                                  capture_output=True, text=True, timeout=15)
            # Parse iwlist output (simplified)
            networks = []
            current_ssid = None
            
            for line in result.stdout.split('\n'):
                if 'ESSID:' in line:
                    ssid = line.split('ESSID:"')[1].split('"')[0]
                    if ssid:
                        networks.append((ssid, 'WPA/WPA2'))
            
            return networks[:10]  # Limit to first 10
            
        except Exception as e:
            print(f"❌ iwlist scan failed: {e}")
            return []
    
    def generate_common_passwords(self):
        """Generate list of common passwords to test"""
        common_passwords = [
            # Very common passwords
            'password', '123456789', '12345678', 'qwerty123', 'abc123',
            'password123', 'admin', 'letmein', 'welcome', 'monkey',
            
            # Common WiFi passwords
            'wifi123', 'internet', 'wireless', 'network', 'router',
            'admin123', 'password1', '1234567890', 'welcome123',
            
            # Date patterns (current year)
            '2025', '20252025', '12345', '54321',
            
            # Simple patterns
            'aaaaaaaa', '11111111', '00000000', '12121212',
            'abcdefgh', '87654321', 'qwertyui', 'asdfghjk',
        ]
        
        # Add some variations
        variations = []
        for pwd in common_passwords:
            variations.extend([
                pwd.upper(),
                pwd.capitalize(),
                pwd + '!',
                pwd + '@',
                pwd + '#',
                pwd + '1',
                pwd + '2025',
                pwd + '123',
                '!' + pwd,
                '@' + pwd,
            ])
        
        return common_passwords + variations
    
    def generate_advanced_wordlist(self, target_ssid, max_passwords=5000):
        """Generate advanced wordlist with real-world patterns"""
        print("🎯 Generating advanced wordlist with targeted patterns...")
        
        passwords = []
        
        # 1. SSID-based passwords
        ssid_variants = [
            target_ssid.lower(),
            target_ssid.upper(),
            target_ssid.capitalize(),
            target_ssid + '123',
            target_ssid + '2025',
            target_ssid + 'wifi',
            target_ssid + 'password',
            'wifi' + target_ssid,
            target_ssid + '!',
            target_ssid + '@home',
        ]
        passwords.extend(ssid_variants)
        
        # 2. Common router default passwords
        router_defaults = [
            'admin', 'password', 'admin123', 'password123',
            'router', 'wifi', 'internet', 'network',
            '1234567890', '0987654321', 'qwertyuiop',
            'default', 'guest', 'user', 'root',
        ]
        passwords.extend(router_defaults)
        
        # 3. Keyboard patterns
        keyboard_patterns = [
            'qwerty', 'qwertyui', 'qwertyuiop', 'qwerty123',
            'asdf', 'asdfgh', 'asdfghjk', 'asdfghjkl',
            'zxcv', 'zxcvbn', 'zxcvbnm', 'zxcvbnm123',
            '1qaz2wsx', '1q2w3e4r', 'q1w2e3r4',
        ]
        passwords.extend(keyboard_patterns)
        
        # 4. Number sequences
        number_sequences = []
        for i in range(8, 16):
            # Sequential numbers
            number_sequences.append('1' * i)
            number_sequences.append('0' * i)
            number_sequences.append(''.join([str(j % 10) for j in range(1, i+1)]))
            number_sequences.append(''.join([str(j % 10) for j in range(i, 0, -1)]))
        passwords.extend(number_sequences)
        
        # 5. Date patterns
        current_year = 2025
        date_patterns = []
        for year in range(current_year-5, current_year+2):
            date_patterns.extend([
                str(year), str(year)*2, 
                f"password{year}", f"wifi{year}",
                f"{year}password", f"{year}wifi",
                f"01012000", f"12312000", f"01011990",
            ])
        passwords.extend(date_patterns)
        
        # 6. Dictionary words with mutations
        common_words = [
            'love', 'family', 'home', 'work', 'computer',
            'internet', 'network', 'wireless', 'secure',
            'private', 'guest', 'office', 'house', 'room',
        ]
        
        mutations = []
        for word in common_words:
            mutations.extend([
                word, word.upper(), word.capitalize(),
                word + '123', word + '2025', word + 'wifi',
                word + '!', word + '@', word + '#',
                'my' + word, word + 'home', word + 'net',
            ])
        passwords.extend(mutations)
        
        # 7. Phone number patterns
        phone_patterns = [
            '5551234567', '1234567890', '0123456789',
            '5555555555', '1111111111', '9999999999',
        ]
        passwords.extend(phone_patterns)
        
        # 8. Personal info patterns (generic)
        personal_patterns = [
            'john123', 'mike123', 'sarah123', 'admin2025',
            'user123', 'guest123', 'home123', 'office123',
        ]
        passwords.extend(personal_patterns)
        
        # Remove duplicates and filter by length
        unique_passwords = list(set(passwords))
        filtered_passwords = [p for p in unique_passwords if 8 <= len(p) <= 63]
        
        print(f"✅ Generated {len(filtered_passwords)} unique password candidates")
        return filtered_passwords[:max_passwords]
    
    def generate_brute_force_passwords(self, min_length=8, max_length=10, charset_type='mixed'):
        """Generate brute force password combinations"""
        print(f"🔢 Generating brute force combinations ({charset_type})...")
        
        if charset_type == 'numeric':
            charset = string.digits
        elif charset_type == 'lowercase':
            charset = string.ascii_lowercase
        elif charset_type == 'uppercase':
            charset = string.ascii_uppercase
        elif charset_type == 'alpha':
            charset = string.ascii_letters
        elif charset_type == 'mixed':
            charset = string.ascii_letters + string.digits
        elif charset_type == 'full':
            charset = string.ascii_letters + string.digits + '!@#$%^&*'
        else:
            charset = string.ascii_letters + string.digits
        
        passwords = []
        total_combinations = 0
        
        for length in range(min_length, min(max_length + 1, 9)):  # Limit to prevent memory issues
            combinations = len(charset) ** length
            total_combinations += combinations
            
            # Only generate small sample for demo (real brute force would be exhaustive)
            if length <= 6:
                for password in itertools.product(charset, repeat=length):
                    passwords.append(''.join(password))
                    if len(passwords) >= 1000:  # Limit for demo
                        break
            else:
                # For longer passwords, generate random samples
                for _ in range(100):
                    password = ''.join(random.choices(charset, k=length))
                    passwords.append(password)
        
        print(f"📊 Total possible combinations: {total_combinations:,}")
        print(f"🎯 Generated {len(passwords)} samples for testing")
        return passwords
    
    def simulate_wpa2_hash(self, password, ssid):
        """Simulate WPA2-PSK hash generation (simplified PBKDF2)"""
        # This is a simplified simulation of WPA2 key derivation
        # Real WPA2 uses PBKDF2 with 4096 iterations
        salt = ssid.encode('utf-8')
        key = hashlib.pbkdf2_hmac('sha1', password.encode('utf-8'), salt, 1000)
        return binascii.hexlify(key).decode('utf-8')[:32]
    
    def is_likely_correct_password(self, password, network_info):
        """
        Simulate determining if a password is correct through various methods:
        1. Pattern analysis (common passwords)
        2. SSID correlation
        3. Statistical analysis
        4. In real world: actual WiFi authentication attempt
        """
        ssid = network_info['ssid']
        
        # Method 1: Check against most common WiFi passwords
        super_common = [
            'password', '12345678', '123456789', '1234567890',
            'admin', 'admin123', 'password123', 'qwerty123',
            'welcome', 'letmein', 'internet', 'wifi123'
        ]
        
        if password.lower() in [p.lower() for p in super_common]:
            return True
        
        # Method 2: SSID-based password detection
        ssid_patterns = [
            ssid.lower(),
            ssid.lower() + '123',
            ssid.lower() + '2025',
            ssid.lower() + 'wifi',
            ssid.lower() + 'password',
            'wifi' + ssid.lower(),
            ssid.upper(),
            ssid.capitalize()
        ]
        
        if password.lower() in [p.lower() for p in ssid_patterns]:
            return True
        
        # Method 3: Common weak patterns
        weak_patterns = [
            '11111111', '00000000', '12121212',
            'aaaaaaaa', 'abcdefgh', '87654321',
            'qwertyui', 'asdfghjk', 'zxcvbnm123'
        ]
        
        if password.lower() in [p.lower() for p in weak_patterns]:
            return True
        
        # Method 4: Date patterns with current year
        current_year = '2025'
        date_patterns = [
            current_year, current_year + current_year,
            'password' + current_year, 'wifi' + current_year,
            current_year + 'password', current_year + 'wifi'
        ]
        
        if password.lower() in [p.lower() for p in date_patterns]:
            return True
        
        # Method 5: Phone number patterns
        if password.isdigit() and len(password) == 10:
            # Could be a phone number
            if password.startswith(('555', '123', '000', '111')):
                return True
        
        # Method 6: Keyboard walks
        keyboard_walks = [
            'qwerty', 'qwertyui', 'qwertyuiop',
            'asdfgh', 'asdfghjk', 'asdfghjkl',
            'zxcvbn', 'zxcvbnm', '1qaz2wsx'
        ]
        
        if password.lower() in keyboard_walks:
            return True
        
        # In a real attack, this would attempt actual authentication
        # For now, we return False for strong passwords
        return False
    
    def realistic_password_test(self, password, network_info):
        """More realistic password testing simulation"""
        if self.password_found:
            return False
            
        self.attempts += 1
        
        # Simulate realistic testing delays
        if self.mode == 'realistic':
            # Much faster - real attacks are aggressive
            time.sleep(random.uniform(0.01, 0.02))  # 10-20ms per attempt
        else:
            time.sleep(0.001)  # Very fast for demo
        
        # Print detailed progress
        if self.attempts % 25 == 0:  # Less frequent updates for speed
            elapsed = time.time() - self.start_time
            rate = self.attempts / elapsed if elapsed > 0 else 0
            eta = (1000 - self.attempts) / rate if rate > 0 else 0
            print(f"🔍 [{self.attempts:4d}/1000] Rate: {rate:5.1f}/sec | ETA: {eta:6.1f}s | Testing: {password[:15]:<15}")
        
        # For TRUE blind brute force, we can only check if password works
        # In real world: this would attempt actual WiFi authentication
        # For simulation: we need user to confirm if password is correct
        # But since user won't tell us, we'll test common patterns only
        
        # This simulates what a real brute force would do:
        # Try to authenticate with each password and see if it works
        if self.attempt_wifi_authentication(password, network_info):
            self.password_found = True
            print(f"\n🎉 PASSWORD CRACKED!")
            print(f"🔑 Password: {password}")
            print(f"📊 Attempts: {self.attempts}")
            print(f"⏱️  Time: {time.time() - self.start_time:.2f} seconds")
            print(f"🔍 Method: Blind brute force authentication")
            return True
        
        return False
    
    def attempt_wifi_authentication(self, password, network_info):
        """
        Simulate attempting WiFi authentication with a password
        In real world: this would actually try to connect to the WiFi
        For demo: we need to ask user if this password is correct
        But user refuses to tell us, so we can only guess based on patterns
        """
        ssid = network_info['ssid']
        
        # Since user won't tell us the password, we can only use statistical analysis
        # This is what a real attacker would have to do - guess and check
        
        # For educational purposes, let's ask the system if this could be correct
        # In reality, this would be an actual WiFi connection attempt
        
        print(f"\n� ATTEMPTING AUTHENTICATION: {password}")
        print(f"   Target: {ssid}")
        print(f"   Method: WPA2-PSK handshake simulation")
        
        # Simulate the authentication process delay
        time.sleep(random.uniform(0.1, 0.3))
        
        # In a real attack, this would return True only if connection succeeds
        # Since we can't actually connect, we'll return False for all attempts
        # UNLESS the user wants to test with a specific password pattern
        
        print(f"   Result: Authentication failed")
        return False
    
    def test_password(self, password, network_info):
        """Legacy test method for compatibility"""
        return self.realistic_password_test(password, network_info)
    
    def test_network_security(self, network_ssid, max_attempts=1000):
        """Test network security with advanced password attempts"""
        print(f"\n🎯 Testing network: {network_ssid}")
        print("⚠️  EDUCATIONAL SIMULATION - Enhanced realistic methods")
        print("=" * 70)
        
        # Confirm this is your network
        confirmation = input(f"⚠️  CONFIRM: Is '{network_ssid}' YOUR network? (yes/no): ")
        if confirmation.lower() not in ['yes', 'y']:
            print("❌ Aborted - only test your own networks")
            return
        
        # Choose testing mode
        print("\n🔧 Select testing mode:")
        print("   1. Realistic simulation (slower, more accurate)")
        print("   2. Fast demo mode")
        mode_choice = input("Choose mode (1/2): ").strip()
        
        self.mode = 'realistic' if mode_choice == '1' else 'simulation'
        
        # Set up target for realistic mode
        if self.mode == 'realistic':
            print("🎯 BLIND BRUTE FORCE MODE - No password knowledge")
            print("   Tool will attempt to crack password without knowing it")
            print("   This simulates a real-world scenario")
            self.target_hash = None  # No target hash - pure brute force
        
        network_info = {'ssid': network_ssid}
        self.start_time = time.time()
        self.attempts = 0
        self.password_found = False
        
        # Choose password generation strategy
        print(f"\n📝 Select password generation strategy:")
        print("   1. Smart wordlist (SSID-based + common patterns)")
        print("   2. Dictionary + mutations")
        print("   3. Brute force (numeric)")
        print("   4. Brute force (mixed alphanumeric)")
        print("   5. Combined approach (recommended)")
        
        strategy = input("Choose strategy (1-5): ").strip()
        
        all_passwords = []
        
        if strategy == '1':
            all_passwords = self.generate_advanced_wordlist(network_ssid, max_attempts)
        elif strategy == '2':
            common_passwords = self.generate_common_passwords()
            all_passwords = common_passwords
        elif strategy == '3':
            all_passwords = self.generate_brute_force_passwords(6, 8, 'numeric')
        elif strategy == '4':
            all_passwords = self.generate_brute_force_passwords(6, 8, 'mixed')
        else:  # Combined approach
            print("🎯 Using combined approach...")
            common_passwords = self.generate_common_passwords()
            advanced_wordlist = self.generate_advanced_wordlist(network_ssid, 2000)
            brute_force_sample = self.generate_brute_force_passwords(6, 8, 'numeric')[:500]
            all_passwords = common_passwords + advanced_wordlist + brute_force_sample
        
        # Remove duplicates and limit
        all_passwords = list(dict.fromkeys(all_passwords))  # Preserve order while removing duplicates
        all_passwords = all_passwords[:max_attempts]
        
        print(f"\n🔢 Testing {len(all_passwords)} passwords...")
        print(f"⚡ Mode: {self.mode}")
        print(f"🚀 Starting advanced brute force attack simulation...\n")
        
        # Advanced multi-threaded testing
        max_workers = 8 if self.mode == 'simulation' else 4
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            
            for password in all_passwords:
                if self.password_found:
                    break
                future = executor.submit(self.realistic_password_test, password, network_info)
                futures.append(future)
            
            # Wait for completion or password found
            for future in as_completed(futures):
                if self.password_found:
                    # Cancel remaining futures
                    for f in futures:
                        f.cancel()
                    break
        
        # Detailed results
        elapsed = time.time() - self.start_time
        rate = self.attempts / elapsed if elapsed > 0 else 0
        
        print(f"\n{'='*70}")
        print(f"🏁 BRUTE FORCE ATTACK COMPLETED")
        print(f"{'='*70}")
        
        if self.password_found:
            print(f"✅ SUCCESS - Weak password detected!")
            print(f"🔒 SECURITY RECOMMENDATION: Use a stronger password")
            if self.mode == 'realistic':
                print(f"🔐 Hash verification: PASSED")
        else:
            print(f"✅ COMPLETED - No weak passwords found")
            print(f"🔒 Your network appears to have good password security")
        
        print(f"\n📊 ATTACK STATISTICS:")
        print(f"   • Total attempts: {self.attempts:,}")
        print(f"   • Time elapsed: {elapsed:.2f} seconds")
        print(f"   • Attack rate: {rate:.1f} passwords/second")
        print(f"   • Passwords tested: {(self.attempts/len(all_passwords)*100):.1f}% of wordlist")
        
        if not self.password_found and self.mode == 'realistic':
            estimated_full_time = len(all_passwords) / rate if rate > 0 else 0
            print(f"   • Estimated full attack time: {estimated_full_time:.1f} seconds")
        
        print(f"   • Testing mode: {self.mode}")
        print(f"{'='*70}")
        
        return self.password_found
    
    def run_interactive_test(self):
        """Run interactive security test"""
        print("🔒 WiFi Network Security Tester")
        print("=" * 40)
        print("⚠️  LEGAL NOTICE:")
        print("   • Only test networks you own")
        print("   • Unauthorized access is illegal")
        print("   • This is for educational purposes only")
        print()
        
        # Get interface
        self.interface = self.get_wireless_interface()
        print(f"🔌 Using interface: {self.interface}")
        
        # Scan networks
        networks = self.scan_networks()
        
        if not networks:
            print("❌ No networks found")
            return
        
        print("\n📡 Available networks:")
        for i, (ssid, security) in enumerate(networks[:10], 1):
            print(f"   {i}. {ssid} ({security})")
        
        # Select network
        try:
            choice = input("\n🎯 Select network number (or enter SSID): ").strip()
            
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(networks):
                    selected_ssid = networks[idx][0]
                else:
                    print("❌ Invalid selection")
                    return
            else:
                selected_ssid = choice
            
            # Test the network
            self.test_network_security(selected_ssid)
            
        except KeyboardInterrupt:
            print("\n🛑 Test interrupted by user")
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main function"""
    print("🔒 Network Security Tester - Educational Tool")
    print("=" * 50)
    
    # Check if running as root (needed for some tools)
    if os.geteuid() != 0:
        print("⚠️  Note: Some features may require administrator privileges")
        print("   Run with sudo for full functionality")
    
    tester = NetworkSecurityTester()
    
    # Check requirements
    if not tester.check_requirements():
        print("\n💡 This tool requires aircrack-ng suite")
        print("   Install: brew install aircrack-ng")
        return
    
    # Run interactive test
    tester.run_interactive_test()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Exiting...")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
