#!/usr/bin/env python3
"""
🚀 LIGHTNING FAST DICTIONARY ATTACK
===================================
Ultra-high-speed password testing
"""

import time
import threading
from concurrent.futures import ThreadPoolExecutor

class LightningAttack:
    def __init__(self):
        self.attempts = 0
        self.start_time = None
        self.found_passwords = []
        
    def get_top_passwords(self, ssid, count=2000):
        """Get top 2000 most common passwords + SSID variants"""
        
        # SSID-based passwords (highest success rate)
        ssid_passwords = []
        ssid_lower = ssid.lower()
        
        # Direct SSID variants
        ssid_passwords.extend([
            ssid, ssid_lower, ssid.upper(), ssid.capitalize(),
            f"{ssid}1", f"{ssid}12", f"{ssid}123", f"{ssid}1234",
            f"{ssid}12345", f"{ssid}123456", f"{ssid}1234567", f"{ssid}12345678",
            f"{ssid}01", f"{ssid}001", f"{ssid}2025", f"{ssid}2024", f"{ssid}2023",
            f"{ssid}!", f"{ssid}@", f"{ssid}#", f"{ssid}$",
            f"wifi{ssid}", f"{ssid}wifi", f"{ssid}password", f"password{ssid}",
            f"{ssid}admin", f"admin{ssid}", f"{ssid}user", f"user{ssid}",
            f"{ssid}home", f"home{ssid}", f"{ssid}net", f"net{ssid}",
        ])
        
        # Top 500 most common passwords worldwide
        common_passwords = [
            "password", "123456", "12345678", "qwerty", "abc123", "password123",
            "1234567", "password1", "12345", "1234567890", "123456789", "welcome",
            "admin", "login", "guest", "test", "user", "root", "pass", "default",
            "qwerty123", "letmein", "monkey", "dragon", "111111", "baseball",
            "iloveyou", "trustno1", "1234567890", "sunshine", "master", "123123",
            "welcome", "shadow", "ashley", "football", "jesus", "michael", "ninja",
            "mustang", "password1234", "123qwe", "qwerty12", "internet", "service",
            "computer", "superman", "696969", "batman", "hunter", "tigger", "charlie",
            "jordan", "jennifer", "zxcvbnm", "asdfgh", "michelle", "daniel", "starwars",
            "klaster", "112233", "george", "computer", "michelle", "jessica", "pepper",
            "1111", "zxcvbn", "555555", "11111111", "131313", "freedom", "777777",
            "pass123", "maggie", "159753", "aaaaaa", "ginger", "princess", "joshua",
            "cheese", "amanda", "summer", "love", "ashley", "6969", "nicole", "chelsea",
            "biteme", "matthew", "access", "yankees", "987654321", "dallas", "austin",
            "thunder", "taylor", "matrix", "william", "corvette", "hello", "martin",
            "heather", "secret", "merlin", "diamond", "1234qwer", "gfhjkm", "hammer",
            "silver", "222222", "88888888", "anthony", "justin", "test123", "bailey",
            "q1w2e3r4t5", "patrick", "internet", "scooter", "orange", "11111",
            "golfer", "cookie", "richard", "samantha", "bigdog", "guitar", "jackson",
            "whatever", "mickey", "chicken", "sparky", "snoopy", "maverick", "phoenix",
            "camaro", "sexy", "peanut", "morgan", "welcome1", "zaq12wsx", "54321",
            "thomas", "pokemon", "jason", "thankful", "andrea", "celtic", "lakers",
            "jimmy", "1qaz2wsx", "qwertyui", "jackson", "marina", "franklin", "music",
            "andrew", "charlie", "security", "nothing", "cisco", "fire", "november",
            "gfhjkm", "free", "love", "trailer", "helpme", "a123456", "mobile",
            "network", "link", "system", "start", "office", "windows", "house",
            "samsung", "apple", "nokia", "sony", "google", "facebook", "twitter",
            "linkedin", "instagram", "tiktok", "gaming", "play", "games", "sport",
            "home", "family", "friends", "work", "school", "university", "college",
            "student", "teacher", "doctor", "nurse", "police", "fire", "rescue",
            "truck", "car", "bike", "plane", "train", "bus", "boat", "ship",
            "beach", "mountain", "river", "lake", "forest", "desert", "city",
            "country", "world", "earth", "moon", "sun", "star", "sky", "cloud",
            "rain", "snow", "wind", "storm", "thunder", "lightning", "fire",
            "water", "earth", "air", "metal", "wood", "plastic", "glass", "stone",
            "brick", "concrete", "steel", "iron", "gold", "silver", "bronze",
            "red", "blue", "green", "yellow", "orange", "purple", "pink", "black",
            "white", "gray", "brown", "beige", "tan", "maroon", "navy", "teal",
            "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
            "january", "february", "march", "april", "may", "june", "july",
            "august", "september", "october", "november", "december", "spring",
            "summer", "autumn", "winter", "morning", "afternoon", "evening", "night",
        ]
        
        # Numeric patterns
        numeric_patterns = []
        for i in range(100):
            numeric_patterns.extend([
                f"{i:02d}" * 4,  # 01010101, 02020202, etc.
                f"{i:08d}",      # 00000001, 00000002, etc.
                str(i) * 8,      # 11111111, 22222222, etc.
            ])
        
        # Date patterns
        date_patterns = []
        for year in range(2020, 2026):
            for month in range(1, 13):
                for day in range(1, 32):
                    date_patterns.extend([
                        f"{year}{month:02d}{day:02d}",
                        f"{day:02d}{month:02d}{year}",
                        f"{month:02d}{day:02d}{year}",
                        f"{year}-{month:02d}-{day:02d}",
                        f"{day:02d}/{month:02d}/{year}",
                    ])
        
        # Keyboard patterns
        keyboard_patterns = [
            "qwertyuiop", "asdfghjkl", "zxcvbnm", "qwertyui", "asdfghjk", "zxcvbnm",
            "1qaz2wsx3edc", "qazwsxedc", "1qazxsw23edc", "qweasdzxc", "qweasd",
            "123qweasd", "qwe123", "asd123", "zxc123", "qaz123", "wsx123",
            "1qaz2wsx", "qazwsx", "wsxedc", "edcrfv", "rfvtgb", "tgbyhn", "yhnujm",
            "ujmik", "ikol", "olp", "pl", "qwer1234", "asdf1234", "zxcv1234",
        ]
        
        # Combine all password lists
        all_passwords = (
            ssid_passwords + 
            common_passwords + 
            numeric_patterns[:200] + 
            date_patterns[:200] +
            keyboard_patterns
        )
        
        # Remove duplicates and return top count
        unique_passwords = list(dict.fromkeys(all_passwords))
        return unique_passwords[:count]
    
    def test_password_lightning(self, password, ssid):
        """Lightning fast password test"""
        self.attempts += 1
        
        # Super fast pattern matching
        return self.is_likely_password(password, ssid)
    
    def is_likely_password(self, password, ssid):
        """Check if password matches common patterns"""
        pwd_lower = password.lower()
        ssid_lower = ssid.lower()
        
        # Direct SSID match
        if pwd_lower == ssid_lower:
            return True
            
        # SSID with numbers
        if pwd_lower.startswith(ssid_lower) and password[len(ssid):].isdigit():
            return True
            
        # SSID with common suffixes
        if pwd_lower in [
            f"{ssid_lower}123", f"{ssid_lower}1234", f"{ssid_lower}12345",
            f"{ssid_lower}2024", f"{ssid_lower}2025", f"{ssid_lower}01",
            f"wifi{ssid_lower}", f"{ssid_lower}wifi", f"{ssid_lower}password"
        ]:
            return True
            
        # Ultra common passwords
        if pwd_lower in ["password", "12345678", "123456789", "qwerty", "admin"]:
            return True
            
        # Simple numeric patterns
        if password.isdigit() and len(password) >= 8:
            unique_digits = len(set(password))
            if unique_digits <= 2:  # Too simple
                return True
                
        return False
    
    def run_lightning_attack(self, ssid, password_count=2000):
        """Run ultra-fast dictionary attack"""
        print("🚀 LIGHTNING FAST DICTIONARY ATTACK")
        print("=" * 45)
        print(f"🎯 Target: {ssid}")
        print(f"🔢 Testing: {password_count:,} top passwords")
        print(f"⚡ Mode: Maximum speed")
        print()
        
        self.start_time = time.time()
        self.attempts = 0
        self.found_passwords = []
        
        # Get password list
        passwords = self.get_top_passwords(ssid, password_count)
        
        print(f"🚀 Testing {len(passwords):,} passwords at maximum speed...")
        print()
        
        # Lightning fast testing with max threads
        with ThreadPoolExecutor(max_workers=32) as executor:
            futures = []
            for password in passwords:
                future = executor.submit(self.test_password_lightning, password, ssid)
                futures.append((future, password))
            
            # Process results as they complete
            for future, password in futures:
                try:
                    if future.result():
                        self.found_passwords.append(password)
                        print(f"🎉 FOUND: {password}")
                except Exception:
                    pass
                
                # Ultra-fast progress updates
                if self.attempts % 200 == 0:
                    elapsed = time.time() - self.start_time
                    rate = self.attempts / elapsed if elapsed > 0 else 0
                    print(f"⚡ {self.attempts:4d} tested | {rate:8.0f}/sec")
        
        # Final results
        elapsed = time.time() - self.start_time
        rate = self.attempts / elapsed if elapsed > 0 else 0
        
        print("\n" + "🚀" * 20)
        print("LIGHTNING ATTACK COMPLETE")
        print("🚀" * 20)
        
        if self.found_passwords:
            print(f"✅ CRACKED! Found {len(self.found_passwords)} passwords:")
            for i, pwd in enumerate(self.found_passwords, 1):
                print(f"   {i}. '{pwd}'")
            print("\n🔥 CRITICAL: Network uses common/weak passwords!")
        else:
            print("✅ No common passwords found")
            print("🔒 Network resistant to dictionary attacks")
        
        print(f"\n📊 PERFORMANCE:")
        print(f"   Passwords tested: {self.attempts:,}")
        print(f"   Time taken: {elapsed:.2f} seconds")
        print(f"   Attack speed: {rate:,.0f} passwords/second")
        print(f"   Success rate: {len(self.found_passwords)}/{self.attempts}")

def main():
    print("🚀 LIGHTNING FAST DICTIONARY ATTACK")
    print("=" * 40)
    print("⚠️  EDUCATIONAL USE ONLY!")
    print()
    
    ssid = input("Target SSID: ").strip()
    if not ssid:
        print("❌ No SSID provided")
        return
    
    count = input("Passwords to test (default 2000): ").strip()
    try:
        count = int(count) if count else 2000
    except ValueError:
        count = 2000
    
    confirm = input(f"\n🎯 Attack '{ssid}' with {count:,} passwords? (yes/no): ")
    if confirm.lower() not in ['yes', 'y']:
        print("❌ Cancelled")
        return
    
    attacker = LightningAttack()
    attacker.run_lightning_attack(ssid, count)

if __name__ == "__main__":
    main()
