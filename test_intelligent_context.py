#!/usr/bin/env python3
"""
🧪 TEST INTELLIGENT CONTEXT ANALYSIS
=====================================
Test the enhanced completeness analyzer that intelligently uses RAM/ROM/chat history
"""

import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.prompt_completeness_analyzer import PromptCompletenessAnalyzer

def create_realistic_context():
    """Create realistic RAM, ROM, and chat context for testing"""
    
    # RAM Context (Recent interactions)
    ram_context = [
        {
            "user_input": "set brightness to 80%",
            "response": "✅ Brightness set to 80%",
            "timestamp": "2025-08-12T10:00:00"
        },
        {
            "user_input": "open chrome browser",
            "response": "✅ Chrome opened successfully",
            "timestamp": "2025-08-12T10:01:00"
        },
        {
            "user_input": "turn on bluetooth",
            "response": "✅ Bluetooth enabled",
            "timestamp": "2025-08-12T10:02:00"
        },
        {
            "user_input": "set volume to 60%",
            "response": "✅ Volume set to 60%",
            "timestamp": "2025-08-12T10:03:00"
        },
        {
            "user_input": "increase brightness to 90%",
            "response": "✅ Brightness set to 90%",
            "timestamp": "2025-08-12T10:04:00"
        }
    ]
    
    # ROM Context (Long-term patterns)
    rom_context = [
        {
            "pattern": "user frequently opens chrome browser",
            "frequency": 25,
            "last_used": "2025-08-12"
        },
        {
            "pattern": "user adjusts brightness regularly",
            "frequency": 18,
            "last_used": "2025-08-12"
        },
        {
            "pattern": "user controls bluetooth devices",
            "frequency": 12,
            "last_used": "2025-08-12"
        },
        {
            "pattern": "user closes chrome when done browsing",
            "frequency": 20,
            "last_used": "2025-08-11"
        },
        {
            "pattern": "user sets volume levels",
            "frequency": 15,
            "last_used": "2025-08-12"
        }
    ]
    
    # Chat History (Recent conversation)
    chat_history = [
        {"role": "user", "content": "set brightness to 80%"},
        {"role": "assistant", "content": "I'll set the brightness to 80%"},
        {"role": "user", "content": "open chrome browser"},
        {"role": "assistant", "content": "Opening Chrome browser"},
        {"role": "user", "content": "turn on bluetooth"},
        {"role": "assistant", "content": "Enabling Bluetooth"},
        {"role": "user", "content": "set volume to 60%"},
        {"role": "assistant", "content": "Setting volume to 60%"},
        {"role": "user", "content": "increase brightness to 90%"},
        {"role": "assistant", "content": "Increasing brightness to 90%"}
    ]
    
    return ram_context, rom_context, chat_history

