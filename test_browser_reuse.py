#!/usr/bin/env python3
"""
Test improved browser instance management and password vault integration
"""
import asyncio
import sys
import os

# Add the parent directory to the path so we can import chotu_autonomous
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chotu_autonomous import ChouAutonomous

async def test_browser_reuse():
    """Test that multiple commands reuse the same browser instance"""
    
    print("🧪 Testing Browser Instance Reuse")
    print("=" * 60)
    
    # Initialize Chotu Autonomous
    chotu = ChouAutonomous()
    
    try:
        # Test 1: Open first website
        print("🧪 Test 1: Open instagram.com")
        print("-" * 40)
        result1 = await chotu.process_user_input("Open Chrome and search instagram.com")
        print(f"📊 Result 1: {result1[:100]}...")
        
        print("\n" + "="*60)
        
        # Test 2: Open second website in new tab (should reuse browser)
        print("🧪 Test 2: Open amazon.com in new tab")
        print("-" * 40)
        result2 = await chotu.process_user_input("open amazon.com on next tab")
        print(f"📊 Result 2: {result2[:100]}...")
        
        print("\n" + "="*60)
        
        # Test 3: Try Instagram login (should attempt auto-login)
        print("🧪 Test 3: Login to Instagram")
        print("-" * 40)
        result3 = await chotu.process_user_input("login to instagram.com")
        print(f"📊 Result 3: {result3[:100]}...")
        
        print("\n✅ All tests completed!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean shutdown
        try:
            if hasattr(chotu, 'autonomous_executor') and chotu.autonomous_executor:
                chotu.autonomous_executor.shutdown()
        except Exception as e:
            print(f"⚠️  Shutdown warning: {e}")

if __name__ == "__main__":
    print("🧪 Browser Reuse & Password Vault Test")
    print("Testing improved browser management...")
    
    # Run the async test
    asyncio.run(test_browser_reuse())
