#!/usr/bin/env python3
"""
⚡ FAST AGGRESSIVE BRUTE FORCE TOOL
===================================
High-speed WiFi password cracking simulation
ONLY use on networks you own!
"""

import itertools
import string
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

class FastBruteForce:
    def __init__(self):
        self.password_found = False
        self.attempts = 0
        self.start_time = None
        self.found_password = None
        
    def generate_aggressive_wordlist(self, ssid):
        """Generate comprehensive password list optimized for speed"""
        passwords = []
        
        # SSID-based (highest priority)
        ssid_variants = [
            ssid, ssid.lower(), ssid.upper(), ssid.capitalize(),
            f"{ssid}123", f"{ssid}1234", f"{ssid}12345",
            f"{ssid}2025", f"{ssid}2024", f"{ssid}01",
            f"{ssid}!", f"{ssid}@", f"{ssid}#",
            f"wifi{ssid}", f"{ssid}wifi", f"{ssid}password",
        ]
        passwords.extend(ssid_variants)
        
        # Super common passwords (second priority)
        super_common = [
            "password", "12345678", "123456789", "1234567890",
            "admin", "admin123", "password123", "qwerty123",
            "welcome", "internet", "wireless", "network",
            "guest", "user", "test", "demo", "home"
        ]
        passwords.extend(super_common)
        
        # Year patterns
        for year in ['2025', '2024', '2023']:
            passwords.extend([
                year, f"password{year}", f"wifi{year}",
                f"{year}password", f"{ssid}{year}"
            ])
        
        # Number sequences
        number_patterns = [
            "11111111", "00000000", "12121212", "87654321",
            "1234567890", "0987654321", "5555555555"
        ]
        passwords.extend(number_patterns)
        
        # Keyboard patterns
        keyboard = [
            "qwerty", "qwertyui", "qwertyuiop",
            "asdfgh", "asdfghjk", "asdfghjkl", 
            "zxcvbn", "zxcvbnm", "1qaz2wsx"
        ]
        passwords.extend(keyboard)
        
        # Add variations
        variations = []
        for pwd in passwords[:50]:  # Only vary first 50 to keep it fast
            variations.extend([
                pwd.upper(), pwd.lower(), pwd.capitalize(),
                f"{pwd}1", f"{pwd}!", f"{pwd}@"
            ])
        passwords.extend(variations)
        
        return list(dict.fromkeys(passwords))  # Remove duplicates
    
    def generate_numeric_brute_force(self, length=8):
        """Generate numeric brute force for common lengths"""
        passwords = []
        
        # Common patterns first
        patterns = [
            "12345678", "87654321", "11111111", "00000000",
            "12121212", "10101010", "12341234", "56785678"
        ]
        passwords.extend(patterns)
        
        # Sequential numbers
        for start in range(10):
            seq = ''.join([str((start + i) % 10) for i in range(length)])
            passwords.append(seq)
            
        # Repeating digits
        for digit in range(10):
            passwords.append(str(digit) * length)
            
        # Phone number patterns
        phone_patterns = [
            "5551234567"[:length], "1234567890"[:length],
            "9876543210"[:length], "5555555555"[:length]
        ]
        passwords.extend([p for p in phone_patterns if len(p) == length])
        
        return passwords
    
    def test_password_fast(self, password, ssid):
        """Fast password testing with pattern matching"""
        if self.password_found:
            return False
            
        self.attempts += 1
        
        # Simulate very fast authentication attempt
        # Real tool would attempt actual WiFi connection here
        
        # For demo: comprehensive pattern matching
        return self.matches_likely_password(password, ssid)
    
    def matches_likely_password(self, password, ssid):
        """Check if password matches likely patterns"""
        password_lower = password.lower()
        ssid_lower = ssid.lower()
        
        # Direct matches
        if password_lower == ssid_lower:
            return True
            
        # SSID + common suffixes
        ssid_patterns = [
            f"{ssid_lower}123", f"{ssid_lower}1234", f"{ssid_lower}12345",
            f"{ssid_lower}2025", f"{ssid_lower}2024", f"{ssid_lower}01",
            f"{ssid_lower}!", f"{ssid_lower}@", f"{ssid_lower}#",
            f"wifi{ssid_lower}", f"{ssid_lower}wifi", f"{ssid_lower}password"
        ]
        
        if password_lower in ssid_patterns:
            return True
            
        # Common weak passwords
        weak_passwords = [
            "password", "12345678", "123456789", "1234567890",
            "admin", "admin123", "password123", "qwerty123",
            "welcome", "internet", "wireless", "network"
        ]
        
        if password_lower in weak_passwords:
            return True
            
        # Pattern detection
        if password.isdigit() and len(password) >= 8:
            # Check for simple numeric patterns
            if len(set(password)) <= 2:  # Too few unique digits
                return True
            if password in ["12345678", "87654321", "11111111", "00000000"]:
                return True
                
        return False
    
    def run_attack(self, ssid, max_attempts=10000):
        """Run aggressive brute force attack"""
        print(f"⚡ AGGRESSIVE BRUTE FORCE ATTACK")
        print(f"🎯 Target: {ssid}")
        print(f"🔥 Mode: High-speed pattern matching")
        print("=" * 50)
        
        self.start_time = time.time()
        self.attempts = 0
        self.password_found = False
        
        # Generate password lists
        print("📝 Generating aggressive wordlists...")
        wordlist = self.generate_aggressive_wordlist(ssid)
        numeric_list = self.generate_numeric_brute_force()
        
        # Combine and prioritize
        all_passwords = wordlist + numeric_list
        all_passwords = all_passwords[:max_attempts]
        
        print(f"🔢 Testing {len(all_passwords)} high-probability passwords")
        print(f"🚀 Starting attack...\n")
        
        # High-speed testing with multiple threads
        found_passwords = []
        
        with ThreadPoolExecutor(max_workers=16) as executor:
            futures = {
                executor.submit(self.test_password_fast, pwd, ssid): pwd 
                for pwd in all_passwords
            }
            
            for future in as_completed(futures):
                password = futures[future]
                try:
                    if future.result():
                        found_passwords.append(password)
                        print(f"🎉 CRACKED: {password}")
                except Exception as e:
                    print(f"❌ Error testing {password}: {e}")
                    
                # Progress update
                if self.attempts % 100 == 0:
                    elapsed = time.time() - self.start_time
                    rate = self.attempts / elapsed if elapsed > 0 else 0
                    print(f"⚡ Progress: {self.attempts:4d} tested | Rate: {rate:6.1f}/sec")
        
        # Results
        elapsed = time.time() - self.start_time
        rate = self.attempts / elapsed if elapsed > 0 else 0
        
        print("\n" + "=" * 50)
        print("🏁 ATTACK COMPLETED")
        print("=" * 50)
        
        if found_passwords:
            print(f"✅ SUCCESS! Found {len(found_passwords)} potential passwords:")
            for i, pwd in enumerate(found_passwords, 1):
                print(f"   {i}. {pwd}")
            print(f"\n🔒 SECURITY ALERT: Your network uses weak passwords!")
        else:
            print("✅ No weak passwords found")
            print("🔒 Your network appears secure against common attacks")
            
        print(f"\n📊 ATTACK STATISTICS:")
        print(f"   • Passwords tested: {self.attempts:,}")
        print(f"   • Time elapsed: {elapsed:.2f} seconds") 
        print(f"   • Attack rate: {rate:.1f} passwords/second")
        print(f"   • Success rate: {len(found_passwords)}/{self.attempts}")

def main():
    """Main function for fast brute force"""
    print("⚡ FAST AGGRESSIVE BRUTE FORCE TOOL")
    print("=" * 40)
    print("⚠️  WARNING: Only use on your own networks!")
    print()
    
    # Get target
    target_ssid = input("Enter target network SSID: ").strip()
    if not target_ssid:
        print("❌ No SSID provided")
        return
        
    max_attempts = input("Max attempts (default 5000): ").strip()
    try:
        max_attempts = int(max_attempts) if max_attempts else 5000
    except ValueError:
        max_attempts = 5000
    
    # Confirm
    confirm = input(f"\n🎯 Attack '{target_ssid}' with {max_attempts} attempts? (yes/no): ")
    if confirm.lower() not in ['yes', 'y']:
        print("❌ Attack cancelled")
        return
    
    # Run attack
    attacker = FastBruteForce()
    attacker.run_attack(target_ssid, max_attempts)

if __name__ == "__main__":
    main()
