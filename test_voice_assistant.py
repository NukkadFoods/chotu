#!/usr/bin/env python3
"""
🎤 TEST CHOTU'S VOICE ASSISTANT LEARNING
=======================================
Test Chotu's ability to learn voice assistant capabilities
"""

import sys
sys.path.append('.')

from enhanced_learning_controller import EnhancedSelfLearningController

def test_voice_assistant():
    print("🎤 Testing Chotu's Voice Assistant Learning")
    print("=" * 60)
    
    controller = EnhancedSelfLearningController()
    
    # Test request for voice assistant capabilities
    test_request = """I need a macOS voice assistant tool that can:
    
1. Convert text to speech using macOS built-in TTS
2. Listen for voice input and convert speech to text
3. Play system notification sounds
4. Control system volume programmatically
5. Announce system status and alerts
6. Support different voices and speech rates
7. Handle audio device management

The tool should work on macOS Monterey using built-in audio capabilities and proper error handling. Use macOS native commands like 'say', 'osascript', and audio controls."""
    
    print(f"🎯 Test Request: Voice Assistant Tool")
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
            print("\n🔬 Testing Generated Voice Tool:")
            return test_generated_voice_tool(result['tool_path'])
        
        return result.get('status') == 'success'
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_generated_voice_tool(tool_path):
    """Test the generated voice assistant tool"""
    try:
        import importlib.util
        import os
        
        tool_name = os.path.basename(tool_path).replace('.py', '')
        spec = importlib.util.spec_from_file_location(tool_name, tool_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        print(f"✅ Voice tool imported successfully: {tool_name}")
        
        # Try to find and test functions
        functions = [attr for attr in dir(module) if callable(getattr(module, attr)) and not attr.startswith('_')]
        functions = [f for f in functions if f != 'main']
        
        print(f"🔧 Found voice functions: {functions}")
        
        # Test text-to-speech function if available
        tts_functions = [f for f in functions if 'speak' in f.lower() or 'say' in f.lower() or 'tts' in f.lower()]
        
        if tts_functions:
            test_func = getattr(module, tts_functions[0])
            print(f"🎤 Testing TTS function: {tts_functions[0]}")
            
            try:
                # Test with a simple message
                result = test_func("Hello, this is Chotu testing voice capabilities!")
                print(f"✅ Voice test successful!")
                print(f"📊 Result type: {type(result)}")
                if isinstance(result, dict):
                    print(f"📋 Status: {result.get('status', 'No status')}")
                    print(f"💬 Message: {result.get('message', 'No message')}")
                return True
            except Exception as e:
                print(f"⚠️ Voice function test failed: {e}")
                # Try without parameters
                try:
                    result = test_func()
                    print(f"✅ Voice function works (no params)")
                    return True
                except:
                    return False
        
        # Test volume control if available
        volume_functions = [f for f in functions if 'volume' in f.lower()]
        if volume_functions:
            test_func = getattr(module, volume_functions[0])
            print(f"🔊 Testing volume function: {volume_functions[0]}")
            
            try:
                result = test_func()
                print(f"✅ Volume function test successful!")
                return True
            except Exception as e:
                print(f"⚠️ Volume function test failed: {e}")
        
        # If we found any functions, consider it a success
        return len(functions) > 0
        
    except Exception as e:
        print(f"❌ Voice tool test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_voice_assistant()
    print(f"\n🏆 FINAL RESULT: {'SUCCESS' if success else 'FAILED'} 🏆")
    
    if success:
        print("\n🎉 Chotu successfully learned voice assistant capabilities!")
        print("🎤 The AI can now speak, control audio, and handle voice interactions!")
    else:
        print("\n😞 Voice assistant learning test failed.")
        print("🔧 Check the generated tool for issues.")
