#!/usr/bin/env python3
"""
Test Parameter Extraction and Recipe Loading
"""

import asyncio
from chotu_autonomous import ChouAutonomous

async def test_parameter_extraction():
    """Test dynamic parameter extraction without browser"""
    print("🧪 Testing Parameter Extraction")
    print("=" * 50)
    
    try:
        autonomous = ChouAutonomous()
        executor = autonomous.autonomous_executor
        
        # Test different search commands
        test_commands = [
            "search mushrooms on amazon.com",
            "search for books on amazon",
            "find laptops on amazon.com",
            "look for headphones on google.com",
            "search cameras",
        ]
        
        for command in test_commands:
            params = executor._extract_dynamic_parameters(command)
            print(f"Command: '{command}' -> Parameters: {params}")
        
        return "✅ Parameter extraction test completed"
        
    except Exception as e:
        print(f"❌ Parameter extraction test failed: {e}")
        import traceback
        traceback.print_exc()
        return f"❌ Error: {e}"

async def test_recipe_loading():
    """Test recipe loading and matching"""
    print("\n📚 Testing Recipe Loading and Matching")
    print("=" * 50)
    
    try:
        autonomous = ChouAutonomous()
        executor = autonomous.autonomous_executor
        memory = executor.memory
        
        # List all loaded recipes
        recipes = memory.get_all_tasks()
        print(f"Loaded {len(recipes)} recipes:")
        
        for recipe in recipes:
            print(f"  - {recipe.task_name}: {recipe.trigger_phrases}")
        
        # Test trigger matching
        test_commands = [
            "open chrome",
            "search mushrooms on amazon.com",
            "navigate to google",
        ]
        
        for command in test_commands:
            recipe = memory.find_task_by_trigger(command)
            if recipe:
                print(f"✅ '{command}' -> Found recipe: {recipe.task_name}")
            else:
                print(f"❌ '{command}' -> No recipe found")
        
        return "✅ Recipe loading test completed"
        
    except Exception as e:
        print(f"❌ Recipe loading test failed: {e}")
        import traceback
        traceback.print_exc()
        return f"❌ Error: {e}"

async def main():
    print("🚀 Testing Core Autonomous System Components")
    print("Testing without browser initialization")
    print("=" * 60)
    
    # Test parameter extraction
    param_result = await test_parameter_extraction()
    print(f"\n{param_result}")
    
    # Test recipe loading
    recipe_result = await test_recipe_loading()
    print(f"\n{recipe_result}")
    
    print("\n🏁 Core component tests completed!")

if __name__ == "__main__":
    asyncio.run(main())
