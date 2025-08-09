#!/usr/bin/env python3
"""
🔍 BLUETOOTH COMMAND DEBUGGING
============================
Diagnose empty reply issues from MCP server
"""

import subprocess
import requests
import json
import time
from datetime import datetime

def test_blueutil_directly():
    """Test blueutil commands directly"""
    print("🔧 TESTING BLUEUTIL DIRECTLY")
    print("=" * 40)
    
    commands = [
        ["blueutil", "--paired"],
        ["blueutil", "--connected"], 
        ["blueutil", "--power"]
    ]
    
    for cmd in commands:
        try:
            print(f"⚡ Running: {' '.join(cmd)}")
            start_time = time.time()
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            end_time = time.time()
            
            print(f"✅ Exit code: {result.returncode}")
            print(f"⏱️ Time taken: {end_time - start_time:.2f}s")
            print(f"📤 stdout: {result.stdout[:200]}...")
            print(f"📥 stderr: {result.stderr}")
            print("-" * 30)
            
        except subprocess.TimeoutExpired:
            print(f"⏰ TIMEOUT after 5 seconds")
            print("-" * 30)
        except Exception as e:
            print(f"❌ Error: {e}")
            print("-" * 30)

def test_mcp_bluetooth_function():
    """Test the MCP bluetooth function directly"""
    print("\n🏗️ TESTING MCP BLUETOOTH FUNCTION")
    print("=" * 40)
    
    try:
        import sys
        sys.path.append('/Users/mahendrabahubali/chotu/mcp')
        
        # Import the function directly
        from mcp_server import list_bluetooth_devices
        
        print("🔄 Calling list_bluetooth_devices() directly...")
        start_time = time.time()
        result = list_bluetooth_devices()
        end_time = time.time()
        
        print(f"✅ Result: {result}")
        print(f"⏱️ Time taken: {end_time - start_time:.2f}s")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def test_mcp_server_requests():
    """Test MCP server with different request patterns"""
    print("\n🌐 TESTING MCP SERVER REQUESTS")
    print("=" * 40)
    
    test_requests = [
        {"intent": "list bluetooth devices", "timeout": 3},
        {"intent": "bluetooth devices", "timeout": 3},
        {"intent": "show bluetooth devices", "timeout": 3},
        {"intent": "enable bluetooth", "timeout": 3},
    ]
    
    for req in test_requests:
        try:
            print(f"📡 Testing: '{req['intent']}'")
            start_time = time.time()
            
            response = requests.post('http://localhost:8000/execute', 
                                   json={'intent': req['intent']}, 
                                   timeout=req['timeout'])
            
            end_time = time.time()
            
            print(f"✅ Status: {response.status_code}")
            print(f"⏱️ Time taken: {end_time - start_time:.2f}s")
            
            if response.status_code == 200:
                result = response.json()
                print(f"📄 Response: {str(result)[:200]}...")
            else:
                print(f"📄 Raw response: {response.text[:200]}...")
                
            print("-" * 30)
            
        except requests.exceptions.Timeout:
            print(f"⏰ REQUEST TIMEOUT after {req['timeout']}s")
            print("-" * 30)
        except Exception as e:
            print(f"❌ Error: {e}")
            print("-" * 30)

def test_context_history():
    """Check context history for patterns"""
    print("\n📚 CHECKING CONTEXT HISTORY")
    print("=" * 40)
    
    try:
        with open('/Users/mahendrabahubali/chotu/memory/context.json', 'r') as f:
            context = json.load(f)
        
        bluetooth_interactions = [
            interaction for interaction in context.get('interactions', [])
            if 'bluetooth' in interaction.get('user_input', '').lower()
        ]
        
        print(f"🔍 Found {len(bluetooth_interactions)} Bluetooth interactions:")
        
        for interaction in bluetooth_interactions[-5:]:  # Last 5
            print(f"📅 {interaction.get('timestamp', 'unknown')}")
            print(f"👤 Input: {interaction.get('user_input', 'unknown')}")
            print(f"🤖 Response: {interaction.get('chotu_response', 'unknown')}")
            print(f"✅ Success: {interaction.get('success', 'unknown')}")
            print("-" * 20)
            
    except Exception as e:
        print(f"❌ Error reading context: {e}")

if __name__ == "__main__":
    print("🔍 BLUETOOTH COMMAND DEBUGGING")
    print("=" * 60)
    print(f"⏰ Started at: {datetime.now()}")
    print()
    
    # Run all tests
    test_blueutil_directly()
    test_mcp_bluetooth_function()
    test_mcp_server_requests()
    test_context_history()
    
    print(f"\n⏰ Completed at: {datetime.now()}")
    print("🔍 DEBUGGING COMPLETE")
