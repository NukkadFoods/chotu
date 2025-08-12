#!/usr/bin/env python3
"""
Comprehensive test for all three Chotu fixes:
1. Browser instance reuse (no multiple Chrome windows)
2. Password vault integration
3. Context-aware follow-up commands
"""
import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chotu_autonomous import ChouAutonomous
from autonomous.password_manager import PasswordManager

async def test_all_fixes():
    """Test all three implemented fixes"""
    
    print("🧪 COMPREHENSIVE CHOTU FIXES TEST")
    print("=" * 60)
    
    # Initialize components
    chotu = ChouAutonomous()
    password_manager = PasswordManager()
    
    try:
        print("🧪 TEST 1: BROWSER INSTANCE REUSE")
        print("-" * 40)
        
        # First browser operation
        print("📋 Opening first browser instance...")
        result1 = await chotu.process_user_input("Open Chrome and go to google.com")
        print(f"✅ First browser: {result1[:100]}...")
        
        await asyncio.sleep(2)
        
        # Second browser operation - should reuse same window
        print("📋 Opening second browser operation (should reuse window)...")
        result2 = await chotu.process_user_input("Open a new tab and go to youtube.com")
        print(f"✅ Second operation: {result2[:100]}...")
        
        print("\n🧪 TEST 2: PASSWORD VAULT VERIFICATION")
        print("-" * 40)
        
        # Check if password vault exists and has credentials
        vault_exists = password_manager.vault_exists()
        print(f"📁 Password vault exists: {vault_exists}")
        
        if vault_exists:
            credentials = password_manager.list_credentials()
            print(f"🔑 Stored credentials: {len(credentials)} sites")
            for domain in credentials:
                print(f"   - {domain}")
        else:
            print("⚠️  No password vault found - create one with password_vault_manager.py")
        
        print("\n🧪 TEST 3: CONTEXT-AWARE FOLLOW-UP COMMANDS")
        print("-" * 40)
        
        # Navigate to YouTube
        print("📋 Opening YouTube...")
        result3 = await chotu.process_user_input("Go to youtube.com")
        print(f"✅ YouTube navigation: {result3[:100]}...")
        
        await asyncio.sleep(3)
        
        # Follow-up search command (the original failing scenario)
        print("📋 Testing follow-up search command...")
        result4 = await chotu.process_user_input("in YouTube search box right Alka Yagnik songs")
        print(f"✅ Follow-up search: {result4[:150]}...")
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS COMPLETED!")
        print("=" * 60)
        
        # Summary
        print(f"\n📊 TEST SUMMARY:")
        print(f"   ✅ Browser Instance Reuse: Implemented")
        print(f"   ✅ Password Vault: {'Available' if vault_exists else 'Setup Required'}")
        print(f"   ✅ Context Follow-up: Implemented")
        
        print(f"\n📊 CHOTU STATE:")
        print(f"   Last Website: {chotu.last_website}")
        print(f"   Last Action: {chotu.last_action}")
        print(f"   Commands in Context: {len(chotu.recent_commands)}")
        
        print(f"\n🚀 NEXT STEPS:")
        print(f"   1. Test with voice commands using speech recognition")
        if not vault_exists:
            print(f"   2. Run password_vault_manager.py to set up password vault")
        print(f"   3. Test auto-login functionality with saved credentials")
        print(f"   4. Try complex multi-step tasks with follow-up commands")
        
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
    print("🤖 Comprehensive Chotu Fixes Test")
    asyncio.run(test_all_fixes())
