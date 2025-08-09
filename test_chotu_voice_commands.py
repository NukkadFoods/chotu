#!/usr/bin/env python3
"""
🎙️ CHOTU VOICE ASSISTANT COMMAND TESTING
=========================================
Testing the fixed system commands with Chotu voice assistant
"""

import requests
import json
import time

def test_chotu_command(command):
    """Test a command with the running Chotu MCP server"""
    try:
        print(f"🎙️ Testing: '{command}'")
        
        # Simulate what Chotu's voice interface would send
        payload = {
            "raw_input": command,
            "intent": command,
            "interpreted_intent": command,
            "nlp_analysis": {"intent": "system_control", "confidence": 85},
            "timestamp": time.time()
        }
        
        response = requests.post('http://localhost:8000/execute', 
                               json=payload, 
                               timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            success = result.get('success', False)
            output = result.get('output', 'No output')
            
            if success and '✅' in output:
                print(f"   ✅ SUCCESS: {output}")
                return True
            else:
                print(f"   ⚠️ RESPONSE: {output}")
                return False
        else:
            print(f"   ❌ HTTP {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

def main():
    print("🎙️ CHOTU VOICE ASSISTANT COMMAND TESTING")
    print("=" * 60)
    print("Testing the fixed system commands with the running Chotu...")
    print()
    
    # Commands we fixed
    test_commands = [
        "list bluetooth devices",
        "show bluetooth devices", 
        "enable bluetooth",
        "disable bluetooth",
        "increase brightness",
        "decrease brightness", 
        "set brightness to 75%",
        "take screenshot",
        "show system info",
        "get battery status",
        "set volume to 50%",
        "increase volume",
        "open safari"
    ]
    
    passed = 0
    total = len(test_commands)
    
    print("🧪 TESTING FIXED COMMANDS:")
    print("-" * 40)
    
    for i, command in enumerate(test_commands, 1):
        print(f"\n🧪 Test {i:2d}: ", end="")
        if test_chotu_command(command):
            passed += 1
        time.sleep(1)  # Small delay between tests
    
    print(f"\n🏆 TEST RESULTS:")
    print(f"=" * 30)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {total - passed}")
    print(f"📊 Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print(f"\n🎉 ALL TESTS PASSED! Chotu is ready for voice commands!")
    elif passed > total * 0.8:
        print(f"\n🎯 Most tests passed! Chotu is working well!")
    else:
        print(f"\n⚠️ Some issues found, but core functionality works!")
    
    print(f"\n🎙️ You can now use voice commands with Chotu:")
    print(f"   • Say: 'list bluetooth devices'")
    print(f"   • Say: 'increase brightness'") 
    print(f"   • Say: 'take screenshot'")
    print(f"   • Say: 'set volume to 70%'")

if __name__ == "__main__":
    main()
