#!/usr/bin/env python3
"""
Test Voice Command Integration for Autonomous System
This script tests the "open chrome" command that was previously failing
"""

import time
import asyncio
import requests
from chotu_autonomous import ChouAutonomous

async def test_autonomous_chrome_command():
    """Test the autonomous system chrome opening command"""
    print("🧪 Testing Autonomous Chrome Command")
    print("=" * 50)
    
    try:
        # Initialize autonomous system
        print("1. Initializing autonomous system...")
        autonomous = ChouAutonomous()
        print("✅ Autonomous system initialized")
        
        # Test the command that was failing
        test_command = "open chrome"
        print(f"\n2. Testing command: '{test_command}'")
        
        # Process the command (now properly await the async function)
        result = await autonomous.process_user_input(test_command)
        
        print(f"\n3. Result:")
        print(f"   Response: {result}")
        
        # Check if the result indicates success (no error prefix)
        if result and not result.startswith("❌"):
            print("✅ Command executed successfully!")
        else:
            print(f"❌ Command failed: {result}")
            
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()

def test_mcp_server_connection():
    """Test if MCP server is responding"""
    print("\n🌐 Testing MCP Server Connection")
    print("=" * 50)
    
    try:
        # Check server status
        response = requests.get("http://localhost:8000/status", timeout=5)
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            print("✅ MCP server is responding")
        else:
            print("⚠️  MCP server responded but with non-200 status")
            
    except requests.ConnectionError:
        print("❌ Cannot connect to MCP server - is it running?")
    except requests.Timeout:
        print("❌ MCP server connection timed out")
    except Exception as e:
        print(f"❌ MCP server test failed: {e}")

async def main():
    """Main async function"""
    print("🚀 Voice Command Integration Test")
    print("This tests the autonomous system that was integrated into Chotu")
    print("=" * 60)
    
    # Test MCP server first
    test_mcp_server_connection()
    
    # Wait a moment
    await asyncio.sleep(2)
    
    # Test autonomous command
    await test_autonomous_chrome_command()
    
    print("\n🏁 Test completed!")

if __name__ == "__main__":
    asyncio.run(main())
