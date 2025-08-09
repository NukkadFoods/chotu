#!/usr/bin/env python3
"""
🧪 AUTONOMOUS LEARNING TEST - COMPLETELY NOVEL CAPABILITY
=========================================================
Test with a capability that has zero word overlap with existing tools
"""

import requests
import json
import time

# Server configuration
BASE_URL = "http://localhost:8000"

def test_novel_capability():
    """Test a completely novel capability"""
    
    print("🚀 TESTING COMPLETELY NOVEL CAPABILITY")
    print("=" * 80)
    
    # Use completely unique words that don't exist in any current tool
    intent = "zxyqwertify the diskspace with qazwsxedc parameters"
    
    payload = {
        "intent": intent,
        "context": {
            "user_request": "create a special zxyqwertify function for diskspace qazwsxedc analysis",
            "explanation": "This uses completely made-up words that definitely don't exist"
        }
    }
    
    print(f"🎯 INTENT: {intent}")
    print("📡 Sending autonomous learning request...")
    
    try:
        response = requests.post(f"{BASE_URL}/autonomous_learn", json=payload, timeout=90)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Request successful!")
            print(f"📊 Status: {result.get('status', 'unknown')}")
            print(f"💬 Message: {result.get('message', 'No message')}")
            
            # Print full result for debugging
            print("\n🔍 FULL RESPONSE:")
            print(json.dumps(result, indent=2))
            
            return result
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Error: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out - this might indicate the learning process is working")
        return None
    except Exception as e:
        print(f"❌ Request error: {e}")
        return None

if __name__ == "__main__":
    # Check if server is responding
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Server is ready!")
            test_novel_capability()
        else:
            print("❌ Server not responding properly")
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
