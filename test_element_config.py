#!/usr/bin/env python3
"""
Quick Test for Amazon Search Fix
"""

import asyncio
from chotu_autonomous import ChouAutonomous

async def test_amazon_search_quick():
    """Quick test of Amazon search element finding"""
    print("🧪 Quick Amazon Search Element Test")
    print("=" * 50)
    
    try:
        autonomous = ChouAutonomous()
        
        # Test parameter extraction
        command = "search mushrooms on amazon.com"
        print(f"Testing command: '{command}'")
        
        # Extract parameters manually to verify
        params = autonomous.autonomous_executor._extract_dynamic_parameters(command)
        print(f"Extracted parameters: {params}")
        
        # Test the recipe finding
        recipe = autonomous.autonomous_executor.memory.find_task_by_trigger(command)
        if recipe:
            print(f"Found recipe: {recipe.task_name}")
            print(f"Action sequence steps: {len(recipe.action_sequence)}")
            
            # Show the click step
            for i, step in enumerate(recipe.action_sequence):
                if step.action_type == "click":
                    print(f"Step {i+1}: {step.action_type} -> target: '{step.target}', value: '{step.value}'")
        else:
            print("No recipe found")
        
        return "✅ Element configuration verified"
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return f"❌ Error: {e}"

async def main():
    print("🚀 Quick Element Finding Test")
    print("Verifying Amazon search configuration")
    print("=" * 50)
    
    result = await test_amazon_search_quick()
    print(f"\n{result}")

if __name__ == "__main__":
    asyncio.run(main())
