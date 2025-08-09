#!/usr/bin/env python3
"""
🧪 AUTONOMOUS LEARNING DEMO TESTS
=================================
Test the self-learning system with various scenarios
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
        response = requests.post(f"{BASE_URL}/autonomous_learn", json=payload, timeout=30)
        
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
        print("⏰ Request timed out - this is normal for complex learning tasks")
        return None
    except Exception as e:
        print(f"❌ Request error: {e}")
        return None

def get_learning_stats():
    """Get current learning statistics"""
    try:
        response = requests.get(f"{BASE_URL}/learning_stats")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to get stats: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Stats error: {e}")
        return None

def run_demo_tests():
    """Run a series of demo tests"""
    
    print("🚀 STARTING AUTONOMOUS LEARNING DEMO TESTS")
    print("=" * 80)
    
    # Test 1: Simple system capability (might already exist)
    test_learning_request(
        "check CPU usage", 
        {"user_request": "I want to monitor CPU usage"},
        "System Monitoring - CPU Usage"
    )
    
    time.sleep(2)
    
    # Test 2: New productivity feature
    test_learning_request(
        "create a reminder for tomorrow",
        {"user_request": "set a reminder for tomorrow at 9 AM"},
        "Productivity - Reminder System"
    )
    
    time.sleep(2)
    
    # Test 3: File management capability
    test_learning_request(
        "compress files into zip archive",
        {"user_request": "zip these files together"},
        "File Management - ZIP Compression"
    )
    
    time.sleep(2)
    
    # Test 4: Network utility
    test_learning_request(
        "check internet speed",
        {"user_request": "test my internet connection speed"},
        "Network - Speed Test"
    )
    
    time.sleep(2)
    
    # Test 5: Media functionality
    test_learning_request(
        "convert image to different format",
        {"user_request": "convert PNG to JPG"},
        "Media - Image Conversion"
    )
    
    # Get final statistics
    print(f"\n{'='*80}")
    print("📊 FINAL LEARNING STATISTICS")
    print("=" * 80)
    
    stats = get_learning_stats()
    if stats:
        print(f"📈 Total Attempts: {stats.get('total_attempts', 0)}")
        print(f"✅ Successful: {stats.get('successful_attempts', 0)}")
        print(f"📊 Success Rate: {stats.get('success_rate', 0):.1f}%")
        print(f"🛠️ Tools Generated: {stats.get('tools_generated', 0)}")
        print(f"❌ Validation Errors: {stats.get('validation_errors', 0)}")
        print(f"🔒 Safety Mode: {'ON' if stats.get('safety_mode') else 'OFF'}")
        print(f"📊 Max Tools: {stats.get('max_tools', 0)}")
    
    print(f"\n🎉 Demo tests completed!")

if __name__ == "__main__":
    # Wait a moment for server to be fully ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(3)
    
    # Check if server is responding
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Server is ready!")
            run_demo_tests()
        else:
            print("❌ Server not responding properly")
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("Make sure the MCP server is running on localhost:8000")
