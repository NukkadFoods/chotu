#!/usr/bin/env python3
"""
Test Clean Chrome Opening
"""

import asyncio
from chotu_autonomous import ChouAutonomous

async def test_clean_chrome():
    print("🧪 Testing Clean Chrome Opening")
    print("=" * 40)
    
    try:
        autonomous = ChouAutonomous()
        
        # Test chrome opening
        print("Opening Chrome with clean logging...")
        result = await autonomous.process_user_input("open chrome")
        print(f"Result: {result}")
        
        return "✅ Test completed"
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return f"❌ Error: {e}"

if __name__ == "__main__":
    asyncio.run(test_clean_chrome())
