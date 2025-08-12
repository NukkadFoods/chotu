#!/usr/bin/env python3
"""
Test script to verify "Open Chrome and search flipkart.com" functionality
"""
import asyncio
import sys
import os

# Add the parent directory to the path so we can import chotu_autonomous
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chotu_autonomous import ChouAutonomous

async def test_flipkart_search():
    """Test the flipkart search functionality"""
    
    print("🤖 Testing: 'Open Chrome and search flipkart.com'")
    print("=" * 50)
    
    # Initialize Chotu Autonomous
    chotu = ChouAutonomous()
    
    try:
        # Test the command that was failing
        test_command = "Open Chrome and search flipkart.com"
        
        print(f"📝 Command: {test_command}")
        print(f"🚀 Executing...")
        
        # Execute the command
        result_str = await chotu.process_user_input(test_command)
        
        print("\n📊 Results:")
        print(f"📝 Response: {result_str}")
        
        # Also check if we can get more detailed results from the executor
        if hasattr(chotu, 'autonomous_executor') and chotu.autonomous_executor:
            print("✅ Autonomous executor is available")
        else:
            print("⚠️  Autonomous executor not found")
        
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
    print("🧪 Flipkart Search Test")
    print("Testing improved autonomous command handling...")
    
    # Run the async test
    asyncio.run(test_flipkart_search())
