#!/usr/bin/env python3
"""
🎵 CHOTU ENHANCED YOUTUBE PLAYER DEMO
===================================
Now with robust ad-skipping that catches "Skip" buttons!
"""

import sys
sys.path.append('/Users/mahendrabahubali/chotu')

from chotu_youtube_player import chotu_play_youtube

def demo_enhanced_player():
    print("🎵 CHOTU ENHANCED YOUTUBE PLAYER")
    print("=" * 50)
    print("🚫 NEW AD-SKIPPING FEATURES:")
    print("   ✅ Detects 'Skip' button by text content")
    print("   ✅ Uses XPath selectors for robust finding")
    print("   ✅ Multiple click methods (JS, ActionChains)")
    print("   ✅ Scans ALL buttons for 'Skip' text")
    print("   ✅ Handles case variations (Skip, SKIP, skip)")
    print("   ✅ Continuous monitoring during playback")
    print("")
    
    song = input("🎶 Enter a song to play (or press Enter for 'kitne bechain hoke'): ").strip()
    if not song:
        song = "kitne bechain hoke"
    
    print(f"\n🚀 Playing: {song}")
    print("🚫 Ad-skipping is ACTIVE - will auto-click any 'Skip' button!")
    print("")
    
    result = chotu_play_youtube(song)
    
    print("\n📊 RESULT:")
    if result.get('success'):
        print("✅ SUCCESS! Video is playing with ad-skipping protection!")
        print(f"🎬 Video: {result.get('video_title', 'Unknown')}")
        print(f"🔧 Method: {result.get('method', 'Unknown')}")
        print("\n🛡️ PROTECTION ACTIVE:")
        print("   • Monitoring for ads continuously")
        print("   • Will auto-click 'Skip' buttons")
        print("   • Enhanced detection algorithms")
    else:
        print(f"❌ FAILED: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    demo_enhanced_player()
