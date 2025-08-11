#!/usr/bin/env python3
"""
🧪 MASSIVE CONTEXT SYSTEM TEST
==============================
Test hundreds of commands to show reasoning pipeline:
- What Chotu thinks (context resolution)
- What GPT thinks (logical validation)  
- Final output
"""

import sys
import os
import random
from datetime import datetime

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.intelligent_context_resolver import resolve_ambiguous_command
from memory.context_validator import validate_context_resolution
from memory.context_manager import ContextManager

def setup_realistic_context():
    """Setup a realistic conversation context"""
    context = ContextManager()
    
    # Various interactions to create complex context
    interactions = [
        ("set brightness to 80%", "✅ Brightness set to 80%"),
        ("open chrome browser", "✅ Chrome opened successfully"),
        ("turn on bluetooth", "✅ Bluetooth enabled"),
        ("set volume to 60%", "✅ Volume set to 60%"),
        ("open safari", "✅ Safari opened"),
        ("enable wifi", "✅ WiFi enabled"),
        ("open terminal", "✅ Terminal opened"),
        ("increase brightness to 90%", "✅ Brightness set to 90%"),
        ("connect bluetooth device", "✅ Connected to AirPods"),
        ("open finder", "✅ Finder opened"),
        ("set volume to 70%", "✅ Volume set to 70%"),
        ("disable bluetooth", "✅ Bluetooth disabled"),
        ("close safari", "✅ Safari closed"),
        ("turn off wifi", "✅ WiFi disabled"),
        ("open youtube", "✅ YouTube opened in browser")
    ]
    
    for user_input, response in interactions:
        context.add_interaction(user_input, response, True)
    
    return context

def generate_test_commands():
    """Generate hundreds of test commands covering all scenarios"""
    
    # Base ambiguous commands
    base_commands = [
        "increase it", "decrease it", "turn it off", "turn it on", "close it", "open it",
        "set it to 50", "make it louder", "make it brighter", "disable it", "enable it",
        "start it", "stop it", "pause it", "play it", "turn up it", "turn down it",
        "activate it", "deactivate it", "switch it", "toggle it", "reset it", "restart it"
    ]
    
    # Add variations with numbers/percentages
    numbered_commands = []
    for cmd in base_commands:
        if "set" in cmd or "increase" in cmd or "decrease" in cmd:
            numbers = ["10", "25", "50", "75", "100", "10%", "25%", "50%", "75%", "100%"]
            for num in numbers:
                numbered_commands.append(cmd.replace("50", num))
    
    # Add contextual variations
    contextual_commands = [
        "make this brighter", "turn that off", "close them", "open those",
        "increase the volume", "decrease the brightness", "turn off the bluetooth",
        "make it half", "set it maximum", "turn it all the way up", "make it minimum",
        "switch this on", "toggle that setting", "activate the wifi", "disable the sound"
    ]
    
    # Add commands with hints
    hint_commands = [
        "make the screen brighter", "turn the volume up", "close the browser",
        "open the application", "disable the connection", "enable the wireless",
        "increase the sound", "decrease the light", "turn off the network",
        "start the program", "stop the service", "pause the video"
    ]
    
    # Add completely ambiguous commands
    vague_commands = [
        "it", "this", "that", "them", "those", "the thing", "the setting",
        "more", "less", "higher", "lower", "on", "off", "better", "worse"
    ]
    
    all_commands = base_commands + numbered_commands + contextual_commands + hint_commands + vague_commands
    
    # Remove duplicates and return
    return list(set(all_commands))

