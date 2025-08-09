#!/usr/bin/env python3
"""
🔧 COMPREHENSIVE SYSTEM COMMAND TEST
=================================
Test all system commands that were previously failing with empty replies
"""

import requests
import json
import time
from datetime import datetime

def test_system_commands():
    """Test various system commands that were previously failing"""
    
    test_commands = [
        # Bluetooth commands
        {"intent": "list bluetooth devices", "expected": "📱 Bluetooth Devices"},
        {"intent": "bluetooth devices", "expected": "📱 Bluetooth Devices"},
        {"intent": "show bluetooth devices", "expected": "📱 Bluetooth Devices"},
        {"intent": "get bluetooth devices", "expected": "📱 Bluetooth Devices"},
        {"intent": "enable bluetooth", "expected": "✅ Bluetooth enabled"},
        {"intent": "disable bluetooth", "expected": "✅ Bluetooth disabled"},
        
        # Volume commands
        {"intent": "set volume to 50%", "expected": "✅"},
        {"intent": "increase volume", "expected": "✅"},
        {"intent": "turn up volume", "expected": "✅"},
        
        # Brightness commands
        {"intent": "set brightness to 75%", "expected": "✅"},
        {"intent": "increase brightness", "expected": "✅"},
        {"intent": "decrease brightness", "expected": "✅"},
        
        # Other system commands
        {"intent": "take screenshot", "expected": "✅"},
        {"intent": "show system info", "expected": ""},
        {"intent": "get battery status", "expected": ""},
        {"intent": "open safari", "expected": "✅"},
    ]
    
    print("🔧 COMPREHENSIVE SYSTEM COMMAND TEST")
    print("=" * 60)
    print(f"⏰ Started at: {datetime.now()}")
    print()
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_commands, 1):
        try:
            print(f"🧪 Test {i:2d}: '{test['intent']}'")
            
            start_time = time.time()
            response = requests.post('http://localhost:8000/execute', 
                                   json={'intent': test['intent']}, 
                                   timeout=10)
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                output = result.get('output', '')
                success = result.get('success', False)
                
                # Check if expected text is in output
                expected = test['expected']
                if expected and expected in output:
                    print(f"   ✅ PASS - Found '{expected}' in response")
                    print(f"   ⏱️ Time: {end_time - start_time:.2f}s")
                    passed += 1
                elif success and not expected:
                    print(f"   ✅ PASS - Command succeeded")
                    print(f"   ⏱️ Time: {end_time - start_time:.2f}s")
                    passed += 1
                else:
                    print(f"   ❌ FAIL - Expected '{expected}', got: {output[:100]}...")
                    print(f"   ⏱️ Time: {end_time - start_time:.2f}s")
                    failed += 1
                    
            else:
                print(f"   ❌ FAIL - HTTP {response.status_code}: {response.text[:100]}...")
                failed += 1
                
        except requests.exceptions.Timeout:
            print(f"   ⏰ TIMEOUT - Command took longer than 10 seconds")
            failed += 1
        except Exception as e:
            print(f"   ❌ ERROR - {e}")
            failed += 1
            
        print()
    
    print("🏆 TEST RESULTS")
    print("=" * 30)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Success Rate: {passed/(passed+failed)*100:.1f}%")
    print(f"⏰ Completed at: {datetime.now()}")
    
    return passed, failed

def test_previously_failing_commands():
    """Test commands that were specifically mentioned as failing"""
    
    print("\n🚨 TESTING PREVIOUSLY FAILING COMMANDS")
    print("=" * 50)
    
    # Commands from context history that failed
    failing_commands = [
        "can you tell me enable bluetooth devices",
        "I said give me bluetooth devices not enable", 
        "disable Bluetooth",
        "increase brightness to 80%"
    ]
    
    for cmd in failing_commands:
        try:
            print(f"🔍 Testing: '{cmd}'")
            response = requests.post('http://localhost:8000/execute', 
                                   json={'intent': cmd}, 
                                   timeout=8)
            
            if response.status_code == 200:
                result = response.json()
                success = result.get('success', False)
                output = result.get('output', '')
                
                if success:
                    print(f"   ✅ NOW WORKING: {output[:100]}...")
                else:
                    print(f"   ❌ Still failing: {output[:100]}...")
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
        
        print()

if __name__ == "__main__":
    print("🔧 SYSTEM COMMAND TESTING SUITE")
    print("=" * 70)
    print("Testing system commands for empty reply issues...")
    print()
    
    # Test main system commands
    passed, failed = test_system_commands()
    
    # Test previously failing commands
    test_previously_failing_commands()
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Empty reply issue resolved!")
    else:
        print(f"\n⚠️ {failed} tests still failing - needs more investigation")
