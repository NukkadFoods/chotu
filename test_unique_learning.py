#!/usr/bin/env python3
"""
🧪 AUTONOMOUS LEARNING DEMO TESTS - UNIQUE CAPABILITIES
======================================================
Test the self-learning system with truly unique capabilities
"""

import requests
import json
import time
from datetime import datetime

# Server configuration
BASE_URL = "http://localhost:8000"

def test_learning_request(intent, context=None, test_name=""):
    """Test a learning request"""
    print(f"\n{'='*60}")
    print(f"🧪 TEST: {test_name}")
    print(f"🎯 INTENT: {intent}")
    print(f"{'='*60}")
    
    payload = {
        "intent": intent,
        "context": context or {}
    }
    
    try:
        # Test autonomous learning
        print("📡 Sending autonomous learning request...")
        response = requests.post(f"{BASE_URL}/autonomous_learn", json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Request successful!")
            print(f"📊 Status: {result.get('status', 'unknown')}")
            print(f"💬 Message: {result.get('message', 'No message')}")
            
            if 'details' in result:
                details = result['details']
                print(f"🔧 Approach: {details.get('approach', 'unknown')}")
                if 'tool_created' in details:
                    print(f"🛠️ Tool Created: {details['tool_created']}")
                if 'module_enhanced' in details:
                    print(f"🔧 Module Enhanced: {details['module_enhanced']}")
                    print(f"🔧 Function Added: {details.get('function_added', 'unknown')}")
            
            return result
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Error: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out - checking server logs...")
        return None
    except Exception as e:
        print(f"❌ Request error: {e}")
        return None

def run_unique_tests():
    """Run tests with unique capabilities"""
    
    print("🚀 TESTING UNIQUE LEARNING CAPABILITIES")
    print("=" * 80)
    
    # Test 1: Very specific unique capability
    test_learning_request(
        "generate system performance report with timestamp",
        {"user_request": "create a detailed performance report with current timestamp"},
        "Unique System Report Generator"
    )
    
    time.sleep(3)
    
    # Test 2: Simple unique capability
    test_learning_request(
        "create temporary test file with random content",
        {"user_request": "make a temp file with some random text"},
        "Simple Temp File Creator"
    )
    
    time.sleep(3)
    
    # Test 3: Very simple capability
    test_learning_request(
        "display current timestamp in pretty format",
        {"user_request": "show me the current time in a nice format"},
        "Pretty Timestamp Display"
    )

if __name__ == "__main__":
    # Check if server is responding
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Server is ready!")
            run_unique_tests()
        else:
            print("❌ Server not responding properly")
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("Make sure the MCP server is running on localhost:8000")
