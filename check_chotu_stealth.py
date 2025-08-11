#!/usr/bin/env python3
"""
Check Chotu's Browser Status - Stealth vs Regular
"""

import sys
import os
import psutil
import re

# Add project root to path
sys.path.append('/Users/mahendrabahubali/chotu')

def check_browser_processes():
    """Check what browser processes are running and their type"""
    print("🔍 Checking Browser Processes")
    print("=" * 50)
    
    chrome_processes = []
    chromedriver_processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if 'chrome' in proc.info['name'].lower():
                chrome_processes.append(proc.info)
            elif 'chromedriver' in proc.info['name'].lower():
                chromedriver_processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    print(f"🌐 Found {len(chrome_processes)} Chrome processes")
    print(f"🤖 Found {len(chromedriver_processes)} ChromeDriver processes")
    
    # Analyze Chrome processes for stealth indicators
    stealth_indicators = 0
    regular_automation = 0
    
    for proc in chrome_processes:
        try:
            cmdline_list = proc.get('cmdline', [])
            if cmdline_list:
                cmdline = ' '.join(cmdline_list)
            else:
                cmdline = ''
        except:
            cmdline = ''
        
        # Check for stealth indicators
        if any(indicator in cmdline for indicator in [
            '--disable-blink-features=AutomationControlled',
            '--exclude-switches=enable-automation',
            '--disable-dev-shm-usage',
            '--no-sandbox',
            'undetected'
        ]):
            stealth_indicators += 1
            print(f"🕵️ Stealth browser detected (PID: {proc['pid']})")
            
        # Check for regular automation
        elif any(indicator in cmdline for indicator in [
            '--enable-automation',
            '--test-type=webdriver',
            '--remote-debugging-port'
        ]):
            regular_automation += 1
            print(f"🤖 Regular automation browser (PID: {proc['pid']})")
    
    return stealth_indicators, regular_automation

def check_chotu_session_status():
    """Check Chotu's YouTube session status"""
    print("\n🎵 Checking Chotu YouTube Session Status")
    print("=" * 50)
    
    try:
        from mcp.tools.enhanced_youtube_automation import enhanced_youtube_status
        
        status = enhanced_youtube_status()
        print(f"📊 Session Status: {status}")
        
        if status.get('session_active'):
            print("✅ YouTube session is active")
            print(f"🌐 Current URL: {status.get('current_url', 'Unknown')}")
            print(f"🎬 Current video: {status.get('current_video', 'None')}")
            
            # Check if it's using stealth browser
            browser_type = status.get('browser_type', 'unknown')
            if 'stealth' in browser_type.lower() or 'undetected' in browser_type.lower():
                print("🕵️ Using STEALTH browser ✅")
            else:
                print("🤖 Using regular automation browser")
        else:
            print("❌ No active YouTube session")
            
    except Exception as e:
        print(f"❌ Cannot check session status: {e}")

def analyze_browser_flags():
    """Analyze browser command line flags for stealth detection"""
    print("\n🔍 Analyzing Browser Command Line Flags")
    print("=" * 50)
    
    stealth_flags = [
        '--disable-blink-features=AutomationControlled',
        '--exclude-switches=enable-automation',
        '--disable-dev-shm-usage',
        '--no-sandbox',
        '--disable-web-security',
        '--disable-features=VizDisplayCompositor'
    ]
    
    automation_flags = [
        '--enable-automation',
        '--test-type=webdriver',
        '--remote-debugging-port'
    ]
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if 'chrome' in proc.info['name'].lower():
                cmdline = ' '.join(proc.info.get('cmdline', []))
                
                stealth_count = sum(1 for flag in stealth_flags if flag in cmdline)
                automation_count = sum(1 for flag in automation_flags if flag in cmdline)
                
                if stealth_count > 0 or automation_count > 0:
                    print(f"\n🌐 Chrome Process PID: {proc.info['pid']}")
                    print(f"🕵️ Stealth flags: {stealth_count}/{len(stealth_flags)}")
                    print(f"🤖 Automation flags: {automation_count}/{len(automation_flags)}")
                    
                    if stealth_count > automation_count:
                        print("✅ This appears to be a STEALTH browser")
                    elif automation_count > 0:
                        print("⚠️ This appears to be regular automation")
                    else:
                        print("❓ Regular Chrome browser")
                        
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

def check_user_data_directories():
    """Check for Chrome user data directories that indicate stealth usage"""
    print("\n📁 Checking Chrome User Data Directories")
    print("=" * 50)
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if 'chrome' in proc.info['name'].lower():
                cmdline = ' '.join(proc.info.get('cmdline', []))
                
                # Look for user-data-dir
                if '--user-data-dir=' in cmdline:
                    data_dir = re.search(r'--user-data-dir=([^\s]+)', cmdline)
                    if data_dir:
                        path = data_dir.group(1)
                        print(f"🌐 PID {proc.info['pid']}: {path}")
                        
                        if 'ChoutuYoutube' in path:
                            print("   ✅ This is Chotu's YouTube browser!")
                        elif 'tmp' in path or 'temp' in path:
                            print("   🕵️ Temporary directory (likely stealth)")
                        else:
                            print("   📁 Custom user directory")
                            
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

if __name__ == "__main__":
    print("🕵️ Chotu Browser Stealth Detection")
    print("🎯 Checking if Chotu is using stealth browser technology")
    print("=" * 60)
    
    # Check processes
    stealth_count, automation_count = check_browser_processes()
    
    # Check session status
    check_chotu_session_status()
    
    # Analyze flags
    analyze_browser_flags()
    
    # Check directories
    check_user_data_directories()
    
    # Summary
    print("\n🎯 STEALTH DETECTION SUMMARY")
    print("=" * 40)
    if stealth_count > 0:
        print("✅ STEALTH BROWSER DETECTED!")
        print("🕵️ Chotu is using advanced anti-detection technology")
    elif automation_count > 0:
        print("⚠️ Regular automation browser detected")
        print("🤖 Chotu is using standard Selenium automation")
    else:
        print("❓ No automation browsers detected")
        print("💭 Chotu might not have an active session")
        
    print(f"\n📊 Final Score:")
    print(f"   🕵️ Stealth browsers: {stealth_count}")
    print(f"   🤖 Regular automation: {automation_count}")
