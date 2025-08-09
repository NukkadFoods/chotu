#!/usr/bin/env python3
"""
Test the improved capability gap analyzer
"""

import sys
import os

# Add the correct path
sys.path.insert(0, '/Users/mahendrabahubali/chotu')
sys.path.insert(0, '/Users/mahendrabahubali/chotu/mcp/self_learning')

from code_analyzer import CodeAnalyzer

def test_analyzer():
    print("🧪 Testing Improved Capability Gap Analyzer")
    print("=" * 50)
    
    analyzer = CodeAnalyzer()
    
    # Test cases that should find existing capabilities
    test_cases = [
        "get battery percentage and charging status",
        "monitor battery level",
        "check network connectivity", 
        "open a file",
        "play music",
        "send an email",
        "get weather information"
    ]
    
    print(f"\n📊 Found {len(analyzer.known_tools)} tool modules")
    print(f"📋 Capability map: {len(analyzer.capability_map)} modules mapped")
    
    # Debug: Show what tools we found
    print(f"\n🔧 Available tools:")
    for module_name, functions in analyzer.known_tools.items():
        func_names = list(functions.keys())
        print(f"   {module_name}: {func_names[:3]}{'...' if len(func_names) > 3 else ''}")
    
    # Debug: Show specific modules we care about
    if 'battery_monitor' in analyzer.known_tools:
        print(f"\n🔋 Battery Monitor Functions: {list(analyzer.known_tools['battery_monitor'].keys())}")
    if 'play_music' in analyzer.known_tools:
        print(f"🎵 Play Music Functions: {list(analyzer.known_tools['play_music'].keys())}")
    if 'send_email' in analyzer.known_tools:
        print(f"📧 Send Email Functions: {list(analyzer.known_tools['send_email'].keys())}")
    
    print("\n" + "="*50)
    
    for intent in test_cases:
        print(f"\n🔍 Testing: '{intent}'")
        
        # First do intent analysis
        analysis = analyzer.analyze_intent(intent, analyzer.known_tools)
        
        print(f"   Intent Category: {analysis.get('intent_category', 'unknown')}")
        print(f"   Missing Capability: {analysis.get('missing_capability', 'unknown')}")
        print(f"   Confidence Score: {analysis.get('confidence_score', 0)}")
        
        # Then validate capability gap
        has_gap = analyzer.validate_capability_gap(intent, analysis)
        
        if has_gap:
            print(f"   ✅ CAPABILITY GAP DETECTED - Would generate new tool")
        else:
            print(f"   ❌ NO GAP - Existing capability found")
        
        print("-" * 40)

if __name__ == "__main__":
    test_analyzer()
