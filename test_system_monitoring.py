#!/usr/bin/env python3
"""
🧪 TEST CHOTU'S SYSTEM MONITORING LEARNING
==========================================
Test Chotu's ability to learn system monitoring capabilities
"""

import sys
sys.path.append('.')

from enhanced_learning_controller import EnhancedSelfLearningController

def test_system_monitoring():
    print("🧪 Testing Chotu's System Monitoring Learning")
    print("=" * 60)
    
    controller = EnhancedSelfLearningController()
    
    # Test request for system monitoring
    test_request = """I need a macOS system monitoring tool that can:
    
1. Check CPU usage and temperature
2. Monitor memory usage and available RAM
3. Check disk space on all mounted volumes
4. Monitor battery status and health
5. List running processes and resource usage
6. Get system uptime and load averages

The tool should return structured data and work on macOS Monterey with proper error handling."""
    
    print(f"🎯 Test Request: System Monitoring Tool")
    print(f"📝 Details: {test_request}")
    print("\n🚀 Starting enhanced learning process...\n")
    
    try:
        result = controller.handle_new_request_enhanced(test_request)
        
        print("\n📊 Learning Result:")
        print(f"Status: {result.get('status', 'Unknown')}")
        print(f"Message: {result.get('message', 'No message')}")
        
        if result.get('tool_path'):
            print(f"Generated Tool: {result['tool_path']}")
            print(f"Tool Name: {result.get('tool_name', 'Unknown')}")
            
            # Test the generated tool
            print("\n🔬 Testing Generated Tool:")
            return test_generated_tool(result['tool_path'])
        
        return result.get('status') == 'success'
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_generated_tool(tool_path):
    """Test the generated system monitoring tool"""
    try:
        import importlib.util
        import os
        
        tool_name = os.path.basename(tool_path).replace('.py', '')
        spec = importlib.util.spec_from_file_location(tool_name, tool_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        print(f"✅ Tool imported successfully: {tool_name}")
        
        # Try to find and test functions
        functions = [attr for attr in dir(module) if callable(getattr(module, attr)) and not attr.startswith('_')]
        functions = [f for f in functions if f != 'main']
        
        print(f"🔧 Found functions: {functions}")
        
        # Test one function if available
        if functions:
            test_func = getattr(module, functions[0])
            print(f"🧪 Testing function: {functions[0]}")
            
            try:
                result = test_func()
                print(f"✅ Function test successful!")
                print(f"📊 Result type: {type(result)}")
                if isinstance(result, dict):
                    print(f"📋 Status: {result.get('status', 'No status')}")
                return True
            except Exception as e:
                print(f"⚠️ Function test failed: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Tool test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_system_monitoring()
    print(f"\n🏆 FINAL RESULT: {'SUCCESS' if success else 'FAILED'} 🏆")
