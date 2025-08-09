#!/usr/bin/env python3
"""
🚫 Test Ad-Skipping Functionality
"""

def test_ad_skip_logic():
    print("🧪 TESTING AD-SKIP DETECTION LOGIC")
    print("=" * 40)
    
    # Simulate button text variations
    test_buttons = [
        {"text": "Skip", "aria_label": "", "class": ""},
        {"text": "Skip Ad", "aria_label": "", "class": ""},
        {"text": "SKIP", "aria_label": "", "class": ""},
        {"text": "", "aria_label": "Skip advertisement", "class": ""},
        {"text": "", "aria_label": "", "class": "ytp-ad-skip-button"},
        {"text": "Skip in 5", "aria_label": "", "class": ""},
    ]
    
    for i, button in enumerate(test_buttons):
        button_text = button["text"].lower()
        aria_label = button["aria_label"].lower()
        class_name = button["class"].lower()
        
        # Test detection logic
        is_skip_button = ("skip" in button_text or 
                         "skip" in aria_label or 
                         "skip" in class_name or
                         "ytp-ad" in class_name)
        
        result = "✅ DETECTED" if is_skip_button else "❌ MISSED"
        print(f"Test {i+1}: {result} - Text:'{button['text']}' Aria:'{button['aria_label']}' Class:'{button['class']}'")
    
    print("\n🎯 SELECTORS BEING USED:")
    selectors = [
        "//button[contains(text(), 'Skip')]",
        "//button[contains(text(), 'skip')]", 
        "//button[contains(text(), 'SKIP')]",
        ".ytp-ad-skip-button",
        "//button[contains(@aria-label, 'Skip')]"
    ]
    
    for selector in selectors:
        print(f"   • {selector}")
    
    print("\n💡 The enhanced version should now catch the 'Skip' button!")

if __name__ == "__main__":
    test_ad_skip_logic()
