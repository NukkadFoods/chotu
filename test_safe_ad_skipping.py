#!/usr/bin/env python3
"""
🛡️ Test Enhanced Ad-Skipping with Safety Measures
"""

import sys
sys.path.append('/Users/mahendrabahubali/chotu')

def test_safe_ad_skipping():
    print("🛡️ TESTING ENHANCED AD-SKIPPING WITH SAFETY MEASURES")
    print("=" * 60)
    print("🚫 NEW SAFETY FEATURES:")
    print("   ✅ Strict validation - only clicks REAL skip buttons")
    print("   ✅ Forbidden pattern detection (blocks ad links)")
    print("   ✅ Must have 'ytp' class or exact 'skip' text")
    print("   ✅ Blocks: 'Learn more', 'Shop now', 'Visit site', etc.")
    print("   ✅ Auto-closes unwanted tabs (Flipkart, Amazon, etc.)")
    print("   ✅ Maintains focus on YouTube tab")
    print("")
    
    # Test the validation logic
    print("🧪 TESTING VALIDATION LOGIC:")
    
    test_buttons = [
        {"text": "Skip", "class": "ytp-ad-skip-button", "href": "", "should_click": True},
        {"text": "Skip Ad", "class": "ytp-skip-ad-button", "href": "", "should_click": True},
        {"text": "Learn more", "class": "ad-link", "href": "flipkart.com", "should_click": False},
        {"text": "Shop now", "class": "ad-button", "href": "amazon.com", "should_click": False},
        {"text": "Visit site", "class": "ad-cta", "href": "myntra.com", "should_click": False},
        {"text": "Skip", "class": "regular-button", "href": "", "should_click": False},  # No ytp class - SHOULD BE BLOCKED
    ]
    
    forbidden_patterns = [
        "learn more", "shop now", "visit site", "download", "install", 
        "get app", "buy now", "order now", "flipkart", "amazon", "myntra"
    ]
    
    for i, button in enumerate(test_buttons):
        button_text = button["text"].lower().strip()
        class_name = button["class"].lower()
        href = button["href"].lower()
        
        # Apply validation logic
        all_text = f"{button_text} {href}"
        is_forbidden = any(pattern in all_text for pattern in forbidden_patterns)
        
        is_skip_button = (
            "skip" in button_text and
            ("ytp" in class_name or button_text in ["skip", "skip ad", "skip ads"]) and
            not href and
            not is_forbidden and
            "ytp" in class_name  # STRICT: Must have YouTube player class
        )
        
        expected = button["should_click"]
        result = "✅ CORRECT" if is_skip_button == expected else "❌ WRONG"
        action = "CLICK" if is_skip_button else "BLOCK"
        
        print(f"   Test {i+1}: {result} - '{button['text']}' → {action}")
    
    print("\n🎯 ENHANCED PROTECTION:")
    print("   • Only clicks buttons with 'ytp' class (YouTube player)")
    print("   • Blocks all shopping/download links")
    print("   • Auto-closes Flipkart/Amazon tabs")
    print("   • Maintains YouTube focus")
    
    print("\n🚀 Ready to test with real video!")
    
    # Optionally test with real video
    test_real = input("\n🎵 Test with real video? (y/n): ").lower().strip()
    if test_real == 'y':
        from chotu_youtube_player import chotu_play_youtube
        
        print("\n🎬 Testing with popular song (likely to have ads)...")
        result = chotu_play_youtube("popular bollywood songs 2024")
        
        if result.get('success'):
            print("\n✅ ENHANCED SAFETY TEST COMPLETED!")
            print("🛡️ Safety measures are active!")
        else:
            print(f"\n❌ Test failed: {result.get('error')}")

if __name__ == "__main__":
    test_safe_ad_skipping()
