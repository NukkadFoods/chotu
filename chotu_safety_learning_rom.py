#!/usr/bin/env python3
"""
🛡️ CHOTU SAFETY LEARNING ROM ENTRY
=================================
Adding comprehensive safety learning to Chotu's permanent memory
"""

import os
import sys
import json
from datetime import datetime

# Add to Chotu's memory system
sys.path.append('/Users/mahendrabahubali/chotu')
sys.path.append('/Users/mahendrabahubali/chotu/memory')

def create_safety_learning_rom_entry():
    """Create comprehensive ROM entry for ad-skipping safety learning"""
    
    # The learning we want to preserve permanently
    safety_learning_entry = {
        "learning_category": "web_automation_safety",
        "timestamp": datetime.now().isoformat(),
        "problem_type": "accidental_click_prevention",
        "learning_context": {
            "original_problem": "Chotu accidentally clicked Flipkart ad instead of skip button during YouTube ad-skipping",
            "user_complaint": "by mistake chotu clicked one of the ads instead of skip button and flipkart opened",
            "risk_scenario": "Unwanted tab opening, potential security risk, bad user experience"
        },
        "root_cause_analysis": {
            "technical_cause": "Insufficient button validation - clicking any button with 'skip' text",
            "missing_validation": [
                "No class name validation (ytp prefix required)",
                "No href checking (external links not blocked)",
                "No forbidden pattern detection",
                "No tab management for unwanted opens"
            ],
            "safety_gap": "Trusting visual text without validating element context"
        },
        "solution_patterns": {
            "multi_layer_validation": {
                "description": "Apply multiple validation layers for safety-critical actions",
                "implementation": [
                    "Strict element class validation (e.g., 'ytp' for YouTube)",
                    "Text content verification (exact match required)",
                    "URL/href checking (block external links)",
                    "Forbidden pattern detection (shopping/ad keywords)",
                    "Context validation (element must be in proper container)"
                ]
            },
            "forbidden_pattern_detection": {
                "description": "Maintain blacklist of patterns that indicate unwanted actions",
                "patterns": [
                    "learn more", "shop now", "visit site", "download", "install",
                    "get app", "buy now", "order now", "flipkart", "amazon", "myntra"
                ],
                "application": "Check all text content and URLs against forbidden patterns"
            },
            "tab_management": {
                "description": "Automatically handle unwanted tab openings",
                "implementation": [
                    "Monitor for new tabs during automation",
                    "Close tabs with forbidden domains",
                    "Maintain focus on original task tab",
                    "Log unwanted tab attempts for learning"
                ]
            }
        },
        "implementation_techniques": {
            "strict_selectors": {
                "youtube_example": "//button[contains(text(), 'Skip') and contains(@class, 'ytp')]",
                "principle": "Combine text matching with class validation",
                "benefit": "Prevents clicking similarly-named but different elements"
            },
            "validation_chain": {
                "step1": "Check element text contains expected keyword",
                "step2": "Validate element has required CSS class",
                "step3": "Ensure no href attribute (no external links)",
                "step4": "Check against forbidden pattern list",
                "step5": "Verify element is in expected container",
                "fail_action": "Block click and log attempt for analysis"
            },
            "safety_monitoring": {
                "pre_click": "Validate element before clicking",
                "post_click": "Monitor for unwanted behavior (new tabs, redirects)",
                "recovery": "Close unwanted tabs, return to original task",
                "learning": "Update forbidden patterns based on new threats"
            }
        },
        "generic_safety_principles": {
            "never_trust_text_alone": "Visual text can be misleading - always validate element context",
            "use_whitelist_approach": "Define what IS allowed rather than what is forbidden",
            "implement_fail_safes": "Always have recovery mechanisms for safety failures",
            "continuous_monitoring": "Monitor automation effects, not just actions",
            "user_feedback_integration": "Learn from user complaints about unwanted behavior"
        },
        "config_file_patterns": {
            "safe_selectors": {
                "description": "Use config files to maintain safe selectors",
                "example": "youtube.json with validated selectors and forbidden patterns",
                "update_strategy": "Update configs when new threats discovered"
            },
            "forbidden_patterns": {
                "description": "Maintain lists of forbidden keywords and domains",
                "categories": ["shopping", "downloads", "ads", "promotions"],
                "update_frequency": "After each safety incident"
            }
        },
        "future_application_scenarios": [
            {
                "scenario": "Form submission automation",
                "safety_concern": "Accidentally submitting wrong forms or clicking ads",
                "application": "Validate form fields and submit buttons with strict selectors"
            },
            {
                "scenario": "Social media automation", 
                "safety_concern": "Accidentally liking/sharing promotional content",
                "application": "Validate content type before engagement actions"
            },
            {
                "scenario": "Shopping automation",
                "safety_concern": "Accidentally purchasing items or clicking competitor ads",
                "application": "Strict product validation and price checking before actions"
            },
            {
                "scenario": "News/content browsing",
                "safety_concern": "Clicking clickbait or malicious links",
                "application": "URL validation and content type checking"
            }
        ],
        "code_implementation_patterns": {
            "validation_function_template": """
def safe_element_click(driver, element_selector, expected_text, required_class, forbidden_patterns):
    try:
        element = driver.find_element(By.XPATH, element_selector)
        
        # Multi-layer validation
        element_text = element.text.lower().strip()
        element_class = element.get_attribute('class').lower()
        element_href = element.get_attribute('href') or ''
        
        # Validation checks
        if expected_text not in element_text:
            return False, f"Text mismatch: expected '{expected_text}', got '{element_text}'"
        
        if required_class not in element_class:
            return False, f"Class validation failed: '{required_class}' not in '{element_class}'"
        
        if element_href:
            return False, f"External link detected: {element_href}"
        
        all_text = f"{element_text} {element_href}"
        for pattern in forbidden_patterns:
            if pattern in all_text:
                return False, f"Forbidden pattern detected: {pattern}"
        
        # Safe to click
        element.click()
        return True, "Successfully clicked safe element"
        
    except Exception as e:
        return False, f"Error during safe click: {e}"
            """,
            "tab_management_template": """
def monitor_and_close_unwanted_tabs(driver, original_tab, forbidden_domains):
    try:
        current_tabs = driver.window_handles
        for tab in current_tabs:
            if tab != original_tab:
                driver.switch_to.window(tab)
                current_url = driver.current_url.lower()
                
                for domain in forbidden_domains:
                    if domain in current_url:
                        print(f"Closing unwanted tab: {current_url}")
                        driver.close()
                        break
        
        # Return to original tab
        driver.switch_to.window(original_tab)
        return True
        
    except Exception as e:
        print(f"Error managing tabs: {e}")
        return False
            """
        },
        "learning_triggers": [
            "User reports unwanted clicking behavior",
            "New tabs opening unexpectedly during automation", 
            "Automation clicking on promotional content",
            "User mentions specific sites/domains to avoid",
            "Safety validation failures during automation"
        ],
        "success_metrics": [
            "Zero unwanted tab openings",
            "Zero clicks on promotional content",
            "100% validation success rate",
            "User satisfaction with automation safety",
            "Reduced false positive click attempts"
        ],
        "confidence_boost": 95,
        "security_profile": "critical_safety_learning",
        "context_tags": [
            "web_automation", "safety", "validation", "ad_blocking", 
            "click_prevention", "tab_management", "user_protection"
        ],
        "success_count": 1,
        "application_priority": "high"
    }
    
    return safety_learning_entry

