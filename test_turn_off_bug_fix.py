#!/usr/bin/env python3
"""
🧪 SPECIFIC BUG FIX TEST
=======================
Test the exact scenario: "turn it off" should resolve to bluetooth, not increase brightness
"""

import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.intelligent_context_resolver import resolve_ambiguous_command
from memory.context_validator import validate_context_resolution
from memory.context_manager import ContextManager

def test_turn_off_bug():
    """Test the specific bug: 'turn it off' should suggest bluetooth off, not increase brightness"""
    
    print("🐛 TESTING SPECIFIC BUG FIX")
    print("=" * 35)
    
    # Setup context exactly as in the failing test
    context = ContextManager()
    
    # Add bluetooth interaction (to make it recent and toggle-able)
    context.add_interaction("turn on bluetooth", "✅ Bluetooth enabled", True)
    context.add_interaction("open safari", "✅ Safari opened", True)
    context.add_interaction("set volume to 50%", "✅ Volume set to 50%", True)
    
    print("📝 Context setup:")
    print("   1. turn on bluetooth → ✅ Bluetooth enabled")
    print("   2. open safari → ✅ Safari opened")
    print("   3. set volume to 50% → ✅ Volume set to 50%")
    
    print(f"\n💬 User command: 'turn it off'")
    print("📝 Expected: Should suggest 'turn bluetooth off' (since bluetooth was recently enabled)")
    print()
    
    # STEP 1: Context resolution
    print("🧠 STEP 1: Context Resolution")
    context_result = resolve_ambiguous_command("turn it off")
    print(f"   Resolved to: '{context_result['resolved_command']}'")
    print(f"   Alternatives: {context_result['alternatives']}")
    
    # STEP 2: Validation
    print("\n🔍 STEP 2: Logical Validation")
    validation_result = validate_context_resolution(
        "turn it off",
        context_result['resolved_command'],
        context_result,
        context_result['alternatives']
    )
    
    print(f"   Valid: {validation_result['valid']}")
    print(f"   Final command: '{validation_result['final_command']}'")
    print(f"   Reasoning: {validation_result['reasoning']}")
    
    # STEP 3: Check if bug is fixed
    print(f"\n🎯 BUG CHECK:")
    
    final_cmd = validation_result['final_command'].lower()
    
    if 'turn' in final_cmd and 'off' in final_cmd:
        if 'bluetooth' in final_cmd:
            print("✅ BUG FIXED! Correctly suggests turning off bluetooth")
        elif 'wifi' in final_cmd:
            print("✅ BUG FIXED! Correctly suggests turning off wifi (also valid)")
        else:
            print(f"⚠️  Partial fix: Suggests turning off something, but not ideal: '{final_cmd}'")
    elif 'increase brightness' in final_cmd:
        print("❌ BUG STILL EXISTS! Still suggests 'increase brightness' for 'turn off' command")
        print("   This is completely wrong - user wants to turn something OFF, not increase anything")
    else:
        print(f"❓ Unexpected result: '{final_cmd}'")
    
    return validation_result

def test_multiple_turn_off_scenarios():
    """Test various 'turn off' scenarios"""
    
    print(f"\n\n🔬 TESTING MULTIPLE 'TURN OFF' SCENARIOS")
    print("=" * 45)
    
    scenarios = [
        {
            "context": [("turn on bluetooth", "✅ Bluetooth enabled")],
            "command": "turn it off",
            "expected": "turn bluetooth off"
        },
        {
            "context": [("enable wifi", "✅ WiFi enabled")],
            "command": "turn it off", 
            "expected": "turn wifi off"
        },
        {
            "context": [("turn on bluetooth", "✅ Bluetooth enabled"), ("open chrome", "✅ Chrome opened")],
            "command": "turn it off",
            "expected": "turn bluetooth off (bluetooth is toggle-able, chrome should be 'closed')"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n🧪 Scenario {i}:")
        
        # Setup context
        context = ContextManager()
        for user_input, response in scenario["context"]:
            context.add_interaction(user_input, response, True)
            print(f"   Context: {user_input} → {response}")
        
        print(f"   Command: '{scenario['command']}'")
        print(f"   Expected: {scenario['expected']}")
        
        # Test resolution
        context_result = resolve_ambiguous_command(scenario["command"])
        validation_result = validate_context_resolution(
            scenario["command"],
            context_result['resolved_command'], 
            context_result,
            context_result['alternatives']
        )
        
        final_cmd = validation_result['final_command']
        print(f"   Result: '{final_cmd}'")
        
        # Check if result makes sense
        if 'turn' in final_cmd.lower() and 'off' in final_cmd.lower():
            print("   ✅ Action preserved correctly (turn off)")
        elif 'increase' in final_cmd.lower() or 'decrease' in final_cmd.lower():
            print("   ❌ BUG: Suggests increase/decrease for 'turn off' command!")
        elif 'NEEDS_CLARIFICATION' in final_cmd:
            print("   🤔 Asks for clarification (acceptable)")
        else:
            print(f"   ❓ Unexpected: {final_cmd}")

if __name__ == "__main__":
    # Run the bug fix test
    result = test_turn_off_bug()
    test_multiple_turn_off_scenarios()
    
    print(f"\n\n🏆 SUMMARY")
    print("=" * 15)
    print("The system should NEVER suggest 'increase brightness' for 'turn it off'")
    print("User intent: TURN OFF something")
    print("Valid suggestions: turn bluetooth off, turn wifi off, close chrome")
    print("Invalid suggestions: increase brightness, decrease volume, etc.")
    print()
    print("🎯 Fix status: Testing complete")