def test_command_pipeline(command, test_num):
    """Test a single command through the full pipeline"""
    
    print(f"\n{'='*60}")
    print(f"TEST #{test_num}: '{command}'")
    print('='*60)
    
    # STEP 1: Context Resolution (What Chotu thinks)
    print("🧠 CHOTU THINKING:")
    context_result = resolve_ambiguous_command(command)
    
    print(f"   Ambiguous: {'YES' if context_result.get('needs_clarification', False) else 'NO'}")
    print(f"   Resolved: '{context_result['resolved_command']}'")
    print(f"   Confidence: {context_result['confidence']}%")
    print(f"   Source: {context_result['context_source']}")
    print(f"   Alternatives: {context_result['alternatives']}")
    
    # STEP 2: GPT Validation (What GPT thinks)
    print("\n🤖 GPT THINKING:")
    validation_result = validate_context_resolution(
        command,
        context_result['resolved_command'],
        context_result,
        context_result['alternatives']
    )
    
    print(f"   Valid: {'YES' if validation_result['valid'] else 'NO'}")
    print(f"   GPT Confidence: {validation_result.get('confidence', 'N/A')}%")
    print(f"   GPT Reasoning: {validation_result['reasoning'][:100]}...")
    
    # STEP 3: Final Decision
    print(f"\n🎯 FINAL OUTPUT:")
    final_cmd = validation_result['final_command']
    
    if validation_result['valid']:
        print(f"   ✅ EXECUTE: '{final_cmd}'")
        chotu_response = f"I understand you want to {final_cmd}"
    elif validation_result['needs_clarification']:
        clarification = validation_result.get('clarification_question', 'Please clarify')
        print(f"   🤔 ASK: '{clarification}'")
        chotu_response = clarification
    else:
        if validation_result.get('suggested_action'):
            suggested = validation_result['suggested_action']
            print(f"   🔧 SUGGEST: '{suggested}'")
            chotu_response = f"I think you meant {suggested}"
        else:
            print(f"   ❌ CONFUSED: Need more information")
            chotu_response = "I'm not sure what you want me to do"
    
    print(f"   🗣️  CHOTU SAYS: '{chotu_response}'")
    
    # Quick analysis
    analysis = analyze_result(command, context_result, validation_result)
    print(f"   📊 ANALYSIS: {analysis}")
    
    return {
        'command': command,
        'chotu_resolved': context_result['resolved_command'],
        'chotu_confidence': context_result['confidence'],
        'gpt_valid': validation_result['valid'],
        'final_output': final_cmd,
        'chotu_response': chotu_response,
        'analysis': analysis
    }

def analyze_result(command, context_result, validation_result):
    """Quick analysis of the result quality"""
    
    cmd_lower = command.lower()
    final_lower = validation_result['final_command'].lower()
    
    # Check if action is preserved
    actions = ['increase', 'decrease', 'turn', 'open', 'close', 'set', 'make']
    original_action = None
    final_action = None
    
    for action in actions:
        if action in cmd_lower:
            original_action = action
        if action in final_lower:
            final_action = action
    
    # Analysis categories
    if validation_result['valid']:
        return "✅ GOOD - Direct resolution worked"
    elif validation_result['needs_clarification']:
        return "🤔 UNCLEAR - Needs user input"
    elif original_action and final_action and original_action == final_action:
        return "🔧 CORRECTED - Action preserved, subject corrected"
    elif original_action and final_action and original_action != final_action:
        return "❌ BAD - Action changed incorrectly"
    elif 'NEEDS_CLARIFICATION' in validation_result['final_command']:
        return "❓ UNCERTAIN - System confused"
    else:
        return "⚠️ UNKNOWN - Unexpected result"

