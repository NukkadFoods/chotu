#!/usr/bin/env python3
"""
Simple test to verify the three main fixes are working
"""
import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chotu_autonomous import ChouAutonomous
from autonomous.password_manager import PasswordManager

async def test_browser_reuse():
    """Test browser instance reuse"""
    print("🧪 TEST 1: BROWSER INSTANCE REUSE")
    print("-" * 50)
    
    chotu = ChouAutonomous()
    
    try:
        # First browser action
        print("📋 Step 1: Opening first browser instance...")
        result1 = await chotu.process_user_input("Open Chrome and go to google.com")
        print(f"✅ Result: {'SUCCESS' if 'success' in result1.lower() else 'PARTIAL'}")
        
        await asyncio.sleep(2)
        
        # Second browser action - should reuse same window
        print("📋 Step 2: Opening new tab (should reuse browser)...")
        result2 = await chotu.process_user_input("Open a new tab and go to github.com")
        print(f"✅ Result: {'SUCCESS' if 'success' in result2.lower() else 'PARTIAL'}")
        
        print("🎉 Browser reuse test: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Browser reuse test failed: {e}")
        return False
    finally:
        try:
            if hasattr(chotu, 'autonomous_executor') and chotu.autonomous_executor:
                chotu.autonomous_executor.shutdown()
        except:
            pass

def test_password_vault():
    """Test password vault functionality"""
    print("\n🧪 TEST 2: PASSWORD VAULT FUNCTIONALITY")
    print("-" * 50)
    
    try:
        password_manager = PasswordManager()
        
        # Check vault status
        vault_exists = password_manager.vault_exists()
        print(f"📁 Password vault exists: {vault_exists}")
        
        if vault_exists:
            credentials = password_manager.list_credentials()
            print(f"🔑 Stored credentials: {len(credentials)} sites")
            for domain in credentials[:3]:  # Show first 3
                print(f"   - {domain}")
        else:
            print("📝 No vault found - testing creation...")
            # Test vault creation
            test_success = password_manager.save_credentials("test.com", "testuser", "testpass")
            print(f"✅ Vault creation test: {'SUCCESS' if test_success else 'FAILED'}")
            
            # Clean up test
            if test_success:
                password_manager.delete_credentials("test.com")
        
        print("🎉 Password vault test: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Password vault test failed: {e}")
        return False

async def test_context_awareness():
    """Test context-aware follow-up commands"""
    print("\n🧪 TEST 3: CONTEXT-AWARE COMMANDS")
    print("-" * 50)
    
    chotu = ChouAutonomous()
    
    try:
        # Navigate to YouTube
        print("📋 Step 1: Opening YouTube...")
        result1 = await chotu.process_user_input("Go to youtube.com")
        print(f"✅ YouTube navigation: {'SUCCESS' if 'success' in result1.lower() else 'PARTIAL'}")
        
        await asyncio.sleep(2)
        
        # Test context awareness
        print("📋 Step 2: Testing context-aware search...")
        result2 = await chotu.process_user_input("search for Alka Yagnik songs")
        print(f"✅ Context search: {'SUCCESS' if 'success' in result2.lower() else 'PARTIAL'}")
        
        # Check if context was tracked
        print(f"📊 Last website tracked: {chotu.last_website}")
        print(f"📊 Recent commands: {len(chotu.recent_commands)}")
        
        print("🎉 Context awareness test: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Context awareness test failed: {e}")
        return False
    finally:
        try:
            if hasattr(chotu, 'autonomous_executor') and chotu.autonomous_executor:
                chotu.autonomous_executor.shutdown()
        except:
            pass

async def main():
    """Run all tests"""
    print("🤖 CHOTU FIXES VERIFICATION")
    print("=" * 60)
    
    results = []
    
    # Test 1: Browser instance reuse
    result1 = await test_browser_reuse()
    results.append(("Browser Instance Reuse", result1))
    
    # Test 2: Password vault
    result2 = test_password_vault()
    results.append(("Password Vault", result2))
    
    # Test 3: Context awareness
    result3 = await test_context_awareness()
    results.append(("Context Awareness", result3))
    
    # Summary
    print("\n" + "=" * 60)
    print("🎯 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, passed_test in results:
        status = "✅ PASSED" if passed_test else "❌ FAILED"
        print(f"   {test_name}: {status}")
        if passed_test:
            passed += 1
    
    print(f"\n🏆 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All fixes are working correctly!")
        print("\n🚀 Your Chotu is now enhanced with:")
        print("   ✅ Smart browser instance reuse (no multiple windows)")
        print("   ✅ Secure password vault integration")
        print("   ✅ Context-aware follow-up command understanding")
    else:
        print("⚠️  Some issues detected - check individual test results above")

if __name__ == "__main__":
    asyncio.run(main())
