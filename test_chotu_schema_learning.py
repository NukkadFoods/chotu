#!/usr/bin/env python3
"""
Test Chotu's schema-driven learning capability
"""

import sys
import os

# Add the project root to the path
sys.path.append('/Users/mahendrabahubali/chotu')

try:
    from enhanced_learning_controller import EnhancedSelfLearningController
    
    print("🧪 Testing Chotu's Enhanced Schema-Driven Learning")
    print("=" * 60)
    
    # Create enhanced controller
    controller = EnhancedSelfLearningController()
    
    # Test request for network management
    test_request = """I need a network management tool that can:
1. Scan for available WiFi networks  
2. Check Bluetooth status
3. Toggle Bluetooth on/off
4. Test network connection quality

This should work specifically on macOS Monterey and use the correct system commands."""
    
    print(f"🎯 Test Request: {test_request}")
    print("\n🚀 Starting enhanced learning process...\n")
    
    # Run enhanced learning
    result = controller.handle_new_request_enhanced(test_request)
    
    print("\n📊 Learning Result:")
    print(f"Status: {result.get('status', 'Unknown')}")
    print(f"Message: {result.get('message', 'No message')}")
    
    if result.get('tool_file'):
        print(f"Generated Tool: {result['tool_file']}")
        
        # Check if the generated tool exists and show a preview
        if os.path.exists(result['tool_file']):
            print("\n📝 Generated Tool Preview:")
            with open(result['tool_file'], 'r') as f:
                lines = f.readlines()
                for i, line in enumerate(lines[:20]):  # Show first 20 lines
                    print(f"{i+1:2d}: {line.rstrip()}")
                if len(lines) > 20:
                    print(f"... ({len(lines) - 20} more lines)")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all required modules are available")
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