def run_massive_test():
    """Run the massive test with hundreds of commands"""
    
    print("🚀 MASSIVE CONTEXT SYSTEM TEST")
    print("Testing hundreds of commands through the full pipeline")
    print("Shows: Chotu thinking → GPT thinking → Final output")
    print()
    
    # Setup context
    print("📝 Setting up realistic context...")
    context = setup_realistic_context()
    print("✅ Context ready with 15 previous interactions")
    
    # Generate test commands
    print("\n🎲 Generating test commands...")
    commands = generate_test_commands()
    print(f"✅ Generated {len(commands)} unique test commands")
    
    # Run tests
    print(f"\n🧪 RUNNING {len(commands)} TESTS...")
    print("Format: Command → Chotu thinks → GPT thinks → Final output")
    
    results = []
    
    for i, command in enumerate(commands, 1):
        try:
            result = test_command_pipeline(command, i)
            results.append(result)
            
            # Brief pause every 10 tests
            if i % 10 == 0:
                print(f"\n⏸️  Completed {i}/{len(commands)} tests...")
                
        except Exception as e:
            print(f"\n❌ ERROR in test #{i} ('{command}'): {e}")
            continue
    
    # Summary analysis
    print(f"\n\n📊 SUMMARY ANALYSIS")
    print("="*50)
    
    total = len(results)
    good = len([r for r in results if r['analysis'].startswith('✅')])
    corrected = len([r for r in results if r['analysis'].startswith('🔧')])
    unclear = len([r for r in results if r['analysis'].startswith('🤔')])
    bad = len([r for r in results if r['analysis'].startswith('❌')])
    
    print(f"Total Commands Tested: {total}")
    print(f"✅ Good Resolutions: {good} ({good/total*100:.1f}%)")
    print(f"🔧 Corrected Results: {corrected} ({corrected/total*100:.1f}%)")
    print(f"🤔 Unclear/Clarification: {unclear} ({unclear/total*100:.1f}%)")
    print(f"❌ Bad Results: {bad} ({bad/total*100:.1f}%)")
    
    # Show examples of each category
    print(f"\n📋 EXAMPLES BY CATEGORY:")
    
    categories = {
        '✅ GOOD': [r for r in results if r['analysis'].startswith('✅')][:3],
        '🔧 CORRECTED': [r for r in results if r['analysis'].startswith('🔧')][:3],
        '🤔 UNCLEAR': [r for r in results if r['analysis'].startswith('🤔')][:3],
        '❌ BAD': [r for r in results if r['analysis'].startswith('❌')][:3]
    }
    
    for category, examples in categories.items():
        if examples:
            print(f"\n{category}:")
            for ex in examples:
                print(f"   '{ex['command']}' → '{ex['final_output']}'")
    
    return results

def quick_pipeline_test():
    """Quick test showing just the pipeline for key commands"""
    
    print("⚡ QUICK PIPELINE TEST")
    print("="*30)
    
    key_commands = [
        "increase it",
        "turn it off", 
        "close it",
        "make it brighter",
        "set it to 50%",
        "disable it",
        "open it",
        "turn this up"
    ]
    
    context = setup_realistic_context()
    
    for i, cmd in enumerate(key_commands, 1):
        print(f"\n{i}. '{cmd}'")
        
        # Context resolution
        context_result = resolve_ambiguous_command(cmd)
        print(f"   🧠 Chotu: '{context_result['resolved_command']}' ({context_result['confidence']}%)")
        
        # GPT validation  
        validation_result = validate_context_resolution(
            cmd, context_result['resolved_command'], 
            context_result, context_result['alternatives']
        )
        
        valid_status = "✅" if validation_result['valid'] else "❌"
        print(f"   🤖 GPT: {valid_status} '{validation_result['final_command']}'")
        
        # Final output
        if validation_result['valid']:
            print(f"   🎯 Result: EXECUTE '{validation_result['final_command']}'")
        elif validation_result['needs_clarification']:
            print(f"   🎯 Result: ASK '{validation_result.get('clarification_question', 'Clarify')[:50]}...'")
        else:
            print(f"   🎯 Result: SUGGEST '{validation_result.get('suggested_action', 'Unknown')}'")

if __name__ == "__main__":
    print("🧪 CHOTU CONTEXT SYSTEM - MASSIVE TESTING")
    print("="*60)
    print("Choose test mode:")
    print("1. Quick pipeline test (8 commands)")
    print("2. Massive test (hundreds of commands)")
    print()
    
    try:
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == "1":
            quick_pipeline_test()
        elif choice == "2":
            run_massive_test()
        else:
            print("Running quick test by default...")
            quick_pipeline_test()
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        
    print("\n🏁 Testing complete!")
