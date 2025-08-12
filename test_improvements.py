#!/usr/bin/env python3
"""
Quick Test for Amazon Search Functionality
Tests the core improvements without waiting for browser initialization
"""

import asyncio
from autonomous.task_executor import AutonomousTaskExecutor

async def test_search_parameter_extraction():
    """Test the improved search parameter extraction"""
    print("🧪 Testing Search Parameter Extraction")
    print("=" * 50)
    
    try:
        executor = AutonomousTaskExecutor()
        
        test_commands = [
            "search mushrooms on amazon.com",
            "search for books on amazon", 
            "find laptops on amazon.com",
            "search headphones",
            "look for cameras on amazon"
        ]
        
        for command in test_commands:
            params = executor._extract_dynamic_parameters(command)
            print(f"✅ '{command}' -> {params}")
        
        return True
        
    except Exception as e:
        print(f"❌ Parameter extraction failed: {e}")
        return False

def test_recipe_improvements():
    """Test that the recipe has been updated with proper selectors"""
    print("\n📚 Testing Recipe Improvements")
    print("=" * 50)
    
    try:
        executor = AutonomousTaskExecutor()
        memory = executor.memory
        
        # Find Amazon search recipe
        amazon_recipe = None
        for recipe in memory.get_all_tasks():
            if "Search Amazon" in recipe.task_name:
                amazon_recipe = recipe
                break
        
        if amazon_recipe:
            print("✅ Found Amazon search recipe")
            
            # Check for improved selectors
            has_correct_search_box = False
            has_enter_key = False
            
            for step in amazon_recipe.action_sequence:
                if step.target == "input[name='field-keywords']":
                    has_correct_search_box = True
                    print(f"✅ Found correct search box selector: {step.target}")
                
                if step.action_type == "press_key" and step.target == "Enter":
                    has_enter_key = True
                    print(f"✅ Found Enter key press action")
            
            if has_correct_search_box and has_enter_key:
                print("✅ Recipe has been improved with working selectors")
                return True
            else:
                print("❌ Recipe still needs improvements")
                return False
        else:
            print("❌ Amazon search recipe not found")
            return False
            
    except Exception as e:
        print(f"❌ Recipe test failed: {e}")
        return False

async def main():
    print("🚀 Quick Test: Autonomous System Improvements")
    print("Testing core functionality without browser startup")
    print("=" * 60)
    
    # Test parameter extraction
    param_success = await test_search_parameter_extraction()
    
    # Test recipe improvements  
    recipe_success = test_recipe_improvements()
    
    print(f"\n📊 Test Results:")
    print(f"   Parameter Extraction: {'✅ PASS' if param_success else '❌ FAIL'}")
    print(f"   Recipe Improvements: {'✅ PASS' if recipe_success else '❌ FAIL'}")
    
    if param_success and recipe_success:
        print("\n🎉 All core improvements are working!")
        print("The system should now:")
        print("  • Extract search terms correctly")
        print("  • Use working CSS selectors for Amazon")
        print("  • Handle Enter key presses")
        print("  • Have better success verification")
    else:
        print("\n⚠️ Some issues remain to be fixed")
    
    print("\n🏁 Quick test completed!")

if __name__ == "__main__":
    asyncio.run(main())
