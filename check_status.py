#!/usr/bin/env python3
"""
Quick Status Check for Running YouTube Automation
"""

import psutil
import time

def check_youtube_processes():
    """Check current YouTube automation status"""
    print("🔍 Current YouTube Automation Status")
    print("=" * 40)
    
    # Check for Chrome processes
    stealth_count = 0
    automation_count = 0
    youtube_tabs = 0
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if 'chrome' in proc.info['name'].lower():
                cmdline_list = proc.info.get('cmdline', [])
                if cmdline_list:
                    cmdline = ' '.join(cmdline_list)
                    
                    # Check for YouTube
                    if 'youtube' in cmdline.lower():
                        youtube_tabs += 1
                    
                    # Check for stealth indicators
                    stealth_indicators = [
                        '--disable-blink-features=AutomationControlled',
                        '--exclude-switches=enable-automation',
                        '--no-sandbox',
                        'undetected'
                    ]
                    
                    automation_indicators = [
                        '--enable-automation',
                        '--test-type=webdriver'
                    ]
                    
                    if any(indicator in cmdline for indicator in stealth_indicators):
                        stealth_count += 1
                    elif any(indicator in cmdline for indicator in automation_indicators):
                        automation_count += 1
                        
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    print(f"🕵️ Stealth browsers: {stealth_count}")
    print(f"🤖 Regular automation: {automation_count}")
    print(f"📺 YouTube tabs: {youtube_tabs}")
    
    if stealth_count > 0:
        print("✅ STEALTH MODE ACTIVE")
    elif automation_count > 0:
        print("⚠️ Using regular automation")
    else:
        print("❓ No automation detected")
    
    if youtube_tabs > 0:
        print("🎵 YouTube sessions active")
    
    return stealth_count, automation_count, youtube_tabs

if __name__ == "__main__":
    print("🎯 YouTube Automation Status Check")
    print(f"⏰ Time: {time.strftime('%H:%M:%S')}")
    print()
    
    stealth, automation, youtube = check_youtube_processes()
    
    print(f"\n📊 Summary:")
    if stealth > 0 and youtube > 0:
        print("🎉 STEALTH YOUTUBE ACTIVE - Perfect!")
    elif stealth > 0:
        print("✅ Stealth ready, waiting for YouTube")
    elif automation > 0:
        print("⚠️ Regular automation detected")
    else:
        print("💤 No automation running")
        
    print(f"\n💡 Run this script again to monitor status")
