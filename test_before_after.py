#!/usr/bin/env python3
"""
🔄 BEFORE vs AFTER COMPARISON
=============================
Compare old generic clarification vs new intelligent context analysis
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.prompt_completeness_analyzer import PromptCompletenessAnalyzer

def demonstrate_improvement():
    """Demonstrate the improvement from generic to intelligent clarification"""
    
    print("🔄 BEFORE vs AFTER: Generic vs Intelligent Context Analysis")
    print("="*70)
    
    analyzer = PromptCompletenessAnalyzer()
    
    # Realistic context where Chrome is open
    ram_context = [
        {
            "user_input": "open chrome browser",
            "response": "✅ Chrome opened successfully",
            "timestamp": "2025-08-12T10:01:00"
        },
        {
            "user_input": "set brightness to 90%", 
            "response": "✅ Brightness set to 90%",
            "timestamp": "2025-08-12T10:02:00"
        },
        {
            "user_input": "turn on bluetooth",
            "response": "✅ Bluetooth enabled",
            "timestamp": "2025-08-12T10:03:00"
        }
    ]
    
    rom_context = [
        {
            "pattern": "user frequently opens chrome browser",
            "frequency": 25,
            "last_used": "2025-08-12"
        },
        {
            "pattern": "user closes chrome when done browsing", 
            "frequency": 20,
            "last_used": "2025-08-11"
        },
        {
            "pattern": "user adjusts brightness regularly",
            "frequency": 18,
            "last_used": "2025-08-12"
        }
    ]
    
    chat_history = [
        {"role": "user", "content": "open chrome browser"},
        {"role": "assistant", "content": "Opening Chrome browser"},
        {"role": "user", "content": "set brightness to 90%"},
        {"role": "assistant", "content": "Setting brightness to 90%"}
    ]
    
    # Test problematic cases
    test_cases = [
        {
            "prompt": "chrome",
            "old_response": "❓ Could you please provide more information or context about what specifically you need related to 'chrome'?",
            "new_expectation": "Chrome is open. Do you want to close it?"
        },
        {
            "prompt": "it",
            "old_response": "❓ Could you please provide more context or specify what 'it' refers to?",
            "new_expectation": "Should refer to brightness (last mentioned)"
        },
        {
            "prompt": "turn it off",
            "old_response": "❓ What specific device or function would you like me to turn off?",
            "new_expectation": "Should suggest bluetooth or chrome based on context"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"TEST CASE {i}: '{test_case['prompt']}'")
        print('='*70)
        
        print(f"❌ OLD SYSTEM (Generic):")
        print(f"   {test_case['old_response']}")
        print(f"   → User frustration: No context awareness!")
        
        print(f"\n✅ NEW SYSTEM (Intelligent):")
        
        # Run new analysis
        analysis = analyzer.analyze_prompt_completeness(
            test_case['prompt'],
            ram_context,
            rom_context,
            chat_history
        )
        
        print(f"   Confidence: {analysis['completeness_confidence']}%")
        
        if analysis.get('clarification', {}).get('needed', False):
            clarification = analysis['clarification']
            print(f"   Question: {clarification['question']}")
            
            if clarification.get('options'):
                print(f"   Smart Options:")
                for j, option in enumerate(clarification['options'], 1):
                    print(f"      {j}. {option}")
                    
            if clarification.get('safety_warning'):
                print(f"   ⚠️  Safety: {clarification['safety_warning']}")
        else:
            exec_plan = analysis.get('execution_plan', {})
            if exec_plan.get('potential_command'):
                print(f"   Direct Execution: '{exec_plan['potential_command']}'")
        
        print(f"   → User experience: Context-aware and helpful!")

def show_intelligence_breakdown():
    """Show how the intelligence analysis works step by step"""
    
    print(f"\n\n🧠 INTELLIGENCE ANALYSIS BREAKDOWN")
    print("="*70)
    
    analyzer = PromptCompletenessAnalyzer()
    
    # Chrome is open scenario
    ram_context = [
        {
            "user_input": "open chrome browser",
            "response": "✅ Chrome opened successfully", 
            "timestamp": "2025-08-12T10:01:00"
        }
    ]
    
    rom_context = [
        {
            "pattern": "user frequently closes chrome when done",
            "frequency": 20,
            "last_used": "2025-08-11"
        }
    ]
    
    chat_history = [
        {"role": "user", "content": "open chrome browser"},
        {"role": "assistant", "content": "Chrome opened successfully"}
    ]
    
    print("SCENARIO: User says 'chrome' when Chrome is currently open")
    print("CONTEXT: Chrome was just opened, user frequently closes Chrome when done")
    
    # Test the intelligence analysis directly
    context_data = {
        'user_prompt': 'chrome',
        'context_sources': {
            'ram_memory': {'entries': ram_context},
            'rom_memory': {'entries': rom_context},
            'chat_history': {'entries': chat_history}
        }
    }
    
    # Show intelligence analysis
    intelligence = analyzer._analyze_context_intelligence(context_data)
    print(f"\n🔍 CONTEXT INTELLIGENCE:")
    print(intelligence)
    
    # Run full analysis
    analysis = analyzer.analyze_prompt_completeness(
        'chrome',
        ram_context,
        rom_context,
        chat_history
    )
    
    print(f"\n🎯 FINAL DECISION:")
    print(f"Confidence: {analysis['completeness_confidence']}%")
    
    if analysis['execution_ready']:
        print("✅ Ready to execute!")
        exec_plan = analysis.get('execution_plan', {})
        if exec_plan.get('potential_command'):
            print(f"Command: {exec_plan['potential_command']}")
    else:
        print("❓ Needs clarification (but intelligent)")
        clarification = analysis.get('clarification', {})
        if clarification.get('question'):
            print(f"Question: {clarification['question']}")

if __name__ == "__main__":
    demonstrate_improvement()
    show_intelligence_breakdown()
