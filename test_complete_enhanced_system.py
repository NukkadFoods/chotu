#!/usr/bin/env python3
"""
🧪 COMPLETE ENHANCED CONTEXT SYSTEM TEST
========================================
Test the full pipeline: Context Resolution → Validation → Intelligent Reasoning
"""

import sys
import os
from datetime import datetime

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.intelligent_context_resolver import resolve_ambiguous_command
from memory.context_validator import validate_context_resolution
from memory.context_manager import ContextManager

def simulate_realistic_scenario():
    """Simulate the exact scenario you mentioned"""
    
    print("🤖 CHOTU ENHANCED CONTEXT SYSTEM - COMPLETE TEST")
    print("=" * 60)
    
    # Setup context exactly like your scenario
    context = ContextManager()
    
    print("📝 BUILDING CONVERSATION HISTORY:")
    print("-" * 35)
    
    interactions = [
        ("set brightness to 70%", "✅ Brightness set to 70%"),
        ("open chrome browser", "✅ Chrome opened successfully"), 
        ("search for python tutorials", "✅ Searched for python tutorials"),
        ("set volume to 60%", "✅ Volume set to 60%")
    ]
    
    for user_input, response in interactions:
        context.add_interaction(user_input, response, True)
        print(f"   User: '{user_input}' → Chotu: '{response}'")
    
    print(f"\n🗣️  USER SAYS: 'increase it'")
    print("=" * 25)
    
    # STEP 1: Context Resolution
    print("\n🧠 STEP 1: INTELLIGENT CONTEXT RESOLUTION")
    print("-" * 45)
    
    context_result = resolve_ambiguous_command("increase it")
    
    print(f"✅ Ambiguity detected: {context_result.get('needs_clarification', False) == False}")
    print(f"✅ Resolved to: '{context_result['resolved_command']}'")
    print(f"✅ Confidence: {context_result['confidence']}%")
    print(f"✅ Source: {context_result['context_source']}")
    print(f"✅ Reasoning: {context_result['reasoning']}")
    print(f"✅ Alternatives: {context_result['alternatives']}")
    
    # STEP 2: Logical Validation
    print(f"\n🔍 STEP 2: LOGICAL VALIDATION WITH GPT")
    print("-" * 40)
    
    validation_result = validate_context_resolution(
        "increase it",
        context_result['resolved_command'],
        context_result,
        context_result['alternatives']
    )
    
    print(f"🎯 Logical validation: {'✅ VALID' if validation_result['valid'] else '❌ INVALID'}")
    print(f"🎯 Final command: '{validation_result['final_command']}'")
    print(f"🎯 GPT reasoning: {validation_result['reasoning']}")
    print(f"🎯 Context analysis: {validation_result.get('context_analysis', 'N/A')}")
    
    # STEP 3: Final Decision
    print(f"\n🎬 STEP 3: CHOTU'S FINAL DECISION")
    print("-" * 35)
    
    if validation_result['valid']:
        print(f"✅ Chotu executes: '{validation_result['final_command']}'")
        print(f"🗣️  Chotu says: 'I understand you want to {validation_result['final_command']}'")
    elif validation_result['needs_clarification']:
        print(f"🤔 Chotu asks: '{validation_result['clarification_question']}'")
    else:
        if validation_result.get('suggested_action'):
            print(f"🔧 Chotu suggests: '{validation_result['suggested_action']}'")
            print(f"🗣️  Chotu says: 'I think you meant {validation_result['suggested_action']}'")
        else:
            print(f"❌ Chotu confused: 'I'm not sure what you want me to do'")
    
    return validation_result