def add_to_chotu_rom():
    """Add the safety learning to Chotu's ROM"""
    
    print("🛡️ ADDING SAFETY LEARNING TO CHOTU'S ROM")
    print("=" * 50)
    
    # Create the learning entry
    safety_entry = create_safety_learning_rom_entry()
    
    # Load existing ROM
    try:
        from memory.memory_manager import load_rom, save_rom
        rom = load_rom()
        print(f"📚 Loaded existing ROM with {len(rom)} entries")
    except:
        # Fallback if memory manager not available
        rom_file = '/Users/mahendrabahubali/chotu/memory/rom.json'
        if os.path.exists(rom_file):
            with open(rom_file, 'r') as f:
                rom = json.load(f)
        else:
            rom = []
            os.makedirs(os.path.dirname(rom_file), exist_ok=True)
        print(f"📚 Loaded ROM with {len(rom)} entries")
    
    # Check if similar safety learning already exists
    existing_safety = [entry for entry in rom if entry.get('learning_category') == 'web_automation_safety']
    
    if existing_safety:
        print(f"⚠️  Found {len(existing_safety)} existing safety entries - updating...")
        # Remove old safety entries and add new comprehensive one
        rom = [entry for entry in rom if entry.get('learning_category') != 'web_automation_safety']
    
    # Add the new comprehensive safety learning
    rom.append(safety_entry)
    
    # Save updated ROM
    try:
        from memory.memory_manager import save_rom
        save_rom(rom)
        print("✅ Successfully added safety learning to memory manager")
    except:
        # Fallback save
        rom_file = '/Users/mahendrabahubali/chotu/memory/rom.json'
        with open(rom_file, 'w') as f:
            json.dump(rom, f, indent=2)
        print("✅ Successfully saved safety learning to ROM file")
    
    print(f"📈 ROM now contains {len(rom)} total entries")
    print("🛡️ Chotu will now apply these safety patterns to all future web automation!")
    
    return True

