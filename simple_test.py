#!/usr/bin/env python3
"""
Simple Integration Test
Test the main Chotu system with a simple command
"""

import asyncio
from chotu_autonomous import ChouAutonomous

async def simple_test():
    print("🧪 Simple Integration Test")
    print("=" * 30)
    
    try:
        # Initialize the autonomous system
        autonomous = ChouAutonomous()
        print("✅ Autonomous system initialized")
        
        # Test a simple command
        result = await autonomous.process_user_input("open chrome")
        print(f"Result: {result}")
        
        # Test search command
        result2 = await autonomous.process_user_input("search for books on amazon")
        print(f"Search result: {result2}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(simple_test())
