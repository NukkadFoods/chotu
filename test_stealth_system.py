#!/usr/bin/env python3
"""
Test the Updated Autonomous System with Stealth Browser
"""

import asyncio
from chotu_autonomous import ChouAutonomous

async def test_chrome_opening():
    """Test stealth Chrome opening"""
    print("🧪 Testing Stealth Chrome Opening")
    print("=" * 50)
    
    try:
        autonomous = ChouAutonomous()
        
        # Test chrome opening
        result = await autonomous.process_user_input("open chrome")
        print(f"Chrome Opening Result: {result}")
        
        # Wait a bit for browser to open
        await asyncio.sleep(3)
        
        return "✅ Chrome test completed"
        
    except Exception as e:
        print(f"❌ Chrome test failed: {e}")
        import traceback
        traceback.print_exc()
        return f"❌ Error: {e}"

async def test_amazon_search():
    """Test Amazon search with parameter substitution"""
    print("\n🛒 Testing Amazon Search with Dynamic Parameters")
    print("=" * 50)
    
    try:
        autonomous = ChouAutonomous()
        
        # Test Amazon search
        test_commands = [
            "search mushrooms on amazon.com",
            "search for books on amazon",
            "find laptops on amazon.com"
        ]
        
        for command in test_commands:
            print(f"\nTesting: '{command}'")
            result = await autonomous.process_user_input(command)
            print(f"Result: {result}")
            await asyncio.sleep(2)  # Wait between tests
        
        return "✅ Amazon search tests completed"
        
    except Exception as e:
        print(f"❌ Amazon search test failed: {e}")
        import traceback
        traceback.print_exc()
        return f"❌ Error: {e}"

async def main():
    print("🚀 Testing Updated Autonomous System")
    print("Testing stealth browser and dynamic parameter substitution")
    print("=" * 60)
    
    # Test chrome opening first
    chrome_result = await test_chrome_opening()
    print(f"\n{chrome_result}")
    
    # Test amazon search
    amazon_result = await test_amazon_search()
    print(f"\n{amazon_result}")
    
    print("\n🏁 All tests completed!")

if __name__ == "__main__":
    asyncio.run(main())