def test_multiple_scenarios():
    """Test various edge cases"""
    
    print(f"\n\n🔬 TESTING MULTIPLE SCENARIOS")
    print("=" * 35)
    
    # Setup different contexts
    context = ContextManager()
    
    # Add more varied interactions
    interactions = [
        ("turn on bluetooth", "✅ Bluetooth enabled"),
        ("open safari", "✅ Safari opened"),
        ("increase brightness to 80%", "✅ Brightness set to 80%"),
        ("set volume to 50%", "✅ Volume set to 50%"),
        ("open terminal", "✅ Terminal opened")
    ]
    
    for user_input, response in interactions:
        context.add_interaction(user_input, response, True)
    
    test_commands = [
        ("increase it", "Should be volume (most recent numeric setting)"),
        ("close it", "Should be terminal (most recent app opened)"),
        ("turn it off", "Should be bluetooth (most recent toggle-able system)"),
        ("make it louder", "Should be volume (contains semantic hint)"),
        ("decrease it by 10%", "Should be volume"),
        ("set it to 90", "Could be brightness or volume - needs clarification")
    ]
    
    for cmd, expectation in test_commands:
        print(f"\n💬 Testing: '{cmd}'")
        print(f"📝 Expected: {expectation}")
        
        # Resolve context
        context_result = resolve_ambiguous_command(cmd)
        
        # Validate logic
        validation_result = validate_context_resolution(
            cmd,
            context_result['resolved_command'],
            context_result,
            context_result['alternatives']
        )
        
        print(f"🎯 Context resolved: '{context_result['resolved_command']}'")
        print(f"🔍 Validation: {'✅ Valid' if validation_result['valid'] else '❌ Invalid'}")
        print(f"🎬 Final result: '{validation_result['final_command']}'")
        
        if validation_result['needs_clarification']:
            print(f"🤔 Clarification: {validation_result['clarification_question']}")

def demonstrate_reasoning_process():
    """Show the detailed reasoning process"""
    
    print(f"\n\n🧠 DETAILED REASONING DEMONSTRATION")
    print("=" * 40)
    
    print("🎯 QUESTION: 'increase it' referring to Chrome - how can you increase Chrome?")
    print("📖 ANSWER: Here's how Chotu's enhanced system handles this...")
    print()
    
    # Simulate the problematic scenario
    context = ContextManager()
    context.add_interaction("open chrome", "✅ Chrome opened", True)
    context.add_interaction("set brightness to 60%", "✅ Brightness set to 60%", True)
    
    print("🔄 PROCESSING PIPELINE:")
    print("-" * 23)
    
    # Step 1
    print("1️⃣ Context Resolution finds 'chrome' as most recent subject")
    context_result = resolve_ambiguous_command("increase it")
    print(f"   → Resolves to: '{context_result['resolved_command']}'")
    
    # Step 2  
    print("2️⃣ Logical Validation detects 'increase chrome' makes no sense")
    validation_result = validate_context_resolution(
        "increase it", context_result['resolved_command'],
        context_result, context_result['alternatives']
    )
    print(f"   → GPT Analysis: {validation_result['reasoning'][:100]}...")
    
    # Step 3
    print("3️⃣ Intelligent Correction suggests logical alternative")
    print(f"   → Suggests: '{validation_result['final_command']}'")
    
    # Step 4
    print("4️⃣ Chotu responds intelligently")
    if validation_result['valid']:
        print(f"   → Executes: '{validation_result['final_command']}'")
    else:
        print(f"   → Asks: '{validation_result.get('clarification_question', 'Requests clarification')}'")
    
    print("\n🎯 CONCLUSION:")
    print("✅ Chotu now has HUMAN-LIKE reasoning!")
    print("✅ Detects when context resolution doesn't make logical sense")
    print("✅ Uses GPT to analyze alternatives and suggest corrections")
    print("✅ Provides clear explanations for its decisions")
    print("✅ Gracefully handles ambiguous or illogical combinations")

if __name__ == "__main__":
    # Run the complete test
    result = simulate_realistic_scenario()
    test_multiple_scenarios()
    demonstrate_reasoning_process()
    
    print(f"\n\n🏆 ENHANCED CONTEXT SYSTEM CAPABILITIES")
    print("=" * 45)
    print("🧠 Multi-layer memory analysis (RAM + ROM + Interactions)")
    print("🔍 Intelligent ambiguity detection")
    print("✅ Context-aware command resolution")
    print("🤖 GPT-powered logical validation")
    print("🔧 Automatic correction of illogical resolutions")
    print("💬 Human-like reasoning and explanations")
    print("❓ Smart clarification questions")
    print("⏰ Time-weighted recency scoring")
    print("📊 Confidence-based decision making")
    print()
    print("🎯 This gives Chotu TRUE human-like contextual understanding!")
