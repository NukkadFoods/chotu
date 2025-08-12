#!/usr/bin/env python3
"""
Test script to verify self-healing and new tab functionality
"""
import asyncio
import sys
import os

# Add the parent directory to the path so we can import chotu_autonomous
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chotu_autonomous import ChouAutonomous

async def test_commands():
    """Test various commands with self-healing"""
    
    print("🧪 Testing Self-Healing and New Tab Functionality")
    print("=" * 60)
    
    # Initialize Chotu Autonomous
    chotu = ChouAutonomous()
    
    test_commands = [
        "open amazon.com on next tab",
        "Open Chrome and search flipkart.com",
        "open instagram.com next to google.com step"
    ]
    
    for i, test_command in enumerate(test_commands, 1):
        print(f"\n🧪 Test {i}: {test_command}")
        print("-" * 40)
        
        try:
            print(f"📝 Command: {test_command}")
            print(f"🚀 Executing...")
            
            # Execute the command
            result_str = await chotu.process_user_input(test_command)
            
            print(f"📊 Result: {result_str}")
            
        except Exception as e:
            print(f"❌ Test {i} failed with error: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n" + "="*60)
    
    # Clean shutdown
    try:
        if hasattr(chotu, 'autonomous_executor') and chotu.autonomous_executor:
            chotu.autonomous_executor.shutdown()
    except Exception as e:
        print(f"⚠️  Shutdown warning: {e}")

if __name__ == "__main__":
    print("🔧 Self-Healing Test Suite")
    print("Testing improved command handling and automatic fixes...")
    
    # Run the async test
    asyncio.run(test_commands())
