#!/usr/bin/env python3
"""
Quick verification that all three fixes are implemented
"""

print("🤖 CHOTU FIXES VERIFICATION")
print("=" * 50)

# Test 1: Check browser instance reuse implementation
print("🧪 TEST 1: Browser Instance Reuse")
try:
    with open('autonomous/action_engine.py', 'r') as f:
        content = f.read()
        if '_browser_instances' in content and 'Reusing existing browser instance' in content:
            print("   ✅ Browser instance reuse: IMPLEMENTED")
        else:
            print("   ❌ Browser instance reuse: NOT FOUND")
except Exception as e:
    print(f"   ❌ Error checking browser reuse: {e}")

# Test 2: Check password vault implementation  
print("\n🧪 TEST 2: Password Vault")
try:
    from autonomous.password_manager import PasswordManager
    pm = PasswordManager()
    if hasattr(pm, 'vault_exists') and hasattr(pm, 'save_credentials'):
        print("   ✅ Password vault: IMPLEMENTED")
        
        # Check if vault file can be created
        vault_exists = pm.vault_exists()
        print(f"   📁 Vault file exists: {vault_exists}")
        
    else:
        print("   ❌ Password vault: MISSING METHODS")
except Exception as e:
    print(f"   ❌ Error checking password vault: {e}")

# Test 3: Check context awareness implementation
print("\n🧪 TEST 3: Context Awareness")
try:
    with open('chotu_autonomous.py', 'r') as f:
        content = f.read()
        if '_enhance_with_context' in content and 'recent_commands' in content:
            print("   ✅ Context awareness: IMPLEMENTED")
        else:
            print("   ❌ Context awareness: NOT FOUND")
except Exception as e:
    print(f"   ❌ Error checking context awareness: {e}")

# Test 4: Check YouTube search recipe
print("\n🧪 TEST 4: YouTube Search Recipe")
try:
    import json
    with open('autonomous/memory/task_recipes.json', 'r') as f:
        recipes_data = json.load(f)
        youtube_found = False
        
        # Check if any task has YouTube in its name
        for task_id, task_data in recipes_data.items():
            if 'YouTube' in task_data.get('task_name', ''):
                youtube_found = True
                break
        
        if youtube_found:
            print("   ✅ YouTube search recipe: FOUND")
        else:
            print("   ❌ YouTube search recipe: NOT FOUND")
except Exception as e:
    print(f"   ❌ Error checking YouTube recipe: {e}")

print("\n" + "=" * 50)
print("🎯 VERIFICATION COMPLETE")
print("\nℹ️  This verification checks that all code fixes are in place.")
print("   To test actual functionality, try these commands:")
print("   1. 'Open Chrome and go to youtube.com'")
print("   2. 'Open a new tab and go to google.com'") 
print("   3. 'search for your favorite songs'")
print("=" * 50)