def verify_rom_entry():
    """Verify the ROM entry was added correctly"""
    
    print("\n🔍 VERIFYING ROM ENTRY")
    print("=" * 30)
    
    try:
        from memory.memory_manager import load_rom
        rom = load_rom()
    except:
        rom_file = '/Users/mahendrabahubali/chotu/memory/rom.json'
        with open(rom_file, 'r') as f:
            rom = json.load(f)
    
    # Find safety learning entries
    safety_entries = [entry for entry in rom if entry.get('learning_category') == 'web_automation_safety']
    
    if safety_entries:
        entry = safety_entries[0]
        print("✅ Safety learning found in ROM!")
        print(f"   📅 Timestamp: {entry.get('timestamp', 'unknown')}")
        print(f"   🎯 Problem Type: {entry.get('problem_type', 'unknown')}")
        print(f"   🔧 Solution Patterns: {len(entry.get('solution_patterns', {}))}")
        print(f"   🚨 Forbidden Patterns: {len(entry.get('solution_patterns', {}).get('forbidden_pattern_detection', {}).get('patterns', []))}")
        print(f"   📋 Future Scenarios: {len(entry.get('future_application_scenarios', []))}")
        print(f"   🎚️ Confidence Boost: {entry.get('confidence_boost', 0)}")
        return True
    else:
        print("❌ Safety learning not found in ROM!")
        return False

if __name__ == "__main__":
    print("🛡️ CHOTU SAFETY LEARNING ROM INTEGRATION")
    print("=" * 60)
    print("Adding comprehensive ad-skipping safety learning to Chotu's permanent memory...")
    print()
    
    # Add the learning
    success = add_to_chotu_rom()
    
    if success:
        # Verify it was added
        verify_rom_entry()
        
        print("\n🎉 SAFETY LEARNING INTEGRATION COMPLETE!")
        print("=" * 50)
        print("🧠 Chotu now has permanent knowledge about:")
        print("   ✅ Multi-layer validation for safety-critical actions")
        print("   ✅ Forbidden pattern detection for ads/shopping")
        print("   ✅ Tab management for unwanted openings")
        print("   ✅ Generic safety principles for all web automation")
        print("   ✅ Code patterns for implementing safe automation")
        print()
        print("🚀 Future web automation will automatically apply these safety measures!")
    else:
        print("❌ Failed to integrate safety learning into ROM")
