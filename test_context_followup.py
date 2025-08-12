#!/usr/bin/env python3
"""
Test the context-aware follow-up command functionality
"""
import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chotu_autonomous import ChouAutonomous

async def test_context_follow_up():
    """Test context-aware follow-up commands"""
    
    print("🧪 TESTING CONTEXT-AWARE FOLLOW-UP COMMANDS")
    print("=" * 60)
    
    # Initialize Chotu Autonomous
    chotu = ChouAutonomous()
    
    try:
        # Test 1: Open YouTube
        print("🧪 Step 1: Open YouTube")
        print("-" * 40)
        result1 = await chotu.process_user_input("Open Chrome and search youtube.com")
        print(f"📊 Result: Success" if "successful" in result1.lower() else f"📊 Result: {result1[:100]}...")
        
        # Small delay
        await asyncio.sleep(2)
        
        # Test 2: Follow-up search command (the failing scenario)
        print("\n🧪 Step 2: Follow-up search command")
        print("-" * 40)
        print("Testing: 'in YouTube search box right Alka Yagnik songs'")
        result2 = await chotu.process_user_input("in YouTube search box right Alka Yagnik songs")
        print(f"📊 Result: Success" if "successful" in result2.lower() else f"📊 Result: {result2[:150]}...")
        
        # Test 3: Alternative follow-up patterns
        await asyncio.sleep(2)
        print("\n🧪 Step 3: Alternative follow-up pattern")
        print("-" * 40)
        print("Testing: 'search for Hindi songs on YouTube'")
        result3 = await chotu.process_user_input("search for Hindi songs on YouTube")
        print(f"📊 Result: Success" if "successful" in result3.lower() else f"📊 Result: {result3[:150]}...")
        
        print("\n" + "=" * 60)
        print("🎉 CONTEXT FOLLOW-UP TESTS COMPLETED!")
        print("=" * 60)
        
        # Show context state
        print(f"\n📊 CONTEXT STATE:")
        print(f"   Last Website: {chotu.last_website}")
        print(f"   Last Action: {chotu.last_action}")
        print(f"   Recent Commands: {len(chotu.recent_commands)}")
        
        for i, cmd in enumerate(chotu.recent_commands[-3:], 1):
            print(f"   {i}. {cmd['command'][:50]}...")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n🧹 Cleaning up...")
        try:
            if hasattr(chotu, 'autonomous_executor') and chotu.autonomous_executor:
                chotu.autonomous_executor.shutdown()
                print("✅ Browser closed successfully")
        except Exception as e:
            print(f"⚠️  Shutdown warning: {e}")

if __name__ == "__main__":
    print("🤖 Context-Aware Follow-up Command Test")
    asyncio.run(test_context_follow_up())
