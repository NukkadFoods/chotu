#!/usr/bin/env python3
"""
🔍 ISOLATE STEALTH BROWSER WARNING
=================================
Find where exactly the warning is coming from
"""

import sys
import os

# Add paths
base_path = "/Users/mahendrabahubali/chotu"
paths_to_add = [
    base_path,
    f"{base_path}/mcp",
    f"{base_path}/mcp/tools", 
    f"{base_path}/utils",
    f"{base_path}/memory"
]

for path in paths_to_add:
    if path not in sys.path:
        sys.path.insert(0, path)

print("🔍 Testing individual imports to find stealth browser warning...")

# Test 1: Import stealth browser directly
print("\n1️⃣ Importing stealth_browser directly...")
try:
    from stealth_browser import StealthBrowser
    print("✅ stealth_browser imported successfully")
except Exception as e:
    print(f"❌ stealth_browser import failed: {e}")

# Test 2: Import enhanced YouTube automation
print("\n2️⃣ Importing enhanced_youtube_automation...")
try:
    from enhanced_youtube_automation import EnhancedYouTubeAutomation
    print("✅ enhanced_youtube_automation imported successfully")
except Exception as e:
    print(f"❌ enhanced_youtube_automation import failed: {e}")

# Test 3: Import enhanced YouTube automation backup  
print("\n3️⃣ Importing enhanced_youtube_automation_backup...")
try:
    from enhanced_youtube_automation_backup import YouTubeSessionManager
    print("✅ enhanced_youtube_automation_backup imported successfully")
except Exception as e:
    print(f"❌ enhanced_youtube_automation_backup import failed: {e}")

# Test 4: Import session aware YouTube
print("\n4️⃣ Importing session_aware_youtube...")
try:
    from session_aware_youtube import session_aware_youtube_play
    print("✅ session_aware_youtube imported successfully")
except Exception as e:
    print(f"❌ session_aware_youtube import failed: {e}")

print("\n🎯 Import isolation test completed!")
print("If you see '⚠️ Stealth browser not available' above, we found the source!")
