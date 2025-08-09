#!/usr/bin/env python3
"""
🧪 AUTONOMOUS LEARNING TEST - REALISTIC HIGH PRIORITY
====================================================
Test with a realistic capability that should be high priority
"""

import requests
import json
import time

# Server configuration
BASE_URL = "http://localhost:8000"

def test_realistic_capability():
    """Test a realistic high-priority capability"""
    
    print("🚀 TESTING REALISTIC HIGH-PRIORITY CAPABILITY")
    print("=" * 80)
    
    # A realistic capability that's useful and should be high priority
    intent = "get battery percentage and charging status"
    
    payload = {
        "intent": intent,
        "context": {
            "user_request": "I want to check my MacBook's battery level and if it's charging",
            "priority": "high",
            "urgency": "user requested feature"
        }
    }
    
    print(f"🎯 INTENT: {intent}")
    print("📡 Sending autonomous learning request...")
    
    try:
        response = requests.post(f"{BASE_URL}/autonomous_learn", json=payload, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Request successful!")
            print(f"📊 Status: {result.get('status', 'unknown')}")
            print(f"💬 Message: {result.get('message', 'No message')}")
            
            # Print relevant parts of the response
            if 'plan' in result:
                plan = result['plan']
                print(f"\n📋 LEARNING PLAN:")
                print(f"   Priority: {plan.get('priority_level', 'unknown')}")
                print(f"   Effort: {plan.get('estimated_effort', 'unknown')}")
                print(f"   Type: {plan.get('implementation_type', 'unknown')}")
                
            if 'details' in result:
                details = result['details']
                print(f"\n🔧 IMPLEMENTATION:")
                print(f"   Approach: {details.get('approach', 'unknown')}")
                if 'tool_created' in details:
                    print(f"   Tool Created: {details['tool_created']}")
                    
            # Check if learning actually happened
            if result.get('status') == 'success':
                print("\n🎉 LEARNING SUCCESS! Let's verify the new tool...")
                
                # Check learning stats
                stats_response = requests.get(f"{BASE_URL}/learning_stats")
                if stats_response.status_code == 200:
                    stats = stats_response.json()
                    print(f"📊 Updated Stats - Success Rate: {stats.get('success_rate', 0):.1f}%")
                    print(f"🛠️ Tools Generated: {stats.get('tools_generated', 0)}")
            
            return result
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Error: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out - checking if learning is in progress...")
        # Check server logs
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
            test_realistic_capability()
        else:
            print("❌ Server not responding properly")
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
