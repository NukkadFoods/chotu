#!/usr/bin/env python3
"""
Chotu Text-Only Mode - Test your enhancements without audio issues
"""
import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import Chotu without audio components
from chotu_autonomous import ChouAutonomous

async def test_text_mode():
    """Test Chotu in text-only mode"""
    print("🤖 CHOTU TEXT-ONLY MODE")
    print("=" * 50)
    print("Testing your enhanced Chotu without audio!")
    print("Type 'quit' to exit")
    print("=" * 50)
    
    # Initialize Chotu
    chotu = ChouAutonomous()
    
    while True:
        try:
            # Get text input
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'stop']:
                print("🤖 Chotu: Goodbye!")
                break
            
            if not user_input:
                continue
            
            print(f"🤖 Chotu: Processing '{user_input}'...")
            
            # Process the command
            result = await chotu.process_user_input(user_input)
            
            print(f"🤖 Chotu: {result}")
            
        except KeyboardInterrupt:
            print("\n🤖 Chotu: Interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            
    # Cleanup
    try:
        if hasattr(chotu, 'autonomous_executor') and chotu.autonomous_executor:
            chotu.autonomous_executor.shutdown()
            print("✅ Browser closed successfully")
    except Exception as e:
        print(f"⚠️  Shutdown warning: {e}")

if __name__ == "__main__":
    print("🚀 Starting Chotu in Text-Only Mode...")
    print("💡 This avoids the audio error while testing your enhancements!")
    
    # Test suggestions
    print("\n🎯 Try these commands to test your fixes:")
    print("   1. 'Open Chrome and go to youtube.com'")
    print("   2. 'Open a new tab and go to google.com'")
    print("   3. 'search for your favorite songs'")
    print("   4. 'go to instagram.com'")
    
    asyncio.run(test_text_mode())
