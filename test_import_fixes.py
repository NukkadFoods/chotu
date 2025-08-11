#!/usr/bin/env python3
"""
🧪 TEST FIXED IMPORTS
====================
Test that all the warnings are resolved
"""

import sys
import os

# Add necessary paths
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

print("🧪 Testing Fixed Imports")
print("=" * 40)

# Test 1: Stealth Browser
print("\n🕵️ Test 1: Stealth Browser Import")
try:
    from mcp.tools.enhanced_youtube_automation import STEALTH_AVAILABLE
    if STEALTH_AVAILABLE:
        print("✅ Stealth browser available (no warning)")
    else:
        print("⚠️ Stealth browser not available")
except Exception as e:
    print(f"❌ Import failed: {e}")

# Test 2: Enhanced YouTube Automation
print("\n🎵 Test 2: Enhanced YouTube Automation")
try:
    from mcp.tools.enhanced_youtube_automation import enhanced_youtube_play
    print("✅ Enhanced YouTube automation imported successfully")
except Exception as e:
    print(f"❌ Enhanced YouTube import failed: {e}")

# Test 3: Web Automation Tool  
print("\n🌐 Test 3: Web Automation Tool")
try:
    from mcp.tools.web_automation_tool import ENHANCED_YOUTUBE_AVAILABLE
    if ENHANCED_YOUTUBE_AVAILABLE:
        print("✅ Web automation tool imports working")
    else:
        print("⚠️ Web automation components not available")
except Exception as e:
    print(f"❌ Web automation import failed: {e}")

# Test 4: Session-Aware YouTube
print("\n🎯 Test 4: Session-Aware YouTube")
try:
    from mcp.tools.session_aware_youtube import session_aware_youtube_play
    print("✅ Session-aware YouTube system available")
except Exception as e:
    print(f"❌ Session-aware import failed: {e}")

# Test 5: Context Memory
print("\n🧠 Test 5: Context Memory System")
try:
    from memory.context_memory import get_context_memory
    print("✅ Context memory system available")
except Exception as e:
    print(f"❌ Context memory import failed: {e}")

print("\n🎉 Import testing completed!")
print("If all tests show ✅, the warnings should be fixed.")