def test_intelligent_context_analysis():
    """Test the intelligent context analysis with various scenarios"""
    
    print("🧪 TESTING INTELLIGENT CONTEXT ANALYSIS")
    print("="*60)
    
    analyzer = PromptCompletenessAnalyzer()
    ram_context, rom_context, chat_history = create_realistic_context()
    
    # Test scenarios that should now be much smarter
    test_cases = [
        {
            "prompt": "chrome",
            "description": "Single word - should analyze that Chrome is open and suggest close",
            "expected_intelligence": "Chrome is open, user likely wants to close it"
        },
        {
            "prompt": "it",
            "description": "Pronoun - should refer to last mentioned (brightness)",
            "expected_intelligence": "Should refer to brightness from recent context"
        },
        {
            "prompt": "turn it off",
            "description": "Ambiguous but should infer from context",
            "expected_intelligence": "Should suggest turning off bluetooth or chrome"
        },
        {
            "prompt": "brightness",
            "description": "Single word - should suggest adjustment based on current 90%",
            "expected_intelligence": "Brightness is at 90%, suggest adjustment"
        },
        {
            "prompt": "make it louder",
            "description": "Should refer to volume from recent context",
            "expected_intelligence": "Should refer to volume"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"TEST {i}: '{test_case['prompt']}'")
        print(f"SCENARIO: {test_case['description']}")
        print('='*60)
        
        # Run analysis
        analysis = analyzer.analyze_prompt_completeness(
            test_case['prompt'],
            ram_context,
            rom_context,
            chat_history
        )
        
        # Display results
        print(f"🎯 CONFIDENCE: {analysis['completeness_confidence']}%")
        print(f"📊 CATEGORY: {analysis['confidence_category']}")
        print(f"🚦 READY: {'✅ YES' if analysis['execution_ready'] else '❌ NO'}")
        
        # Show intelligent analysis
        if 'reasoning' in analysis:
            print(f"\n🧠 INTELLIGENT REASONING:")
            reasoning = analysis['reasoning'][:200] + "..." if len(analysis['reasoning']) > 200 else analysis['reasoning']
            print(f"   {reasoning}")
        
        # Show clarification (if needed)
        if analysis.get('clarification', {}).get('needed', False):
            clarification = analysis['clarification']
            print(f"\n❓ SMART CLARIFICATION:")
            print(f"   Question: {clarification['question']}")
            
            if 'options' in clarification and clarification['options']:
                print(f"   Options:")
                for j, option in enumerate(clarification['options'], 1):
                    print(f"      {j}. {option}")
            
            if 'safety_warning' in clarification and clarification['safety_warning']:
                print(f"   ⚠️  Safety: {clarification['safety_warning']}")
        
        # Show execution plan
        exec_plan = analysis.get('execution_plan', {})
        if exec_plan:
            print(f"\n🎯 EXECUTION PLAN:")
            print(f"   Action: {exec_plan.get('recommended_action', 'unknown')}")
            print(f"   Risk: {exec_plan.get('risk_level', 'unknown')}")
            if exec_plan.get('potential_command'):
                print(f"   Command: '{exec_plan['potential_command']}'")

def test_chrome_scenario_specifically():
    """Test the Chrome scenario specifically to show intelligent analysis"""
    
    print(f"\n\n🎯 SPECIFIC CHROME SCENARIO TEST")
    print("="*60)
    
    analyzer = PromptCompletenessAnalyzer()
    
    # Chrome is OPEN scenario
    ram_context_chrome_open = [
        {
            "user_input": "open chrome browser",
            "response": "✅ Chrome opened successfully",
            "timestamp": "2025-08-12T10:01:00"
        }
    ]
    
    rom_context_chrome = [
        {
            "pattern": "user frequently opens chrome browser",
            "frequency": 25,
            "last_used": "2025-08-12"
        },
        {
            "pattern": "user closes chrome when done browsing",
            "frequency": 20,
            "last_used": "2025-08-11"
        }
    ]
    
    chat_history_chrome = [
        {"role": "user", "content": "open chrome browser"},
        {"role": "assistant", "content": "Opening Chrome browser"}
    ]
    
    print("SCENARIO: Chrome is currently OPEN, user says 'chrome'")
    
    analysis = analyzer.analyze_prompt_completeness(
        "chrome",
        ram_context_chrome_open,
        rom_context_chrome,
        chat_history_chrome
    )
    
    print(f"🎯 CONFIDENCE: {analysis['completeness_confidence']}%")
    print(f"📊 CATEGORY: {analysis['confidence_category']}")
    
    if analysis.get('clarification', {}).get('needed', False):
        clarification = analysis['clarification']
        print(f"\n❓ INTELLIGENT CLARIFICATION:")
        print(f"   {clarification['question']}")
        
        if clarification.get('options'):
            print(f"   Suggested options:")
            for i, option in enumerate(clarification['options'], 1):
                print(f"      {i}. {option}")

if __name__ == "__main__":
    test_intelligent_context_analysis()
    test_chrome_scenario_specifically()
