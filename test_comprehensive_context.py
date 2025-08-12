#!/usr/bin/env python3
"""
🧪 COMPREHENSIVE CONTEXT RESOLUTION TEST
========================================
Simulate a realistic conversation flow to demonstrate
how Chotu resolves ambiguous commands using memory layers
"""

import sys
import os
import json
from datetime import datetime

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.intelligent_context_resolver import resolve_ambiguous_command, get_clarification_question
from memory.context_manager import ContextManager
from memory.memory_manager import save_ram

def simulate_conversation_scenario():
    """Simulate a realistic conversation to test context resolution"""
    
    print("🎭 SIMULATING REALISTIC CONVERSATION SCENARIO")
    print("=" * 60)
    
    # Initialize context manager
    context = ContextManager()
    
    # Scenario: User is working on their computer
    conversation_flow = [
        {
            "user": "set brightness to 80%",
            "chotu": "✅ Brightness set to 80%",
            "success": True
        },
        {
            "user": "open chrome browser",
            "chotu": "✅ Chrome opened successfully",
            "success": True
        },
        {
            "user": "search for python tutorials",
            "chotu": "✅ Opened Google Chrome and searched for 'python tutorials'",
            "success": True
        },
        {
            "user": "increase volume to 60%",
            "chotu": "✅ Volume set to 60%",
            "success": True
        },
        {
            "user": "play first search result",
            "chotu": "✅ Clicked first search result",
            "success": True
        }
    ]
    
    # Add all interactions to context
    print("📝 Building conversation history...")
    for i, interaction in enumerate(conversation_flow):
        context.add_interaction(
            interaction["user"], 
            interaction["chotu"], 
            interaction["success"]
        )
        print(f"   {i+1}. User: '{interaction['user']}' → Chotu: '{interaction['chotu']}'")
    
    print("\n🧠 NOW TESTING AMBIGUOUS COMMANDS:")
    print("-" * 40)
    
    # Test ambiguous commands that should be resolvable
    test_commands = [
        "increase it",           # Should refer to volume (most recent numeric setting)
        "decrease it by 10%",    # Should refer to volume
        "make it brighter",      # Should refer to brightness (contains hint)
        "close it",              # Should refer to chrome (most recent app opened)
        "set it to 70",          # Could be volume or brightness - should ask for clarification
        "turn it off",           # Should refer to chrome (most recent controllable app)
        "open it again",         # Should refer to chrome
    ]
    
    for cmd in test_commands:
        print(f"\n🔍 User says: '{cmd}'")
        
        # Resolve the command
        result = resolve_ambiguous_command(cmd)
        
        print(f"   🎯 Resolution:")
        print(f"      Resolved: {result['resolved']}")
        print(f"      Confidence: {result['confidence']}%")
        print(f"      Command: '{result['resolved_command']}'")
        print(f"      Source: {result['context_source']}")
        print(f"      Reasoning: {result['reasoning']}")
        
        if result['alternatives']:
            print(f"      Alternatives: {result['alternatives']}")
        
        if result['needs_clarification']:
            question = get_clarification_question(result['alternatives'], cmd)
            print(f"      🤔 Chotu asks: '{question}'")
        else:
            print(f"      ✅ Chotu would execute: '{result['resolved_command']}'")

def test_edge_cases():
    """Test edge cases and corner scenarios"""
    
    print("\n\n🔬 TESTING EDGE CASES")
    print("=" * 30)
    
    edge_cases = [
        "it",                    # Just "it" - should need clarification
        "increase",              # Action without object
        "set the thing to 50",   # Ambiguous object
        "make them louder",      # Plural ambiguous reference
        "turn everything off",   # Multiple objects
        "brightness to 90%",     # Clear command - should not need resolution
    ]
    
    for cmd in edge_cases:
        print(f"\n🔍 Edge case: '{cmd}'")
        result = resolve_ambiguous_command(cmd)
        
        if result['needs_clarification']:
            question = get_clarification_question(result['alternatives'], cmd)
            print(f"   🤔 Needs clarification: '{question}'")
        else:
            print(f"   ✅ Resolved to: '{result['resolved_command']}' (confidence: {result['confidence']}%)")

def demonstrate_memory_layers():
    """Demonstrate how different memory layers are used"""
    
    print("\n\n🏗️  MEMORY LAYER DEMONSTRATION")
    print("=" * 35)
    
    # Create some RAM data to simulate current session
    ram_data = {
        "raw_input": "set chrome volume to 75%",
        "timestamp": datetime.now().isoformat(),
        "nlp_analysis": {
            "intent": "system_control",
            "parameters": {"app_name": "chrome", "control_type": "volume"}
        },
        "memory_context": "User recently opened Chrome and set volume"
    }
    save_ram(ram_data)
    
    print("📊 Memory Layer Analysis for: 'increase it'")
    print("-" * 45)
    
    from memory.intelligent_context_resolver import IntelligentContextResolver
    resolver = IntelligentContextResolver()
    
    # Get detailed context results
    ambiguity_analysis = resolver._analyze_ambiguity("increase it")
    context_results = resolver._search_all_context_layers("increase it", ambiguity_analysis)
    
    print(f"🔍 Ambiguity Analysis:")
    print(f"   Is ambiguous: {ambiguity_analysis['is_ambiguous']}")
    print(f"   Action: {ambiguity_analysis['action']}")
    print(f"   Ambiguous reference: {ambiguity_analysis['ambiguous_reference']}")
    
    print(f"\n📚 Context Layer Results:")
    for layer, subjects in context_results.items():
        if subjects:
            print(f"   {layer.replace('_', ' ').title()}: {len(subjects)} subjects found")
            for subject in subjects[:2]:  # Show top 2
                print(f"      • {subject['subject']} (confidence: {subject.get('confidence', 'N/A')})")
        else:
            print(f"   {layer.replace('_', ' ').title()}: No subjects found")
    
    print(f"\n🎯 Final Resolution:")
    result = resolve_ambiguous_command("increase it")
    print(f"   Command: '{result['resolved_command']}'")
    print(f"   Confidence: {result['confidence']}%")
    print(f"   Source: {result['context_source']}")

if __name__ == "__main__":
    print("🤖 CHOTU INTELLIGENT CONTEXT RESOLUTION - COMPREHENSIVE TEST")
    print("=" * 70)
    
    # Run all tests
    simulate_conversation_scenario()
    test_edge_cases()
    demonstrate_memory_layers()
    
    print("\n\n✅ COMPREHENSIVE TESTING COMPLETED!")
    print("🧠 The intelligent context resolver demonstrates:")
    print("   • Multi-layer memory analysis (RAM, ROM, recent interactions)")
    print("   • Confidence-based resolution with alternatives")
    print("   • Human-like reasoning for ambiguous commands")
    print("   • Graceful handling of unclear contexts")
    print("   • Time-based recency scoring")
    print("   • Subject categorization and controllability analysis")
